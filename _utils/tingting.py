import numpy as np
import math
import cv2, os
import glob


class TingTing():
    
    def __init__(self):

        self.Window_W = 1680
        self.Window_H = 960
        self.Image_W = 1100
        self.Image_H = 300
        self.Camera_X = 400
        self.Camera_Y = 225
        
        self.img = self.Image_Load()
        self.ymin, self.ymax, self.xmin, self.xmax = self.Compute_Center(self.Image_H, self.Image_W, self.Window_H, self.Window_W )
        self.centerX = int((self.xmin + self.xmax)/2)
        self.centerY = int((self.ymin + self.ymax)/2)
        self.waggle = 1
        self.waggle_sate = 1
    

    def Image_Load(self):

        static = [ "Normal.png", "Sad.png", "Love.png", "Sleep.png"]
        path = os.path.join("_image")

        img = []
        for s in static:
            im = cv2.imread(os.path.join(path, s))
            img.append(im)
            
        return img

    def moving(self, objx, objy):

        space = 10
        moveX = (objx - self.centerX ) / 10
        moveY = (self.centerY - objy) / 10

        if moveX >0: 
            moveX = math.ceil(moveX)
        else: 
            moveX = math.floor(moveX)
        if moveY >0: 
            moveY = math.ceil(moveY)
        else: 
            moveY = math.floor(moveY)


        print("Object X : ",objx)
        print("Object Y : ", objy)
        print("Center X : ", self.centerX)
        print("Center Y : ", self.centerY)
        print("Moving X : ",moveX)
        print("Moving Y : ",moveY)
 
        
        self.ymin -= moveY
        self.ymax -= moveY
        self.xmin += moveX
        self.xmax += moveX

        if self.xmin < 0:
            self.xmin =0
            self.xmax = self.Image_W

        if self.xmax > self.Window_W:
            self.xmax = self.Window_W
            self.xmin = self.Window_W - self.Image_W

        if self.ymin <space:
            self.ymin = space
            self.ymax = self.Image_H +space

        if self.ymax > self.Window_H-space:
            self.ymax = self.Window_H -space
            self.ymin = self.Window_H - self.Image_H-space

        self.centerX = int((self.xmin + self.xmax)/2)
        self.centerY = int((self.ymin + self.ymax)/2)
        
    def make_object(self, objx, objy):

        objy = int((objy / self.Camera_Y) * self.Window_H)
        objx = int((objx / self.Camera_X) * self.Window_W)

        return objx, objy
        
    def Compute_Center(self, h,w, fh, fw):
        
        cy = int(fh/2)
        cx = int(fw/2)

        ymin = cy - int(h/2)
        ymax = cy + int(h/2)
        xmin = cx - int(w/2)
        xmax = cx + int(w/2)
        return ymin, ymax, xmin, xmax
    
    def waggles(self, ymin, ymax ):

        self.waggle_sate += self.waggle
        ymin += self.waggle_sate
        ymax += self.waggle_sate

        return ymin, ymax

    def check_waggle(self, ymin):

        if (self.ymin - 10) < ymin:
            self.waggle *=-1

        if ( self.ymin + 10) > ymin:
            self.waggle *=-1

    def Set_Static(self, Now):
        return self.img[Now]

    def Make_Face(self, Static = 2, move=False , objx = 0, objy = 0):
        face = np.zeros((self.Window_H,self.Window_W ,3), dtype=np.uint8)
        img =self.Set_Static(Static)

        if not move:
            ymin, ymax = self.waggles(self.ymin, self.ymax)
            self.check_waggle(ymin)
            face[ymin:ymax, self.xmin:self.xmax] = img

        else:
            nobjx, nobjy = self.make_object(objx, objy)
            self.moving(nobjx, nobjy)
            face[self.ymin:self.ymax, self.xmin:self.xmax] = img

        return face


        