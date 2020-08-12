import numpy as np
import cv2, os
import glob


class TingTing():
    
    def __init__(self):
        
        self.img = self.Image_Load()
    

    def Image_Load(self):

        static = [ "Normal.png", "Sad.png", "Love.png", "Sleep.png"]
        path = os.path.join("_image")

        img = []
        for s in static:
            im = cv2.imread(os.path.join(path, s))
            im = cv2.resize(im, (1280,720))
            img.append(im)
            
        return img

    def Set_Static(self, Now):
        return self.img[Now]

    def Make_Face(self, Static = 0):
        face = np.zeros((720,1280,3), dtype=np.uint8)
        img =self.Set_Static(Static)
        face[:, :] = img

        return face


        