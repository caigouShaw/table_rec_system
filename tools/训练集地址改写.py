input_file = r"C:\Users\Alex\Desktop\MyTrainDataSet\result1.txt"
output_file = r"C:\Users\Alex\Desktop\MyTrainDataSet\result1.txt"

prefix = 'line1/'

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = [prefix + line for line in lines]

with open(output_file, 'w') as f:
    f.writelines(new_lines)
