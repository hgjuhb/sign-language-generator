import numpy as np

def normalize_hand(landmarks, face_center, face_width, face_height, image_width, image_height):
    """
    根據臉部中心座標將手部移動到畫面中的目標位置。
    face_center 是相對於畫面尺寸的(0~1)座標。
    """

    # 計算偏移量
    dx = face_center[0] * image_width - 320 # x軸偏移量，將臉部中心調整到畫面中間
    dy = face_center[1] * image_height - 50 # y軸偏移量，將臉部中心調整到畫面中間偏上

    fw = face_width * image_width
    fh = face_height * image_height

    sx = 100 / fw if fw != 0 else 1  # x軸縮放比例
    sy = 150 / fh if fh != 0 else 1  # y軸縮放比例

    transformed_points = []

    # 根據偏移量移動手部座標
    for x, y, z in landmarks:
        new_x = (x * image_width  - dx) * sx
        new_y = (y * image_height - dy) * sy # 計算新的 y 座標
        transformed_points.append([new_x, new_y, z])  # 保持 z 座標不變
    return transformed_points