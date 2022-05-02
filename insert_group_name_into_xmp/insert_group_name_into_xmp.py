import os


def insert_group_name_and_save_new_file(root_dir, output_dir=None):
    """
    在 xmp 文件中插入“group name”属性，并将文件写入新的文件
    :param root_dir: 需要处理的 xmp 文件所在的文件夹
    :param output_dir: 输出新文件的文件夹，如果传入空，则默认在原文件夹下面新建 result 文件夹
    :return: 没有返回值
    """
    if not os.path.exists(root_dir):
        print("the dir %s does not exists!!!" % root_dir)
        return
    root_dir = root_dir.strip(r"\\")
    count = 0
    output_root_dir = None
    for dir_path in os.listdir(root_dir):
        sub_absolute_dir_path = os.path.join(root_dir, dir_path)
        if not os.path.isdir(sub_absolute_dir_path):
            print("path <%s> is not a dir, read next..." % sub_absolute_dir_path)
            continue
        sub_result_dir = make_dir_of_result(root_dir, dir_path, output_dir)
        if output_root_dir is None:
            output_root_dir = sub_result_dir[0:sub_result_dir.rfind("\\") + 1]
        group_name = dir_path
        for file_path in os.listdir(sub_absolute_dir_path):
            absolute_origin_file_path = os.path.join(sub_absolute_dir_path, file_path)
            if not check_is_valid_file(absolute_origin_file_path):
                continue
            absolute_result_file_path = os.path.join(sub_result_dir, file_path)
            print("read < %s > and insert group name and then save to a new file: %s" % (
                absolute_origin_file_path, absolute_result_file_path))
            if write_result_to_file(absolute_origin_file_path, absolute_result_file_path, group_name):
                count += 1
    print("\nCongrats! Convert %d files successfully, check result in dir: %s" % (count, output_root_dir))


def make_dir_of_result(root_dir, group_name, output_dir=None):
    # 检验生成结果的的目录，如果不存在则新建默认的结果目录
    if output_dir is None:
        result_dir = os.path.join(root_dir.strip(r"\\"), r"result", group_name)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
    else:
        result_dir = os.path.join(output_dir.strip(r"\\"), group_name)
        if os.path.isdir(result_dir) and (not os.path.exists(result_dir)):
            os.makedirs(result_dir)
    return result_dir


def check_is_valid_file(file_path):
    if os.path.isdir(file_path):
        print("<%s> is a dir, read the next..." % file_path)
        return False

    if not (os.path.splitext(file_path)[-1][1:].upper() == r"XMP"):
        print("<%s> is not a xmp file, read the next..." % file_path)
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
                    # group name 的标签开始部分：<crs:Group>，下偏移第 2 行填写 group name
                    right_arrow_idx = lines[index + 2].rfind(r"<")
                    left_arrow_idx = lines[index + 2].find(r">")
                    # 如果right_arrow_idx - left_arrow_idx >= 2，说明已经有 group name，不需要修改
                    if right_arrow_idx - left_arrow_idx <= 1:
                        # 最后结果应该是这样<rdf:li xml:lang="x-default">Fuji</rdf:li>
                        lines[index + 2] = "     <rdf:li xml:lang=\"x-default\">%s</rdf:li>\n" % group_name
                output_file.write(line)
            return True
    except IOError:
        print("IOError")
        return False


if __name__ == '__main__':
    # 将 xmp 文件按目录存放在C:\Users\work 目录中，程序会将子目录作为group—name。如C:\Users\work\Fuji，C:\Users\work\Kodak
    DIR_OF_XMP_FILES = r"C:\Users\work"
    # 可选，默认保存在 DIR_OF_XMP_FILES\result\
    DIR_OF_OUTPUT_RESULT = None
    insert_group_name_and_save_new_file(DIR_OF_XMP_FILES, DIR_OF_OUTPUT_RESULT)
