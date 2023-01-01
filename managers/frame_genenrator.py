import cv2
from deepface import DeepFace

emotion_model = DeepFace.build_model('Emotion')


def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            # gray_img = preprocess_face(img=custom_face, target_size=(48, 48), grayscale=True,
            #                                      enforce_detection=False, detector_backend='opencv')
            # emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
            # emotion_predictions = emotion_model.predict(gray_img)[0, :]
            # sum_of_predictions = emotion_predictions.sum()
            #
            # mood_items = []
            # for i in range(0, len(emotion_labels)):
            #     mood_item = []
            #     emotion_label = emotion_labels[i]
            #     emotion_prediction = 100 * emotion_predictions[i] / sum_of_predictions
            #     mood_item.append(emotion_label)
            #     mood_item.append(emotion_prediction)
            #     mood_items.append(mood_item)
            #
            # emotion_df = pd.DataFrame(mood_items, columns=["emotion", "score"])
            # emotion_df = emotion_df.sort_values(by=["score"], ascending=False).reset_index(drop=True)
            #
            # # background of mood box
            #
            # # transparency
            # overlay = freeze_img.copy()
            # opacity = 0.4
            #
            # if x + w + pivot_img_size < resolution_x:
            #     # right
            #     cv2.rectangle(freeze_img
            #                   # , (x+w,y+20)
            #                   , (x + w, y)
            #                   , (x + w + pivot_img_size, y + h)
            #                   , (64, 64, 64), cv2.FILLED)
            #
            #     cv2.addWeighted(overlay, opacity, freeze_img, 1 - opacity, 0, freeze_img)
            #
            # elif x - pivot_img_size > 0:
            #     # left
            #     cv2.rectangle(freeze_img
            #                   # , (x-pivot_img_size,y+20)
            #                   , (x - pivot_img_size, y)
            #                   , (x, y + h)
            #                   , (64, 64, 64), cv2.FILLED)
            #
            #     cv2.addWeighted(overlay, opacity, freeze_img, 1 - opacity, 0, freeze_img)
            #
            # for index, instance in emotion_df.iterrows():
            #     emotion_label = "%s " % (instance['emotion'])
            #     emotion_score = instance['score'] / 100
            #
            #     bar_x = 35  # this is the size if an emotion is 100%
            #     bar_x = int(bar_x * emotion_score)
            #
            #     if x + w + pivot_img_size < resolution_x:
            #
            #         text_location_y = y + 20 + (index + 1) * 20
            #         text_location_x = x + w
            #
            #         if text_location_y < y + h:
            #             cv2.putText(freeze_img, emotion_label, (text_location_x, text_location_y),
            #                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            #
            #             cv2.rectangle(freeze_img
            #                           , (x + w + 70, y + 13 + (index + 1) * 20)
            #                           , (x + w + 70 + bar_x, y + 13 + (index + 1) * 20 + 5)
            #                           , (255, 255, 255), cv2.FILLED)
            #
            #     elif x - pivot_img_size > 0:
            #
            #         text_location_y = y + 20 + (index + 1) * 20
            #         text_location_x = x - pivot_img_size
            #
            #         if text_location_y <= y + h:
            #             cv2.putText(freeze_img, emotion_label, (text_location_x, text_location_y),
            #                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            #
            #             cv2.rectangle(freeze_img
            #                           , (x - pivot_img_size + 70, y + 13 + (index + 1) * 20)
            #                           , (x - pivot_img_size + 70 + bar_x, y + 13 + (index + 1) * 20 + 5)
            #                           , (255, 255, 255), cv2.FILLED)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if cv2.waitKey(40) == 27:
            break

    cv2.destroyAllWindows()
    camera.release()
