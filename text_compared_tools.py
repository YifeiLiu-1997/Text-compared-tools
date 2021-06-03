"""
    批量字符串比对工具: 用于将算法部生成的识别结果与手工标注的结果进行比对
    原理: 算法部生成的一系列文件夹中的txt文档与手动标注后改动的txt文档，按照编辑距离统计字符串的正确率并输出
    输入: 存放一系列识别结果的文件夹路径，存放一系列标注后结果的文件夹路径
    输出:
    xx 和 xx 比对，字符数 xx, 正确率 xx
    ...
    总字符数: xx, 总正确率: xx
"""

import Levenshtein
import shutil
import os
import re
import tkinter as tk


# 从src找到其中的文件并复制到dest中
def copy_allfiles(src, dest):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest)


# 创建文件夹，测试用
def create_document(dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    else:
        shutil.rmtree(dest)
        os.mkdir(dest)


# 对比两个txt的每一行，统计每一行字符个数，返回总单词数total_word和整个txt的total_ratio, file1为识别，file2为标注
# 实际上，两个txt的行数理论相等，都是去掉bad pic之后的txt
def compare(file_1, file_2):
    f1 = open(file_1, 'r')
    f2 = open(file_2, 'r')
    list_1 = txt_list(f1)
    list_2 = txt_list(f2)
    total_word = 0
    total_ratio = 0
    for element in range(0, len(list_2)):
        total_word = total_word + len(list_2[element])  # 计算全部字符数量
        ratio = Levenshtein.ratio(list_1[element], list_2[element])  # 计算每一行两字符串的莱温斯坦比
        total_ratio = total_ratio + ratio * len(list_2[element])
    total_ratio = total_ratio / total_word

    answer = (file_1 + ' 和 ' + file_2 + ' 比对\n字符数: %d' % total_word + ', 正确率: %2f' % total_ratio + '\n\n')
    result.insert('insert', answer)  # 插入答案
    return [total_word, total_ratio]


# 找出文件夹中以".txt"结尾的文件并将路径返回
def find_txt(src):
    for files in os.listdir(src):
        if files.endswith('.txt'):
            return os.path.join(src, files)


# 找到一个文件夹下所有txt返回列表
def findall_txt(src):
    list_txt_src = []
    for root, dirs, files in os.walk(src):
        for name in files:
            if re.search('(.*).txt', name):
                list_txt_src.append(os.path.join(root, name))
    return list_txt_src


# 将txt每行存至list
def txt_list(file):
    list_file = []
    for line in file:
        list_file.append(line[0:-1])
    return list_file


# 获取输入的路径
def auto_tools_run():
    result.config(state='normal')
    source_path = input_source_path.get().replace('\\', '/')
    revised_path = input_revised_path.get().replace('\\', '/')

    list_info = []  # 存放关于每个txt词数和ratio的列表
    list_source = findall_txt(source_path)
    list_revised = findall_txt(revised_path)

    # 执行比对算法
    for i in range(0, len(list_revised)):
        list_info.append(compare(list_source[i], list_revised[i]))

    # 计算总识别率
    total_word = 0
    total_ratio = 0
    for i in range(0, len(list_info)):
        total_word = total_word + list_info[i][0]
        total_ratio = total_ratio + list_info[i][0] * list_info[i][1]
    total_ratio = total_ratio / total_word
    answer = '总字符数: %d' % total_word + ', 总正确率: %2f' % total_ratio
    result.insert('insert', answer)
    result.config(state='disabled')


# 清除text的内容
def clear():
    result.config(state='normal')
    result.delete('1.0', 'end')
    result.config(state='disabled')


if __name__ == '__main__':
    print("""
    **************************************************************************************
    批量字符串比对工具: 用于将算法部生成的识别结果与手工标注的结果进行比对
    输入: 
    存放一系列识别结果的文件夹路径，存放一系列标注后结果的文件夹路径
    输出:
    xx 和 xx 比对，字符数 xx, 正确率 xx
    ...
    总字符数: xx, 总正确率: xx
    **************************************************************************************
    """)
    # 实例化object，建立窗口window
    window = tk.Tk()

    # 给窗口的可视化起名字
    window.title('正确率批量识别工具')

    # 设定窗口的大小(长 * 宽)
    window.geometry('1024x768')

    # 在图形界面上设定输入框控件entry框并放置
    tk.Label(text='存放所有 识别结果文件夹 的文件夹路径: ').place(x=80, y=20)
    input_source_path = tk.Entry(window, show=None, width=50)  # 显示成明文形式
    input_source_path.place(x=380, y=20)
    tk.Label(text='存放所有 标注后文件夹 的文件夹路径: ').place(x=80, y=50)
    input_revised_path = tk.Entry(window, width=50)
    input_revised_path.place(x=380, y=50)

    # 创建并放置按钮分别触发两种情况
    button_result = tk.Button(window, text='确定', width=20,
                              height=2, command=auto_tools_run).place(x=200, y=85)
    button_clear = tk.Button(window, text='清除结果', width=20,
                             height=2, command=clear).place(x=400, y=85)

    # 创建并放置一个多行文本框text用以显示，指定height=3为文本框是三个字符高度
    result = tk.Text(window, height=30)
    result.place(x=100, y=150)

    window.mainloop()
