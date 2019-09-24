import numpy as np
import random

def iou(box, clusters):
    """
    Calculates the Intersection over Union (IoU) between a box and k clusters.
    :param box: tuple or array, shifted to the origin (i. e. width and height)
    :param clusters: numpy array of shape (k, 2) where k is the number of clusters
    :return: numpy array of shape (k, 0) where k is the number of clusters
    """
    x = np.minimum(clusters[:, 0], box[0])
    y = np.minimum(clusters[:, 1], box[1])
    if np.count_nonzero(x == 0) > 0 or np.count_nonzero(y == 0) > 0:
        raise ValueError("Box has no area")

    intersection = x * y
    box_area = box[0] * box[1]
    cluster_area = clusters[:, 0] * clusters[:, 1]

    iou_ = intersection / (box_area + cluster_area - intersection)

    return iou_


def load_dataset(gt_dir):
    dataset = []
    width = 800
    height = 800
    with open(gt_dir, encoding="utf-8") as gt_f:
        lines = gt_f.readlines()
        if len(lines) != 0:  # 跳过没有目标的图片
            lines = [line.strip() for line in lines]
            for line in lines:
                line_split = line.split(" ")
                if len(line_split) < 10:
                    continue
                origin = [int(float(split)) for split in line_split[:8]]
                # 外接矩形
                xmin = min(origin[0::2]) / width
                xmax = max(origin[0::2]) / width
                ymin = min(origin[1::2]) / height
                ymax = max(origin[1::2]) / height
                if xmax - xmin <= 0 or ymax - ymin <= 0:
                    continue
                dataset.append([xmax - xmin, ymax - ymin])

    return np.array(dataset)

def kmeans(boxes, k, dist=np.median):
    """
    Calculates k-means clustering with the Intersection over Union (IoU) metric.
    :param boxes: numpy array of shape (r, 2), where r is the number of rows
    :param k: number of clusters
    :param dist: distance function
    :return: numpy array of shape (k, 2)
    """
    rows = boxes.shape[0]

    # 返回维度为(32, k),元素随机生成的矩阵
    distances = np.empty((rows, k))
    # print("distance:", distances.shape)
    # 长度32的一维数组
    last_clusters = np.zeros((rows,))
    # print("last_clusters:", last_clusters.shape)

    np.random.seed()

    # the Forgy method will fail if the whole array contains the same rows （k, 2）
    clusters = boxes[np.random.choice(rows, k, replace=False)]  # 选出K个中心
    # print('clusters:', clusters.shape)

    while True:
        for row in range(rows):
            distances[row] = 1 - iou(boxes[row], clusters)
        nearest_clusters = np.argmin(distances, axis=1)
        # print("nearest_clusters:", nearest_clusters)
        print('*****again*****')

        if (last_clusters == nearest_clusters).all():
            break

        num_list = []
        clusters_list = []
        for cluster in range(k):
            # clusters[cluster] = boxes[nearest_clusters == cluster]
            clusters_list.append(boxes[nearest_clusters == cluster])
            num_list.append(len(clusters_list[cluster]))
        # print(' clusters_list:',  clusters_list)
        # print("num_list:", num_list)
        # 重新取k个中心点
        # dist 指：np.median
        for j in range(k):
            if num_list[j] == 0:
                cu_older = num_list.index(max(num_list))
                clusters[j] = random.sample(clusters_list[cu_older], 1)
                # 不等于中位数，否则和k=cu_older的簇重合
                while clusters[j] == dist(clusters_list[cu_older], axis=0):
                    clusters[j] = random.sample(clusters_list[cu_older], 1)
            else:
                clusters[j] = dist(clusters_list[j], axis=0)
                # print('clusts[j]:', clusters[j])

        last_clusters = nearest_clusters

    return clusters


if __name__ == '__main__':
    src_path = "D:/competition/kmeans_cluster/labelTxt/val/P0003__1__0___0.txt"
    data = load_dataset(src_path)
    out = kmeans(data, k=5)
    print(out)
