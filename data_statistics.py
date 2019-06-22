# 2019.06.20
# zmy
import numpy as np
import cv2
import os
import glob
from shapely.geometry import Polygon
from pyecharts import Bar, Pie



def data_statistic():
    label_path = 'D:/everyproject/dataset/train/labelTxt/'
    txt_list = os.listdir(label_path)
    category_list = []
    type_list = []
    source_list = []
    print(len(txt_list))
    # print(txt_list)
    # 按文件名遍历txt文件
    for txt in txt_list:
        info_list = []
        one_info_list = []
        txt_path = label_path + txt
        # print(txt_path)
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

        # 计算每张图像中有多少实例数
        # print(txt+':'+str(len(info_list)))
        str3 = txt.split('.')[0]+':'+str(len(info_list)-2)
        with open('D:/everyproject/dataset/data_analyse/instances_per_img.txt', "a", encoding="UTF-8") as target:
            target.write(str3 + '\n')


        # 计算数据来源
        source_list.append(info_list[0])

        for i in range(2, len(info_list)):
            str1 = info_list[i]
            informations = str1.split(' ')
            # 单一txt
            one_info_list.append(informations[-2])
            # 所有txt
            category_list.append(informations[-2])
            type_list.append(informations[-1])

        # 计算每张图像中的种类数
        one_number = len(set(one_info_list))
        new_line1 = txt.split('.')[0] + ':' + str(one_number)
        with open('D:/everyproject/dataset/data_analyse/categories_per_img.txt', "a", encoding="UTF-8") as target:
            target.write(new_line1 + '\n')
    # print(len(category_list))
    # print(len(type_list))

    # 计算数据来源
    for s in set(source_list):
        str5 = s + ':' + str(source_list.count(s))
        with open('D:/everyproject/dataset/data_analyse/source.txt', "a", encoding="UTF-8") as target:
            target.write(str5 + '\n')

    # 计算0-1实例数
    for r in set(type_list):
        str4 = r+':'+str(type_list.count(r))
        with open('D:/everyproject/dataset/data_analyse/0_1_instances.txt', "a", encoding="UTF-8") as target:
            target.write(str4 + '\n')


    # 计算所有种类数量
    for i in set(category_list):
        # number_dict[i] = category_list.count(i)
        str2 = i+':'+str(category_list.count(i))
        with open('D:/everyproject/dataset/data_analyse/instances_per_category.txt', "a", encoding="UTF-8") as target:
            target.write(str2 + '\n')


def category_percentage():
    txt_path = 'D:/everyproject/dataset/data_analyse/categories_per_img.txt'
    info_list = []
    quantity_list = []
    f = open(txt_path, 'r', encoding='utf-8')
    try:
        for line in f.readlines():
            info_list.append(str(line).strip('\n'))
    finally:
        f.close()

    print(info_list)
    print(len(info_list))

    for info in info_list:
        quantity_list.append(info.split(':')[1])
    print(len(quantity_list))
    for q in set(quantity_list):
        str1 = q + ':' + str(quantity_list.count(q))
        with open('D:/everyproject/dataset/data_analyse/category_percentage.txt', "a", encoding="UTF-8") as target:
            target.write(str1 + '\n')


def instance_percentage():
    txt_path = 'D:/everyproject/dataset/data_analyse/instances_per_img.txt'
    info_list = []
    quantity_list = []
    f = open(txt_path, 'r', encoding='utf-8')
    try:
        for line in f.readlines():
            info_list.append(str(line).strip('\n'))
    finally:
        f.close()

    print(info_list)
    print(len(info_list))

    for info in info_list:
        quantity_list.append(int(info.split(':')[1]))
    print(len(quantity_list))
    sum = 0
    # for i in quantity_list:
    #     sum += i
    # print(sum)
    for q in set(quantity_list):
        sum += quantity_list.count(q)
        str1 = str(q) + ':' + str(quantity_list.count(q))
        with open('D:/everyproject/dataset/data_analyse/instance_percentage.txt', "a", encoding="UTF-8") as target:
            target.write(str1 + '\n')
    print(sum)

def calcu_area(txt_path):
    src_img = 'D:/everyproject/dataset/train/images/'
    img_name = txt_path.split('/')[-1].split('.')[0]

    # 计算对应图片面积
    img = cv2.imread(src_img+img_name+'.png', cv2.IMREAD_ANYCOLOR)
    img_shape = list(img.shape)
    print(str(img_name)+':'+str(img_shape))
    img_area = img_shape[0]*img_shape[1]
    str1 = img_name + ':' + str(img_shape[0]) + ':' + str(img_shape[1]) + ':' + str(img_area)
    with open('D:/everyproject/dataset/data_analyse/img_area/' + img_name + '_area.txt', "a", encoding="UTF-8") as target:
        target.write(str1 + '\n')

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

    # 计算每个目标面积
    for i in range(2, len(info_list)):
        one_list = info_list[i].split(' ')
        # print(len(one_list))
        line1 = []
        for m in range(0, 8):
            line1.append(float(one_list[m]))
        # print(line1)
        a = np.array(line1).reshape(4, 2)
        poly1 = Polygon(a).convex_hull
        obj_area = poly1.area
        # print(poly1)
        str2 = img_name+':'+str(obj_area)+':'+str(obj_area/img_area)
        # print(str2)
        with open('D:/everyproject/dataset/data_analyse/img_area/'+img_name+'_area.txt', "a", encoding="UTF-8") as target:
            target.write(str2 + '\n')

