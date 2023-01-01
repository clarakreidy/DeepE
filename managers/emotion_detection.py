import pandas as pd
import cv2
import time

from deepface import DeepFace
from deepface.commons import functions
from deepface.detectors import FaceDetector


def analysis(time_threshold=0.4, frame_threshold=5):

    detector_backend = 'opencv'
    pivot_img_size = 112  # face recognition result image
    face_detector = FaceDetector.build_model(detector_backend)
    emotion_model = DeepFace.build_model('Emotion')
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    # -----------------------

    freeze = False
    face_detected = False
    face_included_frames = 0  # freeze screen if face detected sequentially 5 frames
    freezed_frame = 0
    tic = time.time()

    # -----------------------

    webcam = cv2.VideoCapture(0)

    while True:
        ret, img = webcam.read()

        if img is None:
            break

        img = cv2.flip(img, 1)
        raw_img = img.copy()
        resolution_x = img.shape[1]

        if not freeze:

            try:
                # faces store list of detected_face and region pair
                faces = FaceDetector.detect_faces(face_detector, detector_backend, img, align=False)
            except:  # to avoid exception if no face detected
                faces = []

            if len(faces) == 0:
                face_included_frames = 0
        else:
            faces = []

        detected_faces = []
        face_index = 0
        for face, (x, y, w, h) in faces:
            if w > 130:  # discard small detected faces

                face_detected = True
                if face_index == 0:
                    face_included_frames = face_included_frames + 1  # increase frame for a single face

                cv2.rectangle(img, (x, y), (x + w, y + h), (67, 67, 67), 1)  # draw rectangle to main image

                # -------------------------------------

                detected_faces.append((x, y, w, h))
                face_index = face_index + 1

        # -------------------------------------

        if face_detected and face_included_frames == frame_threshold and not freeze:
            freeze = True
            base_img = raw_img.copy()
            detected_faces_final = detected_faces.copy()
            tic = time.time()

        if freeze:

            toc = time.time()
            if (toc - tic) < time_threshold:

                if freezed_frame == 0:
                    freeze_img = base_img.copy()

                    for detected_face in detected_faces_final:
                        x = detected_face[0]
                        y = detected_face[1]
                        w = detected_face[2]
                        h = detected_face[3]

                        # draw rectangle to main image
                        cv2.rectangle(freeze_img, (x, y), (x + w, y + h), (67, 67, 67), 1)
                        face = base_img[y:y + h, x:x + w]
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
                        overlay = freeze_img.copy()
                        opacity = 0.4

                        if x + w + pivot_img_size < resolution_x:
                            # right
                            cv2.rectangle(freeze_img
                                          , (x + w, y)
                                          , (x + w + pivot_img_size, y + h)
                                          , (64, 64, 64), cv2.FILLED)

                            cv2.addWeighted(overlay, opacity, freeze_img, 1 - opacity, 0, freeze_img)

                        elif x - pivot_img_size > 0:
                            # left
                            cv2.rectangle(freeze_img
                                          , (x - pivot_img_size, y)
                                          , (x, y + h)
                                          , (64, 64, 64), cv2.FILLED)

                            cv2.addWeighted(overlay, opacity, freeze_img, 1 - opacity, 0, freeze_img)

                        for index, instance in emotion_df.iterrows():
                            emotion_label = "%s " % (instance['emotion'])
                            emotion_score = instance['score'] / 100

                            bar_x = 35  # this is the size if an emotion is 100%
                            bar_x = int(bar_x * emotion_score)

                            if x + w + pivot_img_size < resolution_x:

                                text_location_y = y + 20 + (index + 1) * 20
                                text_location_x = x + w

                                if text_location_y < y + h:
                                    cv2.putText(freeze_img, emotion_label, (text_location_x, text_location_y),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                                    cv2.rectangle(freeze_img
                                                  , (x + w + 70, y + 13 + (index + 1) * 20)
                                                  , (x + w + 70 + bar_x, y + 13 + (index + 1) * 20 + 5)
                                                  , (255, 255, 255), cv2.FILLED)

                            elif x - pivot_img_size > 0:

                                text_location_y = y + 20 + (index + 1) * 20
                                text_location_x = x - pivot_img_size

                                if text_location_y <= y + h:
                                    cv2.putText(freeze_img, emotion_label, (text_location_x, text_location_y),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                                    cv2.rectangle(freeze_img
                                                  , (x - pivot_img_size + 70, y + 13 + (index + 1) * 20)
                                                  , (x - pivot_img_size + 70 + bar_x, y + 13 + (index + 1) * 20 + 5)
                                                  , (255, 255, 255), cv2.FILLED)

                        tic = time.time()  # in this way, freezed image can show 5 seconds

                # -------------------------------

                ret, buffer = cv2.imencode('.jpg', freeze_img)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                freezed_frame = freezed_frame + 1
            else:
                face_detected = False
                face_included_frames = 0
                freeze = False
                freezed_frame = 0

        else:
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    webcam.release()
    cv2.destroyAllWindows()
