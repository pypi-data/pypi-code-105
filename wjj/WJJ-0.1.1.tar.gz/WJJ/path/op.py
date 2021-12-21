def	All_Folders_Files(path):
    list0 = os.listdir(path)
    list_dir = []
    list_file = []
    for i in list0:
        if os.path.isdir(os.path.join(path,i)):
            list_dir.append(i)
        else:
            list_file.append(i)
    return list_dir, list_file
    
  
  
def All_Files(file_path):
    list=[]
    for curDir, dirs, files in os.walk(file_path):

        if len(files)>0:
            path=[os.path.join(curDir,i) for i in files]
            for j in path:
                list.append(j)
    return list