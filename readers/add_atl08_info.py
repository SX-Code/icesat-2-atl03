import numpy as np

from readers.read_HDF5_ATL08 import read_hdf5_atl08
from readers.utils import ismember


def get_atl08_mapping(atl03_ph_index_beg, atl03_segment_id, atl08_classed_pc_indx,
                      atl08_classed_pc_flag, atl08_segment_id):
    """
    Function to map ATL08 to ATL03 class photons
    Args:
        atl03_ph_index_beg:
        atl03_segment_id:
        atl08_classed_pc_indx:
        atl08_classed_pc_flag:
        atl08_segment_id:

    Returns:

    """
    # Get ATL03 data
    indsNotZero = atl03_ph_index_beg != 0
    atl03_ph_index_beg = atl03_ph_index_beg[indsNotZero]
    atl03_segment_id = atl03_segment_id[indsNotZero]

    # Find ATL08 segments that have ATL03 segments
    atl03SegsIn08TF, atl03SegsIn08Inds = ismember(atl08_segment_id, atl03_segment_id)

    # Get ATL08 classed indices and values
    atl08classed_inds = atl08_classed_pc_indx[atl03SegsIn08TF]
    atl08classed_vals = atl08_classed_pc_flag[atl03SegsIn08TF]

    # Determine new mapping into ATL03 data
    atl03_ph_beg_inds = atl03SegsIn08Inds
    atl03_ph_beg_val = atl03_ph_index_beg[atl03_ph_beg_inds]
    newMapping = atl08classed_inds + atl03_ph_beg_val - 2

    # Get max size of output array
    sizeOutput = newMapping[-1]

    # Pre-populate all photon classed array with zeroes
    allph_classed = (np.zeros(sizeOutput + 1)) - 1

    # Populate all photon classed array from ATL08 classifications
    allph_classed[newMapping] = atl08classed_vals

    # Return all photon classed array
    return allph_classed


def add_atl08_classed_flag(filepath_08, beam, atl03_mod):
    """
    添加ATL08分类数据到ATL03中
    Args:
        filepath_08: ATL08数据文件位置
        beam: 波束，与ATL03保持一致
        atl03_mod: ATL03数据

    Returns:
    携带ATL08分类信息
    """
    val_03 = atl03_mod
    val_08 = read_hdf5_atl08(filepath_08, beam)

    # val_03['classed_pc_flag'] = np.zeros_like(val_03['heights']['h_ph']) + np.NaN
    atl03_heights = val_03['heights']['h_ph']

    # -- 分段中的第一个光子（转换为基于0的索引）
    segment_index_begin = val_03['geolocation']['ph_index_beg']
    segment_id = val_03['geolocation']['segment_id']

    # 追踪到ATL03上特定20m Segment_ID的光子的段ID
    ph_segment_id = val_08['signal_photons']['ph_segment_id']

    # 该索引追溯到ATL03上20m segment_id内的特定光子。
    classed_pc_index = val_08['signal_photons']['classed_pc_indx']
    # 每个光子的陆地植被ATBD分类标志为噪声、地面、树冠和树冠顶部。0=噪音，1=地面，2=冠层，或3=冠层顶部
    classed_pc_flag = val_08['signal_photons']['classed_pc_flag']

    # Map ATL08 classifications to ATL03 Photons
    all_ph_classed = get_atl08_mapping(segment_index_begin, segment_id,
                                       classed_pc_index, classed_pc_flag, ph_segment_id)

    if len(all_ph_classed) < len(atl03_heights):
        n_zeros = len(atl03_heights) - len(all_ph_classed)
        zeros = np.zeros(n_zeros)
        all_ph_classed = np.append(all_ph_classed, zeros)

    val_03['classed_pc_flag'] = all_ph_classed

