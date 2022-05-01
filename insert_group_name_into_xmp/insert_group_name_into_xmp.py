import os


def insert_group_name_and_save_new_file(file_dir, group_name, new_file_dir=None):
    """
    在 xmp 文件中插入“group name”属性，并将文件写入新的文件
    :param file_dir: 需要处理的 xmp 文件所在的文件夹
    :param group_name:
    :param new_file_dir: 输出新文件的文件夹，如果传入空，则默认在原文件夹下面新建 result 文件夹
    :return: 没有返回值
    """
    if not os.path.exists(file_dir):
        print("the dir %s does not exists!!!")
        return

    result_dir = make_dir_of_result(file_dir, new_file_dir)

    file_path_list = os.listdir(file_dir)
    count = 0
    for file_path in file_path_list:
        absolute_file_path = os.path.join(file_dir, file_path)
        if not check_is_valid_file(absolute_file_path):
            continue

        new_absolute_file_path = os.path.join(result_dir, file_path)
        print("read < %s > and insert group name and then save to a new file: %s" % (file_path, new_absolute_file_path))
        if write_result_to_file(absolute_file_path, new_absolute_file_path, group_name):
            count += 1
    print("\nCongrats! Convert %d files successfully, check result in dir: %s" % (count, result_dir))


def make_dir_of_result(file_dir, new_file_dir=None):
    # 检验生成结果的的目录，如果不存在则新建默认的结果目录
    if (new_file_dir is None) or (not os.path.exists(new_file_dir)):
        result_dir = file_dir.strip(r"\\") + r"\result"
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        return result_dir


def check_is_valid_file(file_path):
    if os.path.isdir(file_path):
        print("<%s> is a dir, read the next..." % file_path)
        return False

    if os.path.getsize(file_path) <= 0:
        print(r"file <%s> is empty, read the next..." % file_path)
        return False
    return True


def write_result_to_file(absolute_file_path, new_absolute_file_path, group_name):
    try:
        with open(absolute_file_path, "r", encoding="utf-8") as input_file, open(new_absolute_file_path, "w",
                                                                                 encoding="utf-8") as output_file:
            lines = input_file.readlines()
            for index, line in enumerate(lines):
                if r'<crs:Group>' in line:
                    # group name 的标签开始部分：<crs:Group>，下面两行填写 group name
                    group_name_line = lines[index + 2].strip("\n")
                    line = group_name_line + "%s</rdf:li>\n" % group_name
                output_file.write(line)
            return True
    except IOError:
        print("IOError")
        return False


if __name__ == '__main__':
    dir_of_xmp_files = r"C:\user\xmp"
    group_name = r"Fuji"
    # 可选，默认保存在 dir_of_xmp_files\result\
    dir_of_output_result = r""
    insert_group_name_and_save_new_file(dir_of_xmp_files, group_name, dir_of_output_result)
