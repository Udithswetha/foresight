import subprocess
import cv2
import os
import time
import imutils
import urllib
import numpy as np

url="http://192.168.43.71:8080/shot.jpg"

f=open('data.txt','w')
f.write('')
f.close()
while True:
    
    imgPath=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgPath.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img=imutils.resize(img,width=400)
    cv2.imshow("frame",img)
    
    key=cv2.waitKey(1) & 0xFF
    if (key== ord('q')):
        print"capture"
        cv2.imwrite("input.jpg",img)
        time.sleep(5)
        X=subprocess.Popen("sudo tesseract input.jpg data",shell=True)#.communicate
        time.sleep(10)
        print X
        while X is None:
            pass
        f=open('data.txt','r')
        s=f.read()
        f.close()
#        subprocess.call(['sudo','espeak',s])
#        X=0
        subprocess.call('sudo festival --tts data.txt', shell=True)
        X=0
#        s=''
        
        

cv2.destroyAllWindows()
