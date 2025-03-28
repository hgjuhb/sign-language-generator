import cv2
import mediapipe as mp

def handDetextion(image_path):
    res = []
    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
        max_num_hands=2,
        model_complexity=1,
        min_detection_confidence=0.2,
        min_tracking_confidence=0.2,
        static_image_mode=True) as hands:

        img = cv2.imread(image_path)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img2)
        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[i].classification[0].label
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                res.append([handedness, landmarks])
    return res