import os
import cv2
"""基于OpenCV的图像中表格的识别"""


def delete_images(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            os.remove(file_path)
            print(f"Deleted {file_path}")

folder_to_delete = "line"
delete_images(folder_to_delete)

def table_detection(img_path):
    img = cv2.imread(img_path, 1)
    # 灰度图片
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 图片二值化
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    # 二进制非操作
    # binary = cv2.bitwise_not(binary)

    """识别出横线和竖线"""
    rows, cols = binary.shape
    # scale值越大，检测到的直线越多
    scale = 40
    # 自适应获取核值
    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    # 腐蚀
    eroded = cv2.erode(binary, kernel, iterations=1)
    # 膨胀
    dilated_col = cv2.dilate(eroded, kernel, iterations=1)
    cv2.imwrite("other_res/horizontal_line.jpg", dilated_col)

    # 识别横线
    # scale值越大，检测到的直线越多
    scale = 30
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated_row = cv2.dilate(eroded, kernel, iterations=1)
    cv2.imwrite("other_res/dilated_row.jpg", dilated_row)

    # 将横线和竖线组合起来形成一个表格
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    table_segment = cv2.addWeighted(dilated_row, 0.5, dilated_col, 0.5, 0.0)
    table_segment = cv2.erode(cv2.bitwise_not(table_segment), kernel, iterations=2)
    thresh, table_segment = cv2.threshold(table_segment, 0, 255, cv2.THRESH_OTSU)
    cv2.imwrite("other_res/table_segment.jpg", table_segment)

    # 寻找物体的轮廓
    contours, hierarchy = cv2.findContours(table_segment, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = []

    i = 1
    for c in contours:
        # 找到矩形框
        x, y, w, h = cv2.boundingRect(c)
        # (x,y)和(x+w,y+h)代表矩形左上角和右下角的两个点
        #print(w * h)
        if w * h <= 99999:
            bounding_boxes.append([x, y, x + w, y + h])
            # 根据坐标截取图片
            cropped_image = img[y:y + h, x:x + w]
            cv2.imwrite("line/Crop_{0}.jpg".format(i), cropped_image)
            i = i + 1

    for cell in bounding_boxes:
        # 通过bounding_boxes画出图形
        cv2.rectangle(img, (cell[0], cell[1]), (cell[2], cell[3]), (0, 255, 0), 2)


    # 输出图片
    cv2.imwrite("results//table_detection_res.jpg", img)

    #写入坐标
    #result_file = "C:/Users/Alex/PycharmProjects/Table_rec_system/Table_detection/results/pos_res.txt"
    result_file = "results/pos_res.txt"
    i = 0
    with open(result_file, 'w') as f:
        for pos in bounding_boxes:
            i = i + 1
            f.write('{} '.format(i) + ','.join(map(str, pos)) + '\n')
    f.close()


# 图片的输入,为img文件夹中的图片

img_path = r"C:\Users\Alex\PycharmProjects\Table_rec_system\Table_detection\img\1.jpg"
#img_path = "TiltCorrectionOutput/outputFilled.jpg"
table_detection(img_path)
