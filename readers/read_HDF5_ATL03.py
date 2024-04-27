import warnings
import os
import h5py
import re
import pandas as pd


def read_hdf5_atl03_beam(filename, beam, verbose=False):
    return read_hdf5_atl03_beam_h5py(filename, beam)


def read_hdf5_atl03_beam_pandas(filename, beam, verbose=False):
    # 打开HDF5文件进行读取
    h5_store = pd.HDFStore(filename, mode='r')
    root = h5_store.root
    # 为ICESat-2 ATL03变量和属性分配python字典
    atl03_mds = {}

    # 读取文件中每个输入光束
    # beams = [k for k in file_id.keys() if bool(re.match('gt\\d[lr]', k))]
    beams = ['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r']
    if beam not in beams:
        print('请填入正确的光束代码')
        return

    atl03_mds['heights'] = {}
    atl03_mds['geolocation'] = {}

    # -- 获取每个HDF5变量
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # -- ICESat-2 Heights Group
        heights_keys = ['dist_ph_across', 'dist_ph_along', 'h_ph', 'lat_ph', 'lon_ph', 'signal_conf_ph']
        for key in heights_keys:
            atl03_mds['heights'][key] = root[beam]['heights'][key][:]

        geolocation_keys = ['ref_elev', 'ph_index_beg', 'segment_id', 'segment_ph_cnt', 'segment_dist_x',
                            'segment_length']
        # -- ICESat-2 Geolocation Group
        for key in geolocation_keys:
            atl03_mds['geolocation'][key] = root[beam]['geolocation'][key][:]

    h5_store.close()
    return atl03_mds


def read_hdf5_atl03_beam_h5py(filename, beam, verbose=False):
    """
    ATL03 原始数据读取
    Args:
        filename (str): h5文件路径
        beam (str): 光束
        verbose (bool): 输出HDF5信息

    Returns:
        返回ATL03光子数据的heights和geolocation信息
    """

    # 打开HDF5文件进行读取
    file_id = h5py.File(os.path.expanduser(filename), 'r')

    # 输出HDF5文件信息
    if verbose:
        print(file_id.filename)
        print(list(file_id.keys()))
        print(list(file_id['METADATA'].keys()))

    # 为ICESat-2 ATL03变量和属性分配python字典
    atl03_mds = {}

    # 读取文件中每个输入光束
    beams = [k for k in file_id.keys() if bool(re.match('gt\\d[lr]', k))]
    if beam not in beams:
        print('请填入正确的光束代码')
        return

    atl03_mds['heights'] = {}
    atl03_mds['geolocation'] = {}
    atl03_mds['bckgrd_atlas'] = {}

    # -- 获取每个HDF5变量
    # -- ICESat-2 Measurement Group
    for key, val in file_id[beam]['heights'].items():
        atl03_mds['heights'][key] = val[:]

    # -- ICESat-2 Geolocation Group
    for key, val in file_id[beam]['geolocation'].items():
        atl03_mds['geolocation'][key] = val[:]

    for key, val in file_id[beam]['bckgrd_atlas'].items():
        atl03_mds['bckgrd_atlas'][key] = val[:]

    return atl03_mds


def read_hdf5_atl03_coordinate(filename):
    root = pd.HDFStore(filename).root
    atl03_coordinate = {}
    beams = ['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r']
    with warnings.catch_warnings():
        for beam in beams:
            atl03_coordinate[beam] = {}
            atl03_coordinate[beam]['lat'] = root[beam]['heights']['lat_ph'][:]
            atl03_coordinate[beam]['lon'] = root[beam]['heights']['lon_ph'][:]

    return atl03_coordinate
