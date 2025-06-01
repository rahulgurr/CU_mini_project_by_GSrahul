import cv2
import pytesseract
import time
import os
from ultralytics import YOLO

# Set Tesseract path (update this path based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load YOLOv8 model (update the path to your 'model1.pt' file)
model = YOLO('model1.pt')  # Replace with the actual path to your model

# Create output directories if they don't exist
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

    # Run YOLOv8 model on the frame
    results = model(frame)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            plate_img = frame[y1:y2, x1:x2]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Determine aspect ratio
            w = x2 - x1
            h = y2 - y1
            aspect_ratio = w / h
            if 0.7 < aspect_ratio < 1.3:
                print(f"[{plate_count}] 🔲 Square plate detected")
                ocr_config = '--psm 6'  # Multiline OCR
            else:
                print(f"[{plate_count}] 🟥 Rectangular plate detected")
                ocr_config = '--psm 8'  # Single-line OCR

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
            cv2.putText(frame, cleaned_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

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
