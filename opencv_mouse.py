# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:59:32 2017

@author: leon
"""

import cv2
import numpy as np
import wx
import sys

SAVE_FLAG = False
LBUTTONDOWN_FLAG = False
LBUTTONUP_FLAG = False
MOUSEMOVE_FLAG = False
xy1 = [0, 0]
xy2 = [0, 0]


def mouse_event(event, x, y, flags, param):
    global LBUTTONDOWN_FLAG, LBUTTONUP_FLAG, MOUSEMOVE_FLAG, xy1, xy2
    CompositeImg = img.copy()
    
    if event == cv2.EVENT_LBUTTONDOWN:
        LBUTTONDOWN_FLAG = True
        xy1 = x, y 
    
    if event == cv2.EVENT_MOUSEMOVE:
        if LBUTTONDOWN_FLAG == True  and LBUTTONUP_FLAG == False:
            MOUSEMOVE_FLAG = True
            xy2 = x, y
            cv2.rectangle(CompositeImg, (xy1[0], xy1[1]), (xy2[0], xy2[1]), (0, 255, 0), 2)
            cv2.imshow('title', CompositeImg)

               
    if event == cv2.EVENT_LBUTTONUP:
        if LBUTTONDOWN_FLAG == True and MOUSEMOVE_FLAG == True:
            LBUTTONUP_FLAG = True #クリックした後，離すとフラグが立つ
            saveTF()
        elif MOUSEMOVE_FLAG == False:
            LBUTTONDOWN_FLAG = False    

def saveTF():
    global LBUTTONDOWN_FLAG, LBUTTONUP_FLAG, MOUSEMOVE_FLAG
    app = wx.App()
    dialog = wx.MessageBox(u'画像を保存しますか', u'ユーザーメッセージ', wx.YES_NO | wx.NO_DEFAULT)# メッセージボックスを表示

    if dialog == 2:
        global SAVE_FLAG
        SAVE_FLAG = True
    elif dialog == 8:
        cv2.imshow('title',img)
        LBUTTONDOWN_FLAG = False
        LBUTTONUP_FLAG = False
        MOUSEMOVE_FLAG = False
    
    app = None
        

def Adjust(xy1, xy2):
    _xy1 = np.array(xy1)
    _xy2 = np.array(xy2)
    if xy1[0] < 0:
        _xy1[0] = 0
    elif xy1[0] > img.shape[0]:
        _xy1[0] = img.shape[0]  
        
    if xy2[0] < 0:
        _xy2[0] = 0
    elif xy2[0] > img.shape[0]:
        _xy2[0] = img.shape[0]
        
    
    if xy1[1] < 0:
        _xy1[1] = 0
    elif xy1[1] > img.shape[1]:
        _xy1[1] = img.shape[1]  
        
    if xy2[1] < 0:
        _xy2[1] = 0
    elif xy2[1] > img.shape[1]:
        _xy2[1] = img.shape[1]
        
    return _xy1, _xy2


def Trimming(img, _xy1, _xy2):
    if _xy1[0] < _xy2[0]:
        x_start = _xy1[0]
    else:
        x_start = _xy2[0]
         
    if _xy1[1] < _xy2[1]:
        y_start = _xy1[1]
    else:
        y_start = _xy2[1]
         
    dst = img[ y_start : y_start + abs(_xy1[1] - _xy2[1]), x_start : x_start + abs(_xy1[0] - _xy2[0]) ]
    
    return dst   

         
if __name__ == '__main__':
    img = cv2.imread('lena.jpg')
    if img is None:
         app = wx.App()
         dialog = wx.MessageBox(u'画像が読み込めません', u'ユーザーメッセージ')
         app = None
         sys.exit(0)
         
    cv2.namedWindow('title')
    cv2.imshow('title', img)
    cv2.setMouseCallback('title', mouse_event)
            
    while(True):
        if cv2.waitKey(1) == 'q' or SAVE_FLAG == True:
            break      

    _xy1, _xy2 = Adjust(xy1, xy2) #枠がウィンドウを越えた場合に調整する
    dst = Trimming(img, _xy1, _xy2)
    #cv2.imshow('result', dst)
    cv2.imwrite('dst.jpg', dst)  
    cv2.destroyAllWindows()

