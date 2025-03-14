from ultralytics import YOLO
import cv2
import math

def preprocess_frame(frame):
    # Resize the frame to 640x640
    resized_frame = cv2.resize(frame, (640, 640))
    return resized_frame


def video_detection(path_x):
    video_capture = path_x
    # Webcam Object
    cap = cv2.VideoCapture(video_capture)

    model = YOLO("static/best_naga.pt")
    classNames = ["bunga", "matang", "mentah", "semi-matang"]

    while True:
        success, img = cap.read()
        if not success:
            break

        # Preprocess the frame
        img = preprocess_frame(img)
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                conf = math.ceil((box.conf[0]*100))/100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                print(t_size)
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1, y1-2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
        yield img


cv2.destroyAllWindows()
