import pygame; import pygame.camera

import keyboard
import math
import time
import random

pygame.init()

def Get_zvt_prost():
        return ['RGB','HSV','YUV']

class Surfases:
    def __init__(self,size=[]):
        self.surf = pygame.Surface((size[0],size[1]))
        surf1 = self.surf
        
    def set_alphal(self,al):
        if al > 255:al=255
        if al < 0:al=0
        self.surf.set_alpha(al)
    def draw_surf(self,pos=[]):
        screen.blit(self.surf,(pos[0],pos[1]))

    def draw_on_surf(self,sr,pos=[]):
        screen.blit(self,sr,(pos[0],pos[1]))

    def fill_surf(self,col=()):
        self.surf.fill(col)

    class Trans:
        def __init__(self):
            pass
        def Theresld(self,img,search_col,thresjd,set_col):
            pygame.transform.threshold(self.surf,img,search_col,thresjd,set_col)
class Kamera:
    def __init__(self,size,zvet_prost='RGB',num=0):
        self.size = size
        pygame.camera.init()
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[num],(size[0],size[1]), zvet_prost)
        self.cam.set_controls(True,False,1)

    def List_cam(self):
        cams = pygame.camera.list_cameras()
        return cams
    
    def Start(self):self.cam.start()

    def End(self):self.cam.stop()

    def Get_img(self):
        img = self.cam.get_image()
        return img

    def Get_size(self):
        width , height = self.cam.get_size()
        return width , height
    
    def Set_setings(self,wflip,hflip,sun):
        self.cam.set_controls(wflip,hflip,sun)

    def Get_setings(self):
        cont = self.cam.get_controls()
        return cont
class TimeGR:
    def __init__(self):
        pass
    def DELY(self,MLsec):
        time.sleep(MLsec)
class FonT:
    def __init__(self):
        pass
    def GETFONTS():
        return pygame.font.get_fonts()

    def PRINText(self,text='',glass=False,col=(),font='arial',pix=0,x=0,y=0):
        textt = pygame.font.SysFont(font,pix)
        texttt = textt.render(text,glass,col)
        screen.blit(texttt,(x,y))
class GPMath:
    def __init__(self):
        pass
    def COS(self,ugl):
        return math.cos(ugl)
    def SIN(self,ugl):
        return math.sin(ugl)
    
    def RAST(self,pos1=[],pos2=[]):
        if pos1[0]>pos2[0]:w = pos1[0]-pos2[0]
        else:              w = pos2[0]-pos1[0]
        if pos1[1]>pos2[1]:h = pos1[1]-pos2[1]
        else:              h = pos2[1]-pos1[1]
        dl = math.sqrt(w*w+h*h)
        return dl
        
    def RAST_CENT(self,rect1 = [],rect2 = []):
        if rect1[4][0]>rect2[4][0]:w = rect1[4][0]-rect2[4][0]
        else:              w = rect2[4][0]-rect1[4][0]
        if rect1[4][1]>rect2[4][1]:h = rect1[4][1]-rect2[4][1]
        else:              h = rect2[4][1]-rect1[4][1]
        dl = math.sqrt(w*w+h*h)
        return dl

    class RandomGR:
                                    def __init__():
                                        pass   
                                    def GET_randint(nume = 1,stn = 1 ,endn = 1):
                                        num = []
                                        for i in range(nume):num.append(random.randint(stn,endn));return num

                                    def GET_random():
                                        num = random.random();return num         
class Collor:
    def __init__(self):
        pass
    class GetCOL:
                                    def GET_CL_RED(collor=[]):return collor[0]

                                    def GET_CL_GRN(collor=[]):return collor[1]

                                    def GET_CL_BLU(collor=[]):return collor[2]

                                    def GET_CL_RGB(collor=[]):
                                        if collor[0]<127 and collor[1]<127 and collor[2]>127:
                                            col = "blue"
                                        elif collor[0]>127 and collor[1]<127 and collor[2]<127:
                                            col = "red"
                                        elif collor[0]<127 and collor[1]>127 and collor[2]<127:
                                            col = "green"
                                        elif collor[0]==0 and collor[1]==0 and collor[2]==0:
                                            col = "black"
                                        elif collor[0]==255 and collor[1]==255 and collor[2]==255:
                                            col = "white"  
                                        return col

    def SET_COL(self,collor=[]):return collor
    
    def COL_BOT(self,collor1=[],collor2=[]):
        collor=[]
        collor.append((collor1[0]+collor2[0])/2);collor.append((collor1[1]+collor2[1])/2);collor.append((collor1[2]+collor2[2])/2)
        return collor
class MOuse:
    def __init__(self):
        pass
    def GET_Pos(self):
        pos = pygame.mouse.get_pos()
        return pos
    def GET_PRESS_s(self,but=""):
        pr = pygame.mouse.get_pressed()
        if but == "l":
            return pr[0]
        elif but == "r":
            return pr[2]
        elif but == "m":
            return pr[1]

    def SET_VIz(self,viz):
        pygame.mouse.set_visible(viz)
    def GET_VIz(self):
        viz = pygame.mouse.get_visible()
        return viz
    def SET_pos(self,pos=[]):
        pygame.mouse.set_pos([pos[0],pos[1]])
class KB0rd:
    def __init__(self):
        pass
    def On_kee_press(self,key=""):
        on = keyboard.is_pressed(key)
        return on
