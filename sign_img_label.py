import numpy as np
import cv2
import os
from shapely.geometry import Polygon


def draw_object(txt_path, save_path):
    src_img = txt_path.replace('labelTxt', 'images').replace('txt', 'png')
    img_name = txt_path.split('/')[-1].split('.')[0]

    img = cv2.imread(src_img, cv2.IMREAD_ANYCOLOR)

    # 读取文件所有信息
    info_list = []
    f = open(txt_path, 'r', encoding='utf-8')
    try:
        for line in f.readlines():
            if line == '\n':
                continue
            info_list.append(str(line).strip('\n'))
    finally:
        f.close()
    # print(len(info_list))
    # print(info_list)
    draw_list = []

    # 得到所有框的坐标集
    for i in range(2, len(info_list)):
        one_list = info_list[i].split(' ')
        # print(len(one_list))
        line1 = []
        for m in range(0, 8):
            line1.append(float(one_list[m]))
        # print(line1)
        a = np.array(line1).reshape(4, 2)
        b = np.array(a, dtype=np.int32)
        draw_list.append(b)

    # 实心框
    # cv2.fillPoly(img, draw_list, (255, 0, 0))
    # 空心框
    cv2.polylines(img, draw_list, True, (255, 0, 0), thickness=2)

    # cv2.imshow('img', img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    cv2.imwrite(save_path+img_name+'.png', img)
    print(img_name, 'is ok!')

def bianli_txt():
    label_path = 'D:/everyproject/dataset/data_analyse/test_draw_label/train/labelTxt/'
    label2_path = 'D:/everyproject/dataset/data_analyse/test_draw_label/val/labelTxt/'
    save1_path = 'D:/everyproject/dataset/data_analyse/test_draw_label/sign_img/train/'
    save2_path = 'D:/everyproject/dataset/data_analyse/test_draw_label/sign_img/val/'
    # txt_list = os.listdir(label_path)
    # print(len(txt_list))
    # # print(txt_list)
    # # 按文件名遍历txt文件
    # for txt in txt_list:
    #     draw_object(txt_path=label_path + txt, save_path=save1_path)


    txt2_list = os.listdir(label2_path)
    print(len(txt2_list))
    # print(txt_list)
    # 按文件名遍历txt文件
    for txt2 in txt2_list:
        draw_object(txt_path=label2_path + txt2, save_path=save2_path)


if __name__ == '__main__':
    print('Hello')

    bianli_txt()
