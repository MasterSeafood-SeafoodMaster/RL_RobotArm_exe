imgp="C:\\Users\\cfouo\\Desktop\\dataset\\images\\i_test.png"
txtp="C:\\Users\\cfouo\\Desktop\\dataset\\labels\\l_test.txt"

import cv2


with open(txtp, 'r') as file:
    lines = file.readlines()

coordinates = [list(map(float, line.split())) for line in lines]

# 讀取圖片
img = cv2.imread(imgp)

# 在圖片上畫框
for coord in coordinates:
    x1, y1, x2, y2 = [int(c) for c in coord]
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 顯示圖片
cv2.imshow('Image with Bounding Boxes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()



