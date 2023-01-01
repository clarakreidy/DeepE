import pandas as pd
import cv2
import time

from deepface import DeepFace
from deepface.commons import functions
from deepface.detectors import FaceDetector


def stream(source=0, time_threshold=0.5):

    previous = time.time()
    delta = 0
    webcam = cv2.VideoCapture(source)

    while True:
        current = time.time()
        delta += current - previous
        previous = current

        _, frame = webcam.read()
        frame = cv2.flip(frame, 1)

        if delta > time_threshold:
            analysis(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    webcam.release()
    cv2.destroyAllWindows()


def analyze(filename):
    path = f"static/bucket/uploads/{filename}"
    image = cv2.imread(path)
    result = analysis(image)
    ret, buffer = cv2.imencode('.jpg', result)
    frame = buffer.tobytes()

    return frame


def analysis(image):
    detector_backend = 'opencv'
    face_detector = FaceDetector.build_model(detector_backend)
    emotion_model = DeepFace.build_model('Emotion')
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    pivot_img_size = 112  # face recognition result image

    resolution_x = image.shape[1]

    faces = FaceDetector.detect_faces(face_detector, detector_backend, image, align=False)
    for face, (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (67, 67, 67), 1)  # draw rectangle to main image
        # facial attribute analysis
        gray_img = functions.preprocess_face(img=face, target_size=(48, 48), grayscale=True,
                                             enforce_detection=False, detector_backend='opencv')
        emotion_predictions = emotion_model.predict(gray_img)[0, :]
        sum_of_predictions = emotion_predictions.sum()

        mood_items = []
        for i in range(0, len(emotion_labels)):
            mood_item = []
            emotion_label = emotion_labels[i]
            emotion_prediction = 100 * emotion_predictions[i] / sum_of_predictions
            mood_item.append(emotion_label)
            mood_item.append(emotion_prediction)
            mood_items.append(mood_item)

        emotion_df = pd.DataFrame(mood_items, columns=["emotion", "score"])
        emotion_df = emotion_df.sort_values(by=["score"], ascending=False).reset_index(drop=True)

        # background of mood box
        # transparency
        overlay = image.copy()
        opacity = 0.4

        if x + w + pivot_img_size < resolution_x:
            # right
            cv2.rectangle(image
                          , (x + w, y)
                          , (x + w + pivot_img_size, y + h)
                          , (64, 64, 64), cv2.FILLED)

            cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0, image)

        elif x - pivot_img_size > 0:
            # left
            cv2.rectangle(image
                          , (x - pivot_img_size, y)
                          , (x, y + h)
                          , (64, 64, 64), cv2.FILLED)

            cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0, image)

        for index, instance in emotion_df.iterrows():
            emotion_label = "%s " % (instance['emotion'])
            emotion_score = instance['score'] / 100

            bar_x = 35  # this is the size if an emotion is 100%
            bar_x = int(bar_x * emotion_score)

            if x + w + pivot_img_size < resolution_x:

                text_location_y = y + 20 + (index + 1) * 20
                text_location_x = x + w

                if text_location_y < y + h:
                    cv2.putText(image, emotion_label, (text_location_x, text_location_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.rectangle(image
                                  , (x + w + 70, y + 13 + (index + 1) * 20)
                                  , (x + w + 70 + bar_x, y + 13 + (index + 1) * 20 + 5)
                                  , (255, 255, 255), cv2.FILLED)

            elif x - pivot_img_size > 0:

                text_location_y = y + 20 + (index + 1) * 20
                text_location_x = x - pivot_img_size

                if text_location_y <= y + h:
                    cv2.putText(image, emotion_label, (text_location_x, text_location_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.rectangle(image
                                  , (x - pivot_img_size + 70, y + 13 + (index + 1) * 20)
                                  , (x - pivot_img_size + 70 + bar_x, y + 13 + (index + 1) * 20 + 5)
                                  , (255, 255, 255), cv2.FILLED)

    return image