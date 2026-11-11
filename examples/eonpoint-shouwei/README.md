# EonPoint「首尾」生成代码

学它的工程写法（参数化字形、图文同源、按角色上色、批量导出），不要复用它的造型和字形。

这套代码比 `scripts/` 多用了两个第三方库，用来做精确的布尔运算和渲染：

```bash
bash src/setup.sh        # 安装 skia-pathops、fonttools、pillow 与 @resvg/resvg-js 到 ~/.danlogo
cd src
~/.danlogo/venv/bin/python export_final.py /path/to/output    # 导出全部标志、图标、中文字标与字母 SVG
ASSET_OUT=/path/to/out ~/.danlogo/venv/bin/python -c "import assets1, assets2; assets1.concept(); assets2.posters()"
```

| 文件 | 内容 |
|---|---|
| `geo.py` | 几何内核：矩形、超椭圆（四段三次曲线近似，参数 k；0.5523 是正圆，越大越方）、描边、布尔运算、SVG 输出。布尔运算偶尔会静默丢形，切线正好穿过顶点时可能报错：运算后检查面积，并看渲染图 |
| `eptype.py` | 26 个小写字母（超椭圆、交接收细、平切） |
| `wm.py` | 字标排字 |
| `cn.py` | 中文字标的笔画骨架 |
| `brand_f.py` | 组合、色彩模式、图标 |
| `kit.py`、`assets1.py`、`assets2.py` | 规范图、体系图与场景图 |
| `export_final.py` | 导出源文件包 |
