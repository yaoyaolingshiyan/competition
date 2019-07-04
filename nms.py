import numpy as np
import cv2
import aeast.config as config
from shapely.geometry import Polygon


# TODO 可能要注意坐标轴问题
def theta_length_width_to_quad(x, y, theta, length, width):
    """
    把 计算出来的值 还原为四点坐标
    :param x:向右
    :param y:向下
    :param theta:
    :param length:
    :param width:
    :return:
    """
    # 先把这三个归一化的指标还原
    img_width = config.img_width
    # 因为process的原因，长度是一定大于宽度的
    length = length * img_width
    width = width * img_width
    angle = theta * 180  # preprocess的时候做了归一化
    if angle >= 90:
        width, length = length, width
        angle = -(angle - 90)
    else:
        angle = - angle
    rect = ((x, y), (width, length), angle)
    box = cv2.boxPoints(rect)
    return box


def intersection(g_quad, p_quad):
    # 创建带比较的两个点的多边形
    g_poly = Polygon(g_quad).convex_hull
    p_ploy = Polygon(p_quad).convex_hull
    inter = g_poly.intersection(p_ploy).area
    union = g_poly.area + g_poly.area - inter
    if union == 0:
        return 0
    else:
        return inter / union  # 交并比


def nms(predict, confidence_threshold=0.4, iou_threshold=0.3):
    """
    对 一张图 进行 nms
    :param predict:  经过sigmoid之后的数
    :param confidence_threshold:
    :param iou_threshold:
    :return:
    """
    # 因为batch size 为1，所以要先reshape一下， （1024，1024，22）
    predict = predict.reshape([predict.shape[1], predict.shape[2], predict.shape[3]])
    y, x = np.where(predict[:, :, 0] > confidence_threshold)
    # print(type(y))
    # print(len(x))
    y_x_coord = np.concatenate([y.reshape([-1, 1]), x.reshape([-1, 1])], axis=-1)
    print('y_x_coord.shape: ', y_x_coord.shape)
    y_x_map = np.zeros([predict.shape[0], predict.shape[1], 2])
    # 对应（y,x）点存储了合格的score——map点坐标
    y_x_map[y, x] = y_x_coord
    # print(y_x_map)
    # print(y_x_map.shape)

    filter_predict = predict[y, x, :]
    print('filter_predict.shape: ', filter_predict.shape)

    score_list = filter_predict[:, 0]
    theta_length_width_list = filter_predict[:, 1:4]
    class_18_list = filter_predict[:, 5:]
    # print(score_list)
    print('theta_length_width_list: ', theta_length_width_list.shape)
    print('class_18_list.shape: ', class_18_list.shape)

    quad_list = []
    # ##表示有多少个合格的score_map（y,x）点
    for i in range(len(filter_predict)):
        # TODO x,y坐标这里要注意一下
        quad = theta_length_width_to_quad(x[i], y[i], theta_length_width_list[i, 0], theta_length_width_list[i, 1],
                                          theta_length_width_list[i, 2])
        quad = np.array(quad, dtype=np.int32)
        quad_list.append(quad)
    quad_list = np.array(quad_list)

    print('NSM前，目标框数目：', len(quad_list))

    img = np.zeros((1024, 1024), dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(img, quad_list, True, (255, 0, 0), thickness=2)
    cv2.imshow('img', img)
    cv2.waitKey()
    # cv2.destroyAllWindows()

    # 得到由大到小的score下标序列
    order = np.argsort(score_list)[::-1]
    # print(type(order))
    # print(order.size)
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        ovr = np.array([intersection(quad_list[i], quad_list[j]) for j in order[1:]])
        # print(type(ovr))
        # 返回的是符合条件的j的序列
        inds = np.asarray(np.where(ovr <= iou_threshold))
        # print(inds)
        # order[inds + 1]是 j 的真实下标
        order = order[inds[0, :] + 1]

    quad_list = quad_list[keep]
    print('NSM后，目标框数目：', len(quad_list))

    img2 = np.zeros((1024, 1024), dtype=np.uint8)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    cv2.polylines(img2, quad_list, True, (0, 0, 255), thickness=2)
    cv2.imshow('img2', img2)
    cv2.waitKey()
    cv2.destroyAllWindows()

    class_18_list = class_18_list[keep]
    print('符合条件的框序号：', keep)
    print('class_18_list.shape: ', class_18_list.shape)
    return quad_list, class_18_list

def test_nms():

    # 声明predict数组
    predict = np.zeros((1, 1024, 1024, 22), dtype=np.float32)
    # print(a.shape)
    # print(a)

    b = np.random.random((20, 30))
    d = np.random.random((20, 30))
    c = np.random.random((20, 30))
    f = c / 2
    # print(c)
    # print(b)
    # print(b.shape)
    predict[0, 500:520, 500:530, 0] = b
    predict[0, 500:520, 500:530, 1] = d
    predict[0, 500:520, 500:530, 2] = c
    predict[0, 500:520, 500:530, 3] = f
    # print(predict[0, 500:520, 500:530, 1])

    quad_list, class_18_list = nms(predict=predict, confidence_threshold=0.4, iou_threshold=0.05)
