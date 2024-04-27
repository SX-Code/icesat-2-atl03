import os
import h5py
import re


def read_hdf5_atl08(filename, beam, verbose=False):
    file_id = h5py.File(os.path.expanduser(filename), 'r')

    # 输出HDF5文件信息
    if verbose:
        print(file_id.filename)
        print(list(file_id.keys()))
        print(list(file_id['METADATA'].keys()))
    # 为ICESat-2 ATL08变量和属性分配python字典
    atl08_mds = {}

    # 读取文件中每个输入光束
    beams = [k for k in file_id.keys() if bool(re.match('gt\\d[lr]', k))]
    if beam not in beams:
        print('请填入正确的光束代码')
        return

    atl08_mds['signal_photons'] = {}
    # -- ICESat-2 Geolocation Group
    for key, val in file_id[beam]['signal_photons'].items():
        atl08_mds['signal_photons'][key] = val[:]

    return atl08_mds
