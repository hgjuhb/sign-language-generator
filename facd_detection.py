import cv2
import mediapipe as mp
import numpy as np

def face_detection(image_path):
    # 初始化MediaPipe FaceMesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,  # 設置為動態影像模式
        max_num_faces=1,  # 偵測最多1張臉
        min_detection_confidence=0.5,  # 設置最小臉部檢測信心
        min_tracking_confidence=0.5  # 設置最小臉部追蹤信心
    )

    # 讀取影像
    image = cv2.imread(image_path)  # 替換成你的圖像路徑
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 轉換為RGB格式

    # 偵測臉部
    results = face_mesh.process(image_rgb)

    # 計算並回傳臉部中心座標
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 提取臉部關鍵點
            face_points = [(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark]

            # 計算臉部的中心
            min_vals = np.min(face_points, axis=0)
            max_vals = np.max(face_points, axis=0)
            center = (min_vals + max_vals) / 2  # 中心點
            
            face_width = max_vals[0] - min_vals[0]
            face_height = max_vals[1] - min_vals[1]

            # 將臉部中心座標從[0, 1]範圍轉換為影像像素座標
            # image_height, image_width, _ = image.shape
            # center_x = int(center[0] * image_width)
            # center_y = int(center[1] * image_height)
            
            # 顯示臉部中心座標
            return [[center[0], center[1]], face_width, face_height]
            # print(f"Face Center Coordinates: ({center[0]}, {center[1]})")
    else:
        return []