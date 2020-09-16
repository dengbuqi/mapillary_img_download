import cv2
import glob
import os
# load the image and show it
image = cv2.imread('0000000000.jpg')
foldpath = '/home/data/mapillary_data/'
outputpath ='/home/data/mapillary_data_croped/'

cropheight = 320

for fold in glob.glob(foldpath+'/*'):
    outfold = fold.split('/')[-1]
    if not os.path.isdir(outputpath+outfold):
        os.mkdir(outputpath+outfold)
    print('cropping:', outfold,'......')
    for path in glob.glob(fold+'/*'):
        imgname = path.split('/')[-1]
        outimg = outputpath+outfold+'/'+imgname
        if not os.path.isfile(outimg):
            # print(imgname)
            img = cv2.imread(path)
            cv2.imwrite(outimg,img[0:image.shape[0]-cropheight])
    print(outfold,'croped!!!!!!')