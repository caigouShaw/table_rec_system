from pdf2image import convert_from_path

def pdf_to_images(pdf_path, output_path):
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        image_path = f"{output_path}/image_{i}.jpg"
        image.save(image_path, 'JPEG')
        print(f"保存图像：{image_path}")

# 指定输入PDF文件的路径和输出图像的目录
pdf_path = r"C:\Users\Alex\Documents\WeChat Files\wxid_6r4u3wkeeqa621\FileStorage\File\2023-05\柳州资料1.pdf"
output_path = r"C:\Users\Alex\Desktop\tableimg\test2"

# 调用函数进行PDF到图像的转换
pdf_to_images(pdf_path, output_path)