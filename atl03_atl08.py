from glob import glob

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from readers.add_atl08_info import add_atl08_classed_flag
from readers.get_ATL03_x_atc import get_atl03_x_atc
from readers.read_HDF5_ATL03 import read_hdf5_atl03_beam_h5py


def select_atl03_data(atl03_data, mask):
    """
    选择数据范围
    Args:
        atl03_data: 所有数据
        mask (list): 维度范围
    Returns:
    """
    # 选择范围
    d3 = atl03_data
    subset1 = (d3['heights']['lat_ph'] > min(mask)) & (d3['heights']['lat_ph'] < max(mask))

    x_act = d3['heights']['x_atc'][subset1]
    h = d3['heights']['h_ph'][subset1]
    signal_conf_ph = d3['heights']['signal_conf_ph'][subset1]
    lat = d3['heights']['lat_ph'][subset1]
    lon = d3['heights']['lon_ph'][subset1]
    classed_pc_flag = d3['classed_pc_flag'][subset1]

    return x_act, h, signal_conf_ph, lat, lon, classed_pc_flag


def get_atl03_data(filepath, beam):
    """
    读取ATL03数据，根据维度截取数据
    Args:
        filepath (str): h5文件路径
        beam (str): 光束
    Returns:
        返回沿轨道距离，高程距离，光子置信度
    """
    atl03_file = glob(filepath)
    is2_atl03_mds = read_hdf5_atl03_beam_h5py(atl03_file[0], beam=beam, verbose=False)
    # 添加沿轨道距离到数据中
    get_atl03_x_atc(is2_atl03_mds)
    return is2_atl03_mds


def show_classification(x_origin, y_origin, classification, clz):
    """
    :param clz: -1:未分类, 0:噪声, 1:地形, 2:冠层, 3:冠顶, 4:海洋
    :param classification: 分类数据
    :param y_origin:
    :param x_origin:
    """
    plt.subplots(num=1, figsize=(24, 6))
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.xticks(rotation=270)
    ax.set_xlabel('x_atc, km')
    ax.set_ylabel('h, m')
    ax.xaxis.set_major_locator(MultipleLocator(100))
    colors = ['red', 'black', 'green', 'violet', 'blue', 'grey']
    for flag in clz:
        idx = np.where(classification == flag)
        plt.scatter(x_origin[idx], y_origin[idx], s=5, c=colors[flag])

    plt.show()


if __name__ == '__main__':
    data = {
        'filepath': 'D:\\Users\\SongW\\Documents\\ICESat-2 Data\\ATL03\\ATL03_20200620024106_13070701_005_01.h5',
        'filepath_08': 'D:\\Users\\SongW\\Documents\\ICESat-2 Data\\ATL08\\ATL08_20200620024106_13070701_005_01.h5',
        'beam': 'gt2l',
        'mask': [19.6468, 19.6521]
    }
    atl03_data = atl03_data = get_atl03_data(data['filepath'], data['beam'])
    add_atl08_classed_flag(data['filepath_08'], data['beam'], atl03_data)

    x_origin, y_origin, conf, lat, lon, classed_pc_flag = select_atl03_data(atl03_data, data['mask'])

    show_classification(x_origin, y_origin, classed_pc_flag, [-1, 0, 1, 2, 3])
