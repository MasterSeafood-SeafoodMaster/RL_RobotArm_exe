import cv2
import os

# 設定影片路徑和輸出圖片的目錄
video_path = './T&B.mp4'  # 替換為你的影片檔案路徑
output_dir = './img'  # 替換為你想要的輸出目錄

# 如果輸出目錄不存在，則創建它
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 打開影片檔案
cap = cv2.VideoCapture(video_path)

# 確認影片是否成功打開
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 讀取影片的幀數
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 循環遍歷影片的每一幀
frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_idx%5==0:
        # 構建輸出圖片的檔名
        frame_filename = os.path.join(output_dir, f'frame_{frame_idx:04d}.jpg')

        # 將幀儲存為圖片
        cv2.imwrite(frame_filename, frame)

    frame_idx += 1

# 釋放影片對象
cap.release()

print(f"Saved {frame_idx} frames to {output_dir}")