class WinHOW:


    def __init__(self,win_w,win_h):
        global screen,clock
        self.win_w = win_w
        self.win_h = win_h
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        pygame.font.init()
        
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((win_w,win_h))
        
        self.screen = screen
        self.clock = clock



    def get_color(self,x,y):
        col = screen.get_at([x,y])
        col1 = [col[0],col[1],col[2]]
        return col1

    def get_center(self):
        xc = self.win_w/2
        yc = self.win_h/2
        return xc , yc

    def set_fps(self,fps):
        if fps == "MAX":fps = 1000
        if fps == "MIN":fps = 30
        self.clock.tick(fps)

    def get_fps(self):return int(self.clock.get_fps())

    def close(self,running=True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        return running 
    
    def update(self):
        pygame.display.flip()

    
    def BG_col(self,col= (0,0,0)):
        self.screen.fill(col)




    class draw2D:
                                            def __init__(self,):
                                                pass
                                            def drawrect(col=(),pos=[],size=[],sh=0,surf=0):
                                                    rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
                                                    pygame.draw.rect   (surf, 
                                                                            col, 
                                                                            rect,
                                                                            sh)
                                                    center =  [pos[0] + size[0]/2,pos[1]+size[1]/2]
                                                    pos1=[pos[0],pos[1]]
                                                    size1=[size[0],size[1]]
                                                    rectt = [pos1,size1,center,col,sh]
                                                    return rectt

                                            def drawcircle(col=(),pos=[],rad=0,sh=0,surf=0):
                                                    pygame.draw.circle (surf,
                                                                            col,
                                                                            (pos[0],pos[1]),
                                                                            rad,
                                                                            sh)
                                                    center = [pos[0],pos[1]]
                                                    pos1=[pos[0],pos[1]]
                                                    rectt = [pos1,rad,center,col,sh]
                                                    return rectt
                                                            
                                            def drawellips(col=(),pos=[],size=[],sh=0,surf=0):
                                                    rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
                                                    pygame.draw.ellipse(surf,
                                                                            col,
                                                                            rect,
                                                                            sh)
                                                    center =  [pos[0] + size[0]/2,pos[1]+size[1]/2]
                                                    pos1=[pos[0],pos[1]]
                                                    size1=[size[0],size[1]]
                                                    rectt = [pos1,size1,center,col,sh]
                                                    return rectt

                                            def drawtringl(col=(),pos1=[],pos2=[],pos3=[],sh=0,surf=0):
                                                    pygame.draw.polygon(surf,
                                                                            col,
                                                                            [(pos1[0],pos1[1]),(pos2[0],pos2[1]),(pos3[0],pos3[1])],
                                                                            sh)
                                                    rectt = [pos1,pos2,pos3,col,sh]
                                                    return rectt

                                            def drawline(col=(),start_pos=[],end_pos=[],sh=1,surf=0):
                                                    pygame.draw.line(   surf,
                                                                            col,
                                                                            (start_pos[0],start_pos[1]),
                                                                            (end_pos[0],end_pos[1]),
                                                                            sh)
                                                    xcnt = start_pos[0]+(end_pos[0]-start_pos[0])/2;ycnt = start_pos[1]+(end_pos[1]-start_pos[1])/2
                                                    center = [xcnt,ycnt]
                                                    rectt = [start_pos,end_pos,center,col,sh]
                                                    return rectt

                                            def drawliness(col=(),points=(),ZAMKNT=False,sh=1,surf=0):
                                                    pygame.draw.lines(  surf,
                                                                            col,
                                                                            ZAMKNT,
                                                                            points,
                                                                            sh)
                                                    rectt = [points,col,ZAMKNT,sh]
                                                    return rectt

                                            def drawpixel(col=(),pos=[],sh=1,surf=0):
                                                    pygame.draw.line(   surf,
                                                                            col,
                                                                            (pos[0],pos[1]),
                                                                            (pos[0],pos[1]),
                                                                            sh)
                                                    pos=[pos[0],pos[1]]
                                                    rectt = [pos,col,sh]
                                                    return  rectt

                                            def drawarc(col=(),pos=[],size=[],start_angle=0,stop_angle=0,sh=1,surf=0):
                                                    rect= pygame.Rect(pos[0],pos[1],size[0],size[1])
                                                    pygame.draw.arc(    surf,
                                                                        col,
                                                                        rect,
                                                                        start_angle,
                                                                        stop_angle,
                                                                        sh)
                                                    rectt=[pos,size,start_angle,stop_angle,col,sh]
                                                    return rectt
class IMG:
    def __init__(self):
        pass
    def loadIMG(self,file=''):
        imgg = pygame.image.load(file)
        return imgg

    def DrawIMG(self,pos=[],iimmgg=0):
        rect = iimmgg.get_rect(bottomright=(pos[0]+iimmgg.get_width(),
                                            pos[1]+iimmgg.get_height())) 
        screen.blit(iimmgg,rect)
        return rect

    def IMGScale(self,pov,width,height):
        tid = pygame.transform.scale(pov,(width,height))
        return tid
    
    def Save_img(self,pov,file_name=''):
        pygame.image.save(pov,file_name)
class Graphick:
    def __init__(self):
        pass
    def SETcirclGRAPH(self,col=[],znh=[]):
        pit = [col,znh]
        return pit
    def DRcirclGRAPH_2D(self,r=1,xp=1,yp=1,grph=[]):
        kf = 0
        ugl = 1;ugl1=1
        c=r
        g1 = 0
        for g in range(len(grph[0])):
            kf = kf + grph[0][g]

        for g in range(len(grph[1])):
            coll = grph[1][g]
            ugl = ugl1
            for n in range(int(700/kf*grph[0][g1])):
                xl = xp + c * math.sin(ugl)
                yl = yp + c * math.cos(ugl)
                ugl+=0.009
                pygame.draw.line(screen,coll,(xp,yp),(xl,yl),4)
                ugl1 = ugl


            g1 +=1