import numpy as np


def get_atl03_x_atc(atl03_mds):
    val = atl03_mds

    # 初始化
    val['heights']['x_atc'] = np.zeros_like(val['heights']['h_ph']) + np.NaN
    val['heights']['y_atc'] = np.zeros_like(val['heights']['h_ph']) + np.NaN
    val['geolocation']['ref_elev_all'] = np.zeros_like(val['heights']['h_ph'])

    # -- ATL03 Segment ID
    segment_id = val['geolocation']['segment_id']
    # -- 分段中的第一个光子（转换为基于0的索引）
    segment_index_begin = val['geolocation']['ph_index_beg'] - 1
    # -- 分段中的光子事件数
    segment_pe_count = val['geolocation']['segment_ph_cnt']
    # -- 每个ATL03段的沿轨道距离
    segment_distance = val['geolocation']['segment_dist_x']
    # -- 每个ATL03段的轨道长度
    segment_length = val['geolocation']['segment_length']

    # -- 对ATL03段进行迭代，以计算40m的平均值
    # -- 在ATL03中基于1的索引：无效==0
    # -- 此处为基于0的索引：无效==-1
    segment_indices, = np.nonzero((segment_index_begin[:-1] >= 0) &
                                  (segment_index_begin[1:] >= 0))
    for j in segment_indices:
        # -- j 段索引
        idx = segment_index_begin[j]
        # -- 分段中的光子数（使用2个ATL03分段）
        c1 = np.copy(segment_pe_count[j])
        c2 = np.copy(segment_pe_count[j + 1])
        cnt = c1 + c2

        # -- 沿轨道和跨轨道距离
        # -- 获取当前段光子列表，idx当前段(j)第一个光子数量，c1当前段光子数量，idx+c1当前段长度
        distance_along_x = np.copy(val['heights']['dist_ph_along'][idx: idx + cnt])
        ref_elev = np.copy(val['geolocation']['ref_elev'][j])
        # -- 给当前段的光子加上当前段沿轨道距离
        distance_along_x[:c1] += segment_distance[j]
        distance_along_x[c1:] += segment_distance[j + 1]
        distance_along_y = np.copy(val['heights']['dist_ph_across'][idx: idx + cnt])

        val['heights']['x_atc'][idx: idx + cnt] = distance_along_x
        val['heights']['y_atc'][idx: idx + cnt] = distance_along_y
        val['geolocation']['ref_elev_all'][idx: idx + c1] += ref_elev
