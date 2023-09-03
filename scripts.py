import subprocess
import os

# 定义要执行的脚本列表和参数
scripts = [
    ('Table_detection/TiltCorrection.py', ["img/3.jpg"]),
    ('Table_detection/table_Detection.py', []),
    ('tools/infer/predict_rec.py',
     ['--image_dir=C:\\Users\\Alex\\PycharmProjects\\Table_rec_system\\Table_detection\\line',
      '--rec_model_dir=C:\\Users\\Alex\\PycharmProjects\\Table_rec_system\\hand-line_rec\\my_rec_model\\Teacher',
      '--rec_char_dict_path=C:\\Users\\Alex\\PycharmProjects\\Table_rec_system\\ppocr\\utils\\ppocr_keys_v1.txt',
      '--det_model_dir=C:\\Users\\Alex\\PycharmProjects\\Table_rec_system\\hand-line_rec\\my_dec_model\\ch_PP-OCRv3_det_infer']),
    ('table_restore/table_generation.py', []),
    ('table_restore/Table_migration.py', []),
]

# 主目录路径
main_dir = 'C:/Users/Alex/PycharmProjects/Table_rec_system'

# 获取当前工作目录
current_dir = os.getcwd()

# 依次执行每个脚本
for script, args in scripts:
    # 构建脚本文件路径
    script_path = main_dir + '/' + script

    try:
        # 切换到子目录
        os.chdir(os.path.dirname(script_path))

        # 构建命令行参数列表
        cmd = ['python', script_path] + args

        # 使用subprocess模块执行shell命令
        subprocess.call(cmd)
    finally:
        # 返回主目录
        os.chdir(current_dir)
