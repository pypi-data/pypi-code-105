'''
Created on 2021年9月14日

@author: 86139

TODO 
'''
import os
class BatchRename():
    # 批量重命名文件夹中的图片文件
    def __init__(self):
        self.path = './3_images' #表示需要命名处理的文件夹
    def rename(self):
        filelist = os.listdir(self.path)      #获取文件路径
        total_num = len(filelist)             #获取文件长度（个数）
        print(total_num)
        i = 1                                 #表示文件的命名是从1开始的
        for item in filelist:
            # print(item)
            file_name=item.split('.',-1)[0]
            # print(file_name)
            src = os.path.join(os.path.abspath(self.path), item)
            # print(src)
            dst = os.path.join(os.path.abspath(self.path), file_name + '.jpg')
            # print(dst)

            try:
                os.rename(src, dst)
                print ('converting %s to %s ...' % (src, dst))
                i = i + 1
            except:
                continue
        print ('total %d to rename & converted %d jpgs' % (total_num, i))
if __name__ == '__main__':
    demo = BatchRename()
    demo.rename() 