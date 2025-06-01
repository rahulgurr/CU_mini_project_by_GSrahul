import cv2
import pytesseract
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load Indian plate cascade
cascade_path = os.path.join("cascade", "indian_license_plate.xml")
plate_cascade = cv2.CascadeClassifier(cascade_path)

# Ensure output folder exists
os.makedirs("output_plates", exist_ok=True)
os.makedirs("output_texts", exist_ok=True)

def detect_plate(image_path):
    print(f"Processing {image_path}...")

    # Read image
    img = cv2.imread(image_path)    
    if img is None:
        print(f"Image not found or unreadable: {image_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect plates
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    if len(plates) == 0:
        print("No plates detected.")
        return

    filename_base = os.path.splitext(os.path.basename(image_path))[0]

    for i, (x, y, w, h) in enumerate(plates):
        # Extract plate region
        plate_img = img[y:y+h, x:x+w]
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # OCR
        plate_text = pytesseract.image_to_string(plate_img, config='--psm 8')
        cleaned_text = plate_text.strip().replace("\n", " ").replace("\x0c", "")
        print(f"Detected Plate Text: {cleaned_text}")

        # Save plate image
        plate_img_path = f"output_plates/{filename_base}_plate{i}.jpg"
        cv2.imwrite(plate_img_path, plate_img)

        # Save plate text
        text_output_path = f"output_texts/{filename_base}_plate{i}.txt"
        with open(text_output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

    # Optional: show image with rectangles
    cv2.imshow("Detected Plates", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
