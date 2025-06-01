import cv2
import pytesseract
from ultralytics import YOLO
import os
import time

# ✅ Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ✅ Path to your trained YOLOv8 license plate model (.pt file)
model_path = r'C:\Users\Lenovo\Downloads\Licence-Plate-Recognition-with-YOLOv8-and-Easy-OCR-main\Licence-Plate-Recognition-with-YOLOv8-and-Easy-OCR-main\model1.pt'

# ✅ Load YOLO model
model = YOLO(model_path)

# ✅ Create output folders
os.makedirs("output_plates", exist_ok=True)
os.makedirs("output_texts", exist_ok=True)

# ✅ Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot access the webcam.")
    exit()

print("📷 Starting webcam. Press 'q' to quit early.")
start_time = time.time()
plate_counter = 0

while True:
    success, frame = cap.read()
    if not success:
        print("❌ Failed to grab frame")
        break

    # Detect plates
    results = model(frame)[0]

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"Plate {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Crop and OCR
        plate_img = frame[y1:y2, x1:x2]
        text = pytesseract.image_to_string(plate_img, config='--psm 8')
        clean_text = text.strip().replace("\n", " ").replace("\x0c", "")

        # Detect shape (square or rectangular)
        w, h = x2 - x1, y2 - y1
        aspect_ratio = w / h
        if 0.7 < aspect_ratio < 1.3:
            shape = "🔲 Square plate"
        else:
            shape = "🟥 Rectangular plate"
        print(f"[{shape}] Detected Plate Text: {clean_text}")

        # Save image and text
        plate_path = f"output_plates/plate_{plate_counter}.jpg"
        text_path = f"output_texts/plate_{plate_counter}.txt"

        cv2.imwrite(plate_path, plate_img)
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(clean_text)

        plate_counter += 1

    # Show frame
    cv2.imshow("YOLOv8 License Plate Detection", frame)

    # Exit conditions
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting by key press.")
        break

    if time.time() - start_time > 30:
        print("⏰ 30 seconds reached. Exiting.")
        break

cap.release()
cv2.destroyAllWindows()
