import os
import sys
from database import init_db
from plate_detector import detect_plate

def main():
    init_db()

    # If a folder path is provided via command line (from GUI)
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        # Default folder for manual or fallback usage
        folder = 'test_images'

    # Ensure folder exists
    if not os.path.isdir(folder):
        print(f"Folder not found: {folder}")
        return

    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder, filename)
            print(f"Processing {file_path}...")
            detect_plate(file_path)

if __name__ == '__main__':
    main()
