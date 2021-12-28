import re
import os
import zipfile


def decompression(name):
    a = 0
    os.chdir('./')
    if '.zip' in name:
        n = name
    else:
        n = name+'.zip'
    for x in n:
        if x == '.':
            a += 1
    if a >= 2:
        quit(NameError('Error 002: The name does not meet the specification.\n名字不符合规范。'))
    try:
        read_hey = zipfile.ZipFile(n)
    except FileNotFoundError:
        quit(FileNotFoundError('Error 001: File is Not Found.\n错误001：找不到文件。'))
    x = read_hey.namelist()
    try:
        r = os.system('mkdir {}'.format(n[:-4:]))
        if r == 256:
            quit(
                OSError('mkdir: {}: 文件已存在'.format(n[:-4:])))
    except OSError or IOError:
        quit(OSError('Your computer does not support "mkdir" command.\n你的电脑不支持"mkdir"命令'))

    for i in x:
        if '.zip' in i:
            quit(OSError(
                'Error 003: The "zip" file cannot exist ".zip" file.\n.zip文件不能存在于.zip文件中。'))
        content = read_hey.read(i).decode('utf-8')
        print(content)
        with open('./{}/'.format(n[:-4:])+i, 'w')as w:
            w.write(content)

    read_hey.close()
    import platform
    print(platform.system().lower())
    if platform.system().lower() == 'windows':
        os.system('rd /s/q {}'.format(n))
    elif platform.system().lower() == 'linux' or platform.system().lower() == 'unix' or platform.system().lower() == 'mac' or platform.system().lower() == 'darwin':
        os.system('rm -rf {}'.format(n))


def backup2zip(floder, backupfilename):  # floder：要打包的文件夹；backupfilename:指定文件名

    hisname = re.compile(backupfilename + '(_)?(\\d+)?' + '.zip')
    floder = os.path.abspath(floder)
    num = [1]

    allFiles = os.listdir(os.getcwd())  # 历史备份文件名列表
    for i in allFiles:
        mo = hisname.search(i)
        if mo:
            num.append(int(mo.group(2)) + 1)

    backupfilename = backupfilename + '_' + str(num[-1]) + '.zip'
    f = zipfile.ZipFile(backupfilename, 'w')  # c创建一个zip对象

    for floderName, subFolders, fileNames in os.walk(floder):
        f.write(floderName)
        for subFolder in subFolders:
            f.write(os.path.join(floderName, subFolder))
        for fileName in fileNames:
            f.write(os.path.join(floderName, fileName))
    f.close()


# backup2zip('.\\zipexample','backupfile')
backup2zip('./zipp/zipp/index', 'index')
