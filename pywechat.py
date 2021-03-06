# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:19:20 2017

@author: hfutzf
"""
from PIL import Image
import itchat
import win32com.client 
import cv2,os
import win32api,time
from arduino import Arduino 
from PIL import ImageGrab


voice= win32com.client.Dispatch("SAPI.SpVoice")
itchat.login()

face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')

try:
    b = Arduino('COM8')
    pin = 13

    b.output([pin]) 
except:
    pass

itchat.send('python——微信宿舍监控系统\n1.输入照片:发送宿舍实时图像信息。\n2.输入视频:发送宿\
舍实时视频监控信息\n3.发送#+文件（或者程序），远程打开文件\n4.输入开灯，则arduino上的13号led\
灯点亮\n5.输入关灯，则arduino上的13号led灯熄灭\
\n6.发送除上述情况以外的文本，远程实时文本转语音\
输出\n7.输入开始监控，电脑开启摄像头开始监控，若识别出人脸，则通过微信向您报警，并保留图片和视频\
\n8.输入结束监控，则结束监控',toUserName='filehelper')

@itchat.msg_register('Text') #注册文本消息
def text_reply(msg):
    global flag
    message =  msg['Text'] 
    toName = msg['ToUserName'] 
    insert=['照片','视频','开灯','关灯','#','开始监控','结束监控']
    if toName == "filehelper":
        if message == "照片": #远程拍照并发送到手机
        
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.mp4',fourcc, 5.0, (640,480))
            
            start_time=time.clock()
            while(cap.isOpened() and (time.clock()-start_time)<3):
                ret, frame = cap.read()
                if ret==True:
                    frame = cv2.flip(frame,0)
                    out.write(frame)
                    
                    # 释放内存
            cap.release()
            out.release()
            
            vc = cv2.VideoCapture('output.mp4') #读入视频文件  
            c=1  
  
            if vc.isOpened(): #判断是否正常打开  
                rval , frame = vc.read()  
            else:  
                rval = False  
  
            timeF = 4  #视频帧计数间隔频率  
  
            while rval:   #循环读取视频帧  
                rval, frame = vc.read()  
                if(c%timeF == 0): #每隔timeF帧进行存储操作  
                      cv2.imwrite('image'+str(4) + '.jpg',frame) #存储为图像  
                c = c + 1  
                cv2.waitKey(1)  
            vc.release()  
            
            im1 = Image.open("image4.jpg")
            im2 = im1.rotate(180)
            im2.save('image.jpg')
            itchat.send('@img@%s'%u'image.jpg',toUserName='filehelper')
        if not((message in insert) or  message[0]=='#'):
            voice.Speak(message)
            itchat.send('[文本已成功转为语音读出]',toUserName='filehelper')
        if message[0]=='#':
            if os.path.exists(message[1:]):
                try:
                    win32api.ShellExecute(0,'open', message[1:], '','',1)
                    time.sleep(3)
                    im = ImageGrab.grab()
                    im.save('cut.jpg')
                    itchat.send(message[1:]+'已经成功打开',toUserName='filehelper')
                    itchat.send('屏幕截图如下所示',toUserName='filehelper')
                    itchat.send('@img@%s'%u'cut.jpg',toUserName='filehelper')
                except:
                    pass
            else:
                itchat.send('打开文件失败',toUserName='filehelper')
        if message == "视频":
          try:
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.mp4',fourcc, 5.0, (640,480))
            
            start_time=time.clock()
            while(cap.isOpened() and (time.clock()-start_time)<10):
                ret, frame = cap.read()
                if ret==True:
                    frame = cv2.flip(frame,0)
                    out.write(frame)
                    
                    # 释放内存
            cap.release()
            out.release()
            itchat.send('@vid@%s'%u'output.mp4',toUserName='filehelper') 
          except:
              itchat.send('获取视频失败',toUserName='filehelper') 
        if message == "开灯":
            try:
                b.setHigh(pin)
                itchat.send('开灯成功！(:',toUserName='filehelper')
            except:
                itchat.send('开灯失败):',toUserName='filehelper') 
        if message == "关灯":
            try:
                b.setLow(pin)
                itchat.send('关灯成功 ):',toUserName='filehelper')
            except:
                itchat.send('关灯失败 ):',toUserName='filehelper') 
        if message == "开始监控":
          global number
          number=0
          while number<4 :
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.mp4',fourcc, 5.0, (640,480))
            
            start_time=time.clock()
            while(cap.isOpened() and (time.clock()-start_time)<3):
                ret, frame = cap.read()
                if ret==True:
                    frame = cv2.flip(frame,0)
                    out.write(frame)
                    
                    # 释放内存
            cap.release()
            out.release()
            
            vc = cv2.VideoCapture('output.mp4') #读入视频文件  
            c=1  
  
            if vc.isOpened(): #判断是否正常打开  
                rval , frame = vc.read()  
            else:  
                rval = False  
  
            timeF = 2  #视频帧计数间隔频率  
  
            while rval:   #循环读取视频帧  
                rval, frame = vc.read()  
                if(c%timeF == 0): #每隔timeF帧进行存储操作  
                      cv2.imwrite('image'+str(2) + '.jpg',frame) #存储为图像  
                c = c + 1  
                cv2.waitKey(1)  
            vc.release()  
            
            im1 = Image.open("image2.jpg")
            im2 = im1.rotate(180)
            im2.save('image.jpg')
            
            image = cv2.imread('image.jpg')
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            # 探测图片中的人脸
            faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.15,
            minNeighbors = 10,
            minSize = (10,10),
            flags = cv2.IMREAD_GRAYSCALE
                      )
            
            if len(faces)>=1:
                number+=1
                for(x,y,w,h) in faces:
                    cv2.rectangle(image,(x,y),(x+w,y+w),(0,255,0),2)
                itchat.send('有人在你的书桌附近活动',toUserName='filehelper')
                itchat.send('@vid@%s'%u'output.mp4',toUserName='filehelper') 
                itchat.send('@img@%s'%u'image.jpg',toUserName='filehelper')
                voice.Speak('您已经进入视频监控区，请约束好自己的行为！')
        
itchat.run()






