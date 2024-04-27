from glob import glob

from readers.get_ATL03_x_atc import get_atl03_x_atc
from readers.read_HDF5_ATL03 import read_hdf5_atl03_beam, read_hdf5_atl03_coordinate


def read_data(filepath, beam, mask_lat, mask_lon):
    """
    读取数据，返回沿轨道距离和高程距离
    :param filepath: h5文件路径
    :param beam: 轨道光束
    :param mask_lat: 维度范围
    :param mask_lon: 经度范围
    :return:
    """
    atl03_file = glob(filepath)
    is2_atl03_mds = read_hdf5_atl03_beam(atl03_file[0], beam=beam, verbose=False)
    # 添加沿轨道距离到数据中
    get_atl03_x_atc(is2_atl03_mds)
    # 选择范围
    d3 = is2_atl03_mds
    subset1 = (d3['heights']['lat_ph'] >= min(mask_lat)) & (d3['heights']['lat_ph'] <= max(mask_lat))
    if mask_lon is not None:
        if mask_lon[0] is not None and mask_lon[1] is None:
            subset1 = subset1 & (d3['heights']['x_atc'] >= mask_lon[0])
        elif mask_lon[0] is None and mask_lon[1] is not None:
            subset1 = subset1 & (d3['heights']['x_atc'] <= mask_lon[1])
        else:
            subset1 = subset1 & (d3['heights']['x_atc'] >= min(mask_lon)) & (d3['heights']['x_atc'] <= max(mask_lon))
    x_act = d3['heights']['x_atc'][subset1]
    h = d3['heights']['h_ph'][subset1]
    signal_conf_ph = d3['heights']['signal_conf_ph'][subset1]
    lat = d3['heights']['lat_ph'][subset1]
    lon = d3['heights']['lon_ph'][subset1]
    ref_elev = d3['geolocation']['ref_elev_all'][subset1]

    del d3, subset1
    return x_act, h, signal_conf_ph, lat, lon, ref_elev


def read_all_beam_coordinate(filepath, mask_lat, mask_lon):
    """
    读取所有波束的数据
    :param filepath:
    :param mask_lat:
    :param mask_lon:
    :return:
    """
    atl03_file = glob(filepath)
    is2_atl03_mds = read_hdf5_atl03_coordinate(atl03_file[0])

    # 禁止加载全部数据
    # if mask_lat is None or len(mask_lat) == 0 or mask_lon is None or len(mask_lon) == 0:
    #     return False

    d3 = is2_atl03_mds
    if mask_lon is None and mask_lat is None:
        # 加载全部数据
        return d3
    for beam in is2_atl03_mds.keys():
        subset1 = (d3[beam]['lat'] >= min(mask_lat)) & (d3[beam]['lat'] <= max(mask_lat))
        subset1 = subset1 & (d3[beam]['lon'] >= min(mask_lon)) & (d3[beam]['lon'] <= max(mask_lon))
        d3[beam]['lat'] = d3[beam]['lat'][subset1]
        d3[beam]['lon'] = d3[beam]['lon'][subset1]
    return d3
