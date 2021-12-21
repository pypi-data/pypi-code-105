def mycopyfile(srcfile,dstpath):                  # 复制函数 srcfile：文件名，dstpath复制路径
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
        shutil.copy(srcfile, os.path.join(dstpath,fname))   