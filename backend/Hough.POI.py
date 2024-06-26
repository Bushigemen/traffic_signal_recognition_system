import cv2
import numpy as np

# 读取图片
img = cv2.imread('D:\python project\pythonProject1\pictures\R-C.jpg')

# 确保图片读取成功
if img is None:
    print("Error: Could not read the image.")
    exit()

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 应用高斯模糊以减少图像噪声
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 假设你知道图像中圆形的大致半径范围
min_radius = 10  # 最小半径
max_radius = 60# 最大半径

# 使用霍夫圆检测
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 2, 2*min_radius,
                           param1=40, param2=40,
                           minRadius=min_radius, maxRadius=max_radius)

# 确保找到了圆
if circles is not None:
    # 将坐标和半径从浮点数转换为整数
    circles = np.uint16(np.around(circles))

    # 遍历检测到的每个圆
    for (x, y, radius) in circles[0, :]:
        # 计算包含圆的边界框（这里简单地使用半径的两倍作为宽高）
        left = max(0, x - radius)
        top = max(0, y - radius)
        right = min(img.shape[1], x + radius)
        bottom = min(img.shape[0], y + radius)

        # 裁剪出包含圆的图像区域
        circle_roi = img[top:bottom, left:right]

        # 绘制圆形和圆心（仅用于调试，可以注释掉）
        cv2.circle(circle_roi, (x - left, y - top), radius, (0, 255, 0), 2)
        cv2.circle(circle_roi, (x - left, y - top), 2, (0, 0, 255), -1)

        # 显示或保存裁剪出的图像区域（这里只是显示，您可以选择保存）
        cv2.imshow(f'Detected circle {x},{y}', circle_roi)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No circles detected.")