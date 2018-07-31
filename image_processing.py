from os import listdir, mkdir
from os.path import isfile, join
from shutil import copyfile
import cv2
import numpy as np
import matplotlib.pyplot as plt

def square_crop(image):
    height = image.shape[0]
    width = image.shape[1]

    if height < width:
        cropped = image[:, :height]
    else:
        cropped = image[:width, :]
    return cropped.shape

def resize_img(img_root, target_root, new_size, border_size, border_color):
    files = [f for f in listdir(img_root) if isfile(join(img_root, f))]

    for file in files:
        img = cv2.imread('{}{}'.format(img_root, file))

        #resize to square and smaller size
        dims = square_crop(img)
        img = cv2.resize(img, (dims[:2]))
        img = cv2.resize(img, new_size)

        #border
        #img = cv2.copyMakeBorder(img, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=border_color)

        #color channel
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #or HSV

        cv2.imwrite('{}/{}'.format(target_root, file), img)


def train_test_split(target_root, split=.20):
    files = np.array([f for f in listdir(target_root) if isfile(join(target_root, f))])

    train_path = target_root + 'train/'
    test_path = target_root + 'test/'
    valid_path = target_root + 'valid/'
    mkdir(train_path)
    mkdir(test_path)
    mkdir(valid_path)

    test_files = np.random.choice(files, int(split*len(files)))
    for file in test_files:
        copyfile(target_root + file, test_path + file)
    train_files = files[~np.in1d(files, test_files)]
    for file in train_files:
        copyfile(target_root + file, train_path + file)

if __name__ == '__main__':
    img_root = 'test_images/'
    target_root = 'thumbnails/'

    train_test_split(target_root)
    resize_img(img_root, target_root, new_size=(98, 98), border_size=20, border_color=[0,0,0])
