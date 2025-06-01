import cv2
import pytesseract
import time
import os

# Set Tesseract path (change if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load Haar cascade for Indian plates
cascade_path = os.path.join("cascade", "indian_license_plate.xml")
plate_cascade = cv2.CascadeClassifier(cascade_path)

# Create output directories if not exist
os.makedirs("output_plates", exist_ok=True)
os.makedirs("output_texts", exist_ok=True)

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

start_time = time.time()
plate_count = 0

print("🎥 Detecting plates for 30 seconds...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera error.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    for (x, y, w, h) in plates:
        plate_img = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # ▶️ Determine aspect ratio
        aspect_ratio = w / h
        if 0.7 < aspect_ratio < 1.3:
            print(f"[{plate_count}] 🔲 Square plate detected")
        else:
            print(f"[{plate_count}] 🟥 Rectangular plate detected")

        # Choose OCR config based on shape
        ocr_config = '--psm 6' if 0.7 < aspect_ratio < 1.3 else '--psm 8'

        # OCR
        plate_text = pytesseract.image_to_string(plate_img, config=ocr_config)
        cleaned_text = plate_text.strip().replace("\n", " ").replace("\x0c", "")
        print(f"   🔠 Plate Text: {cleaned_text}")

        # Save plate image
        img_path = f"output_plates/plate{plate_count}.jpg"
        cv2.imwrite(img_path, plate_img)

        # Save plate text
        text_path = f"output_texts/plate{plate_count}.txt"
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        # Show text on frame
        cv2.putText(frame, cleaned_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        plate_count += 1

    # Show live video
    cv2.imshow("Live License Plate Detection", frame)

    # Stop after 30 seconds or if user presses 'q'
    if time.time() - start_time > 30:
        print("⏱️ 30 seconds elapsed. Stopping...")
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Stopped by user.")
        break

cap.release()
cv2.destroyAllWindows()
