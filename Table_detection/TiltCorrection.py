import cv2
import numpy as np
import argparse

def deskew_and_fill(image_path):
    def deskew_table(image):
        # 转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 二值化图像
        _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 检测轮廓
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 寻找最大轮廓
        max_contour = max(contours, key=cv2.contourArea)

        # 进行透视变换
        rect = cv2.minAreaRect(max_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # 计算旋转角度
        angle = rect[-1]

        # 对图像进行旋转矫正
        rows, cols = image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))

        return rotated_image

    # 加载图像
    image = cv2.imread(image_path)

    # 表格倾斜矫正
    corrected_image = deskew_table(image)

    # 填充空白区域
    mask = corrected_image[:, :, 0] == 0  # 提取图像中为黑色的区域
    corrected_image[mask] = 255  # 将黑色区域像素值设置为白色 (255)

    return corrected_image

def main(image_path):
    # 图像文件路径作为参数传递给函数
    corrected_image = deskew_and_fill(image_path)
    # 保存结果等进一步操作
    cv2.imwrite('TiltCorrectionOutput/CorrectedImage.jpg', corrected_image)
    cv2.imwrite('TiltCorrectionOutput/outputFilled.jpg', corrected_image)

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='Table Image Deskew and Fill')

    # 添加图像文件路径参数
    parser.add_argument('image_path', type=str, help='Path to the input image file')

    # 解析命令行参数
    args = parser.parse_args()

    # 调用主函数，并将图像文件路径作为参数传递
    main(args.image_path)