import database
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

mp_drawing = mp.solutions.drawing_utils      
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def createLandmarks(coordinates):
    landmarks = []
    for coordinate in coordinates:
        x = coordinate[0]/ 640
        y = coordinate[1]/ 480
        z = coordinate[2]

        landmarks.append(landmark_pb2.NormalizedLandmark(x=x, y=y, z=z))

    hand_landmarks = landmark_pb2.NormalizedLandmarkList(landmark=landmarks)
    return hand_landmarks

def drawHand():
    img = np.zeros((480, 640, 3), dtype=np.uint8)

    while True:
        word = str(input("Enter a word (e.g., 'wash face'): "))
        frames = database.GetCoordinatesByWord(word)
        
        for frame in frames:
            for tags in frame:
                if len(tags) == 0:
                    continue
                print(f"Processing {len(tags)} landmarks...")


                # 創建 hand_landmarks 並繪製
                hand_landmarks = createLandmarks(tags)
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                cv2.imshow('Hand Landmarks', img)
            cv2.waitKey(10)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            img.fill(0)    

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

drawHand()
