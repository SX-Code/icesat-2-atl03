import pandas as pd

from readers import read_data
import matplotlib.pyplot as plt


def show(act, h):
    """
    绘制研究区域数据
    :param act: act，沿轨道距离
    :param h: h，高程
    """
    plt.scatter(act, h)
    plt.show()


def save2file(act, h, conf, lat, lon):
    """
    保存研究区域的一下数据
    :param act: act，沿轨道距离
    :param h: h，高程
    :param conf: 置信度
    :param lat: 维度
    :param lon: 经度
    """
    points = list(zip(act, h, lat, lon, conf))
    data = pd.DataFrame(points, columns=['沿轨道距离', '高程', '维度', '经度', '置信度'])
    data.to_csv('result/points_origin.csv', mode='w', index=False)


if __name__ == '__main__':
    filepath = r'D:\Users\SongW\Downloads\ATL03_20190222135159_08570207_005_01.h5'
    beam = 'gt3l'
    mask_lat = [16.533, 16.550]
    act, h, conf, lat, lon, ref_elev = read_data(filepath, beam, mask_lat, None)
    # save2file(act, h, conf, lat, lon)
    show(act, h)
