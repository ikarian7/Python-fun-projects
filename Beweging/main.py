import cv2
import pygame
import time
import threading

def play_sound(sound_file):
    pygame.mixer.Sound(sound_file).play()

def detect_motion():
    pygame.mixer.init()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Kan de webcam niet openen.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Resolutie: {frame_width}x{frame_height}")

    roi_w = 200  # Beperkte breedte van de ROI
    roi_h = frame_height
    roi_x = 0  # Begin links
    roi_y = 0

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    ret, frame1 = cap.read()
    if not ret:
        print("Kan het eerste frame niet lezen!")
        return

    roi = frame1[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
    last_refresh_time = time.time()
    refresh_interval = 10
    last_sound_time = 0
    sound_interval = 5
    frame_skip = 2
    frame_count = 0
    motion_active = False

    print("Bewegingsdetectie gestart. Druk op ESC om te stoppen.")

    while True:
        frame_count += 1
        ret, frame2 = cap.read()
        if not ret:
            print("Kan geen frame lezen. Controleer de webcamverbinding.")
            break

        if frame_count % frame_skip != 0:
            continue

        try:
            roi_frame2 = frame2[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
        except Exception as e:
            print(f"Fout bij het ophalen van de ROI: {e}")
            continue

        diff = cv2.absdiff(roi, roi_frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = any(cv2.contourArea(contour) > 1000 for contour in contours)

        roi_gray = cv2.cvtColor(roi_frame2, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame2, (roi_x + x, roi_y + y), (roi_x + x + w, roi_y + y + h), (255, 0, 0), 2)

        if motion_detected and time.time() - last_sound_time > sound_interval:
            threading.Thread(target=play_sound, args=("alert.mp3",)).start()
            last_sound_time = time.time()
            if not motion_active:
                print("Beweging gedetecteerd!")
            motion_active = True

        if not motion_detected and motion_active:
            print("Geen beweging meer gedetecteerd.")
            motion_active = False

        if time.time() - last_refresh_time > refresh_interval:
            roi = roi_frame2
            last_refresh_time = time.time()

        display_frame = cv2.resize(frame2, (1280, 720))
        cv2.rectangle(display_frame, (roi_x * 1280 // frame_width, roi_y), 
                      ((roi_x + roi_w) * 1280 // frame_width, roi_y + roi_h * 720 // frame_height), 
                      (0, 255, 0), 2)
        cv2.imshow("Webcam Feed (HD)", display_frame)

        if cv2.waitKey(10) == 27:
            print("Gestopt.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_motion()

