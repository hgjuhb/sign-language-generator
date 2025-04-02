import hand_detection
import video_splitter
import database

import os
import shutil



def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
            except Exception as e:
                print(f"刪除 {file_path} 時發生錯誤: {e}")
    else:
        print(f"資料夾 {folder_path} 不存在")

def read_text_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

database.createDatabase()
database.resetDatabase()


folder_path = './videos'
labels = read_text_file_to_list("./labels.text")

file_names = os.listdir(folder_path)

for file_name in file_names:
    word = labels.pop(0)
    if(database.insertWord(word)):
        path = folder_path + "/" + file_name
        video_splitter.videoSplitter(path, "./frames", 16)
        image_names = os.listdir("./frames")
        for i, image_name in enumerate(image_names):
            result = hand_detection.handDetextion("./frames/" + image_name)
            database.insertFrame(word, i)
            tmp = ""
            for handness, coordinates in result:
                # print(i, handness)
                if tmp == handness:
                    tmp = "Right" if handness == "Left" else "Left"
                else:
                    tmp = handness
                for j, coordinate in enumerate(coordinates):
                    database.insertTag(word, i, j, tmp, coordinate[0], coordinate[1], coordinate[2])
        clear_folder("./frames")