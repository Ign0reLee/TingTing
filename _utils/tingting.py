import numpy as np
import cv2, os
import glob


class TingTing():
    
    def __init__(self):

        self.Window_W = 1680
        self.Window_H = 960
        
        self.img = self.Image_Load()
        self.ymin, self.ymax, self.xmin, self.xmax = self.Compute_Center(300,1100, self.Window_H, self.Window_W )
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

    def Make_Face(self, Static = 2, move=False):
        face = np.zeros((self.Window_H,self.Window_W ,3), dtype=np.uint8)
        img =self.Set_Static(Static)

        if not move:
            ymin, ymax = self.waggles(self.ymin, self.ymax)
            self.check_waggle(ymin)
            face[ymin:ymax, self.xmin:self.xmax] = img

        else:
            face[self.ymin:self.ymax, self.xmin:self.xmax] = img

        return face


        