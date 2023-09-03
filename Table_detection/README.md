# Table_detection
基于OpenCV的图像中表格的识别(Table recognition in image based on OpenCV)

1.识别横线
进行腐蚀和膨胀操作，去除图像中的干扰项，把部分不清晰的横线连起来
![识别横线的效果](https://github.com/GreatJM/Table_detection/blob/main/line/horizontal_line.jpg)

2.识别竖线
进行腐蚀和膨胀操作，去除图像中的干扰项，把部分不清晰的竖线连起来
![识别竖线的效果](https://github.com/GreatJM/Table_detection/blob/main/line/dilated_row.jpg)

3.将竖线和横线组合起来
![将竖线和横线组合起来的效果](https://github.com/GreatJM/Table_detection/blob/main/line/table_segment.jpg)

4.最后输出在原图中识别的表格
![原图识别表格的效果](https://github.com/GreatJM/Table_detection/blob/main/table_detection_img/table_detection_INV8.jpg)