def bianli_txt():
    label_path = 'D:/everyproject/dataset/train/labelTxt/'
    txt_list = os.listdir(label_path)
    print(len(txt_list))
    # print(txt_list)
    # 按文件名遍历txt文件
    for txt in txt_list:
        calcu_area(txt_path=label_path + txt)

# 以下为绘图函数
def draw_instance_per_category():
    txt_path = 'D:/everyproject/dataset/data_analyse/instances_per_category.txt'
    info_list = []
    category_list = []
    quantitly_list = []
    f = open(txt_path, 'r', encoding='utf-8')
    try:
        for line in f.readlines():
            info_list.append(str(line).strip('\n'))
    finally:
        f.close()

    print(info_list)
    print(len(info_list))

    for info in info_list:
        category_list.append(info.split(':')[0])
        quantitly_list.append(int(info.split(':')[1]))
    print(category_list)
    print(quantitly_list)

    # bar = Bar("种类数量", "", )
    # bar.add("数量", category_list, quantitly_list, is_xaxislabel_align=True, xaxis_interval=0)
    # bar.render()

    pie = Pie('', height=1000, width=1500, title_top='bottom')
    pie.add('', category_list, quantitly_list, is_label_show=True)
    pie.render('D:/everyproject/dataset/data_analyse/charts/instances_per_category.html')

def draw_categories_percentage():
    txt_path = 'D:/everyproject/dataset/data_analyse/category_percentage.txt'
    info_list = []
    category_quantity_list = []
    img_quantitly_list = []
    f = open(txt_path, 'r', encoding='utf-8')
    try:
        for line in f.readlines():
            info_list.append(str(line).strip('\n'))
    finally:
        f.close()

    print(info_list)
    print(len(info_list))

    for info in info_list:
        category_quantity_list.append(info.split(':')[0])
        img_quantitly_list.append(int(info.split(':')[1]))
    print(category_quantity_list)
    print(img_quantitly_list)

    # bar = Bar("种类数量", "", )
    # bar.add("数量", category_list, quantitly_list, is_xaxislabel_align=True, xaxis_interval=0)
    # bar.render()

    pie = Pie('', height=1000, width=1500, title_top='bottom')
    pie.add('', category_quantity_list, img_quantitly_list, is_label_show=True)
    pie.render('D:/everyproject/dataset/data_analyse/charts/category_percentage.html')

def draw_instances_percentage():
    txt_path = 'D:/everyproject/dataset/data_analyse/instance_percentage.txt'
    info_list = []
    instance_quantity_list = []
    img_quantitly_list = []
    f = open(txt_path, 'r', encoding='utf-8')
    try:
        for line in f.readlines():
            info_list.append(str(line).strip('\n'))
    finally:
        f.close()

    # print(info_list)
    # print(len(info_list))
    mult_list = [0,0,0,0,0,0,0,0,0]
    for info in info_list:
        instance_quantity_list.append(int(info.split(':')[0]))
        img_quantitly_list.append(int(info.split(':')[1]))
    print(len(instance_quantity_list))
    print(len(img_quantitly_list))

    for m in range(0, len(instance_quantity_list)):
        if instance_quantity_list[m]>=0 and instance_quantity_list[m]<10:
            mult_list[0] = mult_list[0]+img_quantitly_list[m]
        elif instance_quantity_list[m]>=10 and instance_quantity_list[m]<30:
            mult_list[1] = mult_list[1] + img_quantitly_list[m]
        elif instance_quantity_list[m]>=30 and instance_quantity_list[m]<50:
            mult_list[2] = mult_list[2] + img_quantitly_list[m]
        elif instance_quantity_list[m]>=50 and instance_quantity_list[m]<100:
            mult_list[3] = mult_list[3] + img_quantitly_list[m]
        elif instance_quantity_list[m]>=100 and instance_quantity_list[m]<200:
            mult_list[4] = mult_list[4] + img_quantitly_list[m]
        elif instance_quantity_list[m]>=200 and instance_quantity_list[m]<500:
            mult_list[5] = mult_list[5] + img_quantitly_list[m]
        elif instance_quantity_list[m]>=500 and instance_quantity_list[m]<1000:
            mult_list[6] = mult_list[6] + img_quantitly_list[m]
        elif instance_quantity_list[m]>=1000 and instance_quantity_list[m]<2000:
            mult_list[7] = mult_list[7] + img_quantitly_list[m]
        else:
            mult_list[8] = mult_list[8] + img_quantitly_list[m]
    print(mult_list)




    # bar = Bar("种类数量", "", )
    # bar.add("数量", category_list, quantitly_list, is_xaxislabel_align=True, xaxis_interval=0)
    # bar.render()
    range_list = ['0-10', '10-30', '30-50', '50-100', '100-200', '200-500', '500-1000', '1000-2000', '2000+']
    pie = Pie('', height=1000, width=1500, title_top='bottom')
    pie.add('', range_list, mult_list, is_label_show=True)
    pie.render('D:/everyproject/dataset/data_analyse/charts/instance_percentage.html')

