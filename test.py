from asyncio import transports
from sklearn.neighbors import KNeighborsClassifier
# pyrefly: ignore [missing-import]
import cv2
import pickle
import os
import csv
import time
from datetime import datetime
import sys
# pyrefly: ignore [missing-import]
import numpy as np

def speak(str1):
    try:
        from win32com.client import Dispatch
        speaker = Dispatch("SAPI.SpVoice")
        speaker.Speak(str1)
    except Exception as e:
        print(f"[Speech]: {str1}")

# Configuration
PREVENT_DUPLICATES_SAME_DAY = False  # Set to True if a person can only mark attendance once per day

# Locate Haar Cascade classifier
cascade_paths = [
    'data/haarcascade_frontalface_default.xml',
    'haarcascade_frontalface_default.xml',
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
]
cascade_file = next((p for p in cascade_paths if os.path.exists(p)), None)
if cascade_file is None:
    print("Error: haarcascade_frontalface_default.xml not found.")
    exit(1)

facedetect = cv2.CascadeClassifier(cascade_file)

# Load names/labels
if not os.path.exists('data/names.pkl'):
    print("Error: data/names.pkl not found. Please run add_faces.py first.")
    exit(1)

with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)

# Support either faces_data.pkl or faces.pkl
faces_file = 'data/faces_data.pkl' if os.path.exists('data/faces_data.pkl') else ('data/faces.pkl' if os.path.exists('data/faces.pkl') else None)
if faces_file is None:
    print("Error: Face data file not found in data/. Please run add_faces.py first.")
    exit(1)

with open(faces_file, 'rb') as f:
    FACES = pickle.load(f)

print('Loaded faces from:', faces_file)
print('Shape of Faces matrix -->', FACES.shape)
print('Number of Labels -->', len(LABELS))

if FACES.shape[0] != len(LABELS):
    print(f"Warning: Number of faces ({FACES.shape[0]}) does not match number of labels ({len(LABELS)}).")

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("background.png")
COL_NAMES = ['NAME', 'TIME']
os.makedirs("Attendance", exist_ok=True)

# Geometry for placing video inside the background image
if imgBackground is not None:
    bg_h, bg_w = imgBackground.shape[:2]
    if bg_w == 1024 and bg_h == 682:
        # Proper rectangular coordinates that completely cover the card and its blue border
        VX, VY, VW, VH = 119, 122, 786, 423
    else:
        VX, VY, VW, VH = 55, 162, 640, 480
else:
    VX, VY, VW, VH = 0, 0, 640, 480

# Determine input source: static image (e.g. from screenshot 'fb-team.jpeg') or webcam
image_mode = False
image_path = None
if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    image_mode = True
    image_path = sys.argv[1]
    print(f"Running in image mode on: {image_path}")
    source_img = cv2.imread(image_path)
    if source_img is None:
        print(f"Error: Could not load image '{image_path}'.")
        exit(1)
else:
    video = cv2.VideoCapture(0)
    print("Running in live camera mode. Press 'o' to mark attendance, 'q' to quit.")

while True:
    if image_mode:
        frame = source_img.copy()
    else:
        ret, frame = video.read()
        if not ret or frame is None:
            print("Warning: Could not read frame from camera.")
            break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    attendances = []
    seen_names = set()
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

    # Process all detected faces in the current frame/image (like 'for box in bboxes' in screenshot)
    for (x, y, w, h) in faces:
        x2, y2 = x + w, y + h
        crop_img = frame[max(0, y):max(0, y2), max(0, x):max(0, x2), :]
        if crop_img.size == 0 or crop_img.shape[0] == 0 or crop_img.shape[1] == 0:
            continue

        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        name = str(output[0])

        # Drawing bounding box & name tag for each face (using x2, y2 = x + w, y + h)
        cv2.rectangle(frame, (x, y), (x2, y2), (50, 50, 255), 2)
        y_label = max(y, 40)
        cv2.rectangle(frame, (x, y_label - 40), (x2, y_label), (50, 50, 255), -1)
        cv2.putText(frame, name, (x, y_label - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)

        # Collect unique recognized individuals in this frame
        if name not in seen_names:
            seen_names.add(name)
            attendances.append([name, str(timestamp)])

    # Display on background
    if imgBackground is not None:
        display_frame = imgBackground.copy()
        resized_frame = cv2.resize(frame, (VW, VH))
        display_frame[VY:VY + VH, VX:VX + VW] = resized_frame
    else:
        display_frame = frame

    cv2.imshow("Smart Attendance System", display_frame)
    k = cv2.waitKey(1 if not image_mode else 30)

    if k == ord('o'):
        if attendances:
            csv_path = f"Attendance/Attendance_{date}.csv"
            file_exists = os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0

            # Optional check for same-day duplicates
            already_marked = set()
            if PREVENT_DUPLICATES_SAME_DAY and file_exists:
                try:
                    with open(csv_path, "r", newline="") as cf:
                        reader = csv.reader(cf)
                        next(reader, None)
                        for row in reader:
                            if row:
                                already_marked.add(row[0].strip())
                except Exception:
                    pass

            records_to_write = []
            skipped_names = []
            for record in attendances:
                name = record[0]
                if PREVENT_DUPLICATES_SAME_DAY and name in already_marked:
                    skipped_names.append(name)
                else:
                    records_to_write.append(record)

            if records_to_write:
                with open(csv_path, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(COL_NAMES)
                    for record in records_to_write:
                        writer.writerow(record)

                names_list = [r[0] for r in records_to_write]
                if len(names_list) == 1:
                    spoken_names = names_list[0]
                else:
                    spoken_names = ", ".join(names_list[:-1]) + " and " + names_list[-1]

                print(f"Recorded attendance for {len(records_to_write)} person(s): {', '.join(names_list)}")
                speak(f"Attendance taken for {spoken_names}")
            elif skipped_names:
                print(f"Already marked today: {', '.join(skipped_names)}")
                speak(f"{', '.join(skipped_names)} already marked today")

            time.sleep(1)
        else:
            print("No face detected to take attendance.")
            speak("No face detected")

    if k == ord('q'):
        break

if not image_mode:
    video.release()
cv2.destroyAllWindows()


