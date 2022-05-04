import tensorflow as tf
keras = tf.keras
import cv2
import numpy as np
from random import choice

model = keras.models.load_model("BCS.h5")

CLASS_MAP =  {
    0: "Bird",
    1: "Snake",
    2: "Cow",
    3: "None"
}

def mapper(val):
    return CLASS_MAP[val]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # rectangle for user to play
    cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)
    
    # extract the region of image within the user rectangle
    player_move = frame[25:300, 25:300]
    img = cv2.cvtColor(player_move, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img_blur = cv2.GaussianBlur(img, (3,3), 0)
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
    # predict the move made
    pred = model.predict(np.array([sobelxy]))
    player_move_code = np.argmax(pred[0])
    player_move_name = mapper(player_move_code)
    # print(user_move_name)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: " + player_move_name, (5, 25), font, 1.2, (5, 180, 30), 2, cv2.LINE_AA)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
    cv2.imshow("Bird Cow Snake", frame)
cap.release()
cv2.destroyAllWindows()