def draw_data_source():
    txt_path = 'D:/everyproject/dataset/data_analyse/source.txt'
    info_list = []
    source_list = []
    img_quantitly_list = []
    f = open(txt_path, 'r', encoding='utf-8')
    try:
        for line in f.readlines():
            info_list.append(str(line).strip('\n'))
    finally:
        f.close()

    for info in info_list:
        source_list.append(info.split(':')[1])
        img_quantitly_list.append(int(info.split(':')[2]))
    print(source_list)
    print(img_quantitly_list)

    pie = Pie('', height=1000, width=1500, title_top='bottom')
    pie.add('', source_list, img_quantitly_list, is_label_show=True)
    pie.render('D:/everyproject/dataset/data_analyse/charts/data_source.html')

def draw_img_area_percentage():
    txt_path = 'D:/everyproject/dataset/data_analyse/img_area/'
    path_list = glob.glob(txt_path+'*_area.txt')
    print(len(path_list))
    print(path_list)
    img_list = []
    max_object = 0
    min_object = 0
    # 对目标区域面积划分为六个范围
    mult_list = [0,0,0,0,0,0,0]
    # 对图像面积划分为四个范围
    img_mult_list = [0,0,0,0]


    # 读取每个txt文件
    for i in path_list:
        # print(i)
        info_list = []
        f = open(i, 'r', encoding='utf-8')
        try:
            for line in f.readlines():
                info_list.append(str(line).strip('\n'))
        finally:
            f.close()
        img_list.append(int(info_list[0].split(':')[-1]))
        if len(info_list)>1:
            for i in range(1, len(info_list)):
                number = float(info_list[i].split(':')[-1])
                if number>=0 and number<1e-6:
                    mult_list[0] += 1
                elif number>=1e-6 and number<1e-5:
                    mult_list[1] += 1
                elif number>=1e-5 and number<1e-4:
                    mult_list[2] += 1
                elif number>=1e-4 and number<1e-3:
                    mult_list[3] += 1
                elif number>=1e-3 and number<1e-2:
                    mult_list[4] += 1
                elif number>=1e-2 and number<0.1:
                    mult_list[5] += 1
                else:
                    mult_list[6] += 1
        else:
            print(i)
    print(max(img_list))
    print(min(img_list))
    print(max_object)
    print(min_object)
    print(mult_list)

    range_list = ['[0,1e-6]', '[1e-6,1e-5]', '[1e-5,1e-4]', '[1e-4,1e-3]', '[1e-3,1e-2]', '[1e-2,1e-1]', '[o.1,1]']
    pie = Pie('', height=1000, width=1500, title_top='bottom')
    pie.add('', range_list, mult_list, is_label_show=True)
    pie.render('D:/everyproject/dataset/data_analyse/charts/object_area_percentage.html')

    for m in img_list:
        if m>=1.4e+5 and m<1.4e+6:
            img_mult_list[0] += 1
        elif m>=1.4e+6 and m<1.4e+7:
            img_mult_list[1] += 1
        elif m>=1.4e+7 and m<1.4e+8:
            img_mult_list[2] += 1
        else:
            img_mult_list[3] += 1
    print(img_mult_list)
    range2_list = ['[1.4e+5,1.4e+6]', '[1.4e+6,1.4e+7]', '[1.4e+7,1.4e+8]', '[1.4e+8,8e+8]']
    pie = Pie('', height=1000, width=1500, title_top='bottom')
    pie.add('', range2_list, img_mult_list, is_label_show=True)
    pie.render('D:/everyproject/dataset/data_analyse/charts/img_area_percentage.html')



if __name__ == '__main__':
    print("Hello, boy!")
    # data_statistic()
    # category_percentage()
    # instance_percentage()
    # bianli_txt()
    # draw_instance_per_category()
    # draw_categories_percentage()
    # draw_instances_percentage()
    # draw_data_source()
    draw_img_area_percentage()