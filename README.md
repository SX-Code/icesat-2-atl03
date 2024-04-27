# ICESat-2 ATL03数据读取

## 文件结构
```bash
.
├── readers # 数据读取
│   ├── add_atl08_info.py # 从ATL08中读取ATL03分类信息
│   ├── get_ATL03_x_atc.py # 重建ATL03沿轨道距离
│   ├── get_xy_in_segment.py # 分段获取数据
│   ├── read_HDF5_ATL03.py # 读取ATL03数据
│   └── read_HDF5_ATL08.py # 读取ATL08数据
├── atl03_atl08.py # 带分类信息的ATL03
└── main.py # 原始ATL03
```

## 依赖
```markdown
pandas~=2.0.3
matplotlib~=3.7.2
numpy~=1.25.2
h5py~=3.9.0
tables~=3.9.2
```