# import gzip
import os


def load_log_file():
    sqls = []
    for root, dirs, files in os.walk(r"C:\temp"):
        for file in files:
            # 获取文件所属目录
            # print(root)
            # 获取文件路径
            # print(os.path.join(root, file))
            f = None
            if file.startswith('sql-') and file.endswith('.log'):
                print(os.path.join(root, file))
                try:
                    f = open(os.path.join(root, file), mode='r', buffering=-1, encoding=None, errors=None, newline=None,
                             closefd=True, opener=None)
                    while True:
                        text_line = f.readline()
                        if text_line:
                            print(text_line)
                            sqls.append(text_line)
                        else:
                            break
                finally:
                    if f:
                        f.close()

    return sqls


if __name__ == '__main__':
    load_log_file()
