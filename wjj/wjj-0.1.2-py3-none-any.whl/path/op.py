import os


def	all_folders_files(path):
    list0 = os.listdir(path)
    list_dir = []
    list_file = []
    for i in list0:
        if os.path.isdir(os.path.join(path,i)):
            list_dir.append(i)
        else:
            list_file.append(i)
    return list_dir, list_file
    
  
  
def all_files(file_path):
    list=[]
    for curDir, dirs, files in os.walk(file_path):

        if len(files)>0:
            path=[os.path.join(curDir,i) for i in files]
            for j in path:
                list.append(j)
    return list


def path_to_str(path):  # 这个也可以集成函数
    # 先取得文件名路径
    normpath = os.path.normpath(path)  # 转义为通用路径格式
    filepath, _ = os.path.split(normpath)
    Separator = os.sep  # os.sep根据你的平台自动使用分隔符
    part = filepath.split(Separator)  # 字符串根据分隔符分割得到列表
    pathallpart = "-".join(part)  # 第一个往往是.，我们用的都是相对路径所以要去掉
    return pathallpart
