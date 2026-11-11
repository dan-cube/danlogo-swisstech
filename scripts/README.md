# scripts · 通用工具

只依赖 Python 3 标准库与系统命令，适合速写、审看与场景示意。新项目开始时，把需要的文件复制到项目的 `src/`。

**本风格从零造字时**，还需要超椭圆、布尔运算和不裁切的渲染：运行 `examples/eonpoint-shouwei/src/setup.sh`（装 skia-pathops、fonttools、pillow 与 resvg 到 `~/.danlogo`），参照那里的 `geo.py` 写几何，用 `render.mjs` 渲染。注意：
- 本机没有 rsvg-convert / cairosvg 时，`render.sh` 会退到 Quick Look，带 width/height 的非正方形 SVG 会被裁掉一部分（审看板会误报“碰到画布边缘”）。横向字标请用 `render.mjs` 渲染。
- `review.py` 适合方形的符号；横向字标会被按宽度塞进方格，小尺寸那两列看不出东西。字标请另外按实际高度渲染（整个字标 32 px、16 px 高）检查签名与灰度。
- `review.py` 的墨色比例只计黑色；双色稿看黑白版的数字。SVG 自带的 width/height 很小时，“原图”一栏会画得很小：导出时设成 1000 左右。

| 文件 | 作用 |
|---|---|
| `geom.py` | 几何与 SVG 生成：填充 `F`、圆 `C`、闭合多边形 `poly`、挖空 `hole`、截取 `clip_poly`、圆弧点列 `arc_pts`、对称补全 `symmetric`、翻转 `mirror`、旋转 `rotate`、描边 `S`、圆环路径 `ring`、平移缩放 `move`、包围盒 `bbox`、按角色上色渲染 `render`、输出文档 `svg_doc` |
| `sheet.py` | 把多个 SVG 拼成一张对比审看图，可用 `--labels` 加标签 |
| `render.sh` | SVG → PNG（依次尝试 rsvg-convert、cairosvg、macOS Quick Look；Quick Look 输出会按 viewBox 比例自动裁边；带超时与重试） |
| `review.py` | 图形感与辨识度审看板：每个 SVG 一行——原图、剪影、反白、32 px 与 16 px 像素放大、实际大小、圆形头像，标签后附墨色比例；形碰到画布边缘时会提示；`--small` 可给每个原型配小尺寸版，多两列（32 / 16 px）对照。小尺寸与头像按墨迹裁切，画布留白多少不影响结果。反白按黑白取反，彩色稿请另看各色彩版本 |
| `mockup.py` | 场景示意（第 7 阶段）：名片、App 图标、官网首屏、形象墙、提案封面、手提袋的扁平模板，放入本项目的 SVG 即可。用法：`python3 mockup.py card.svg card --assets 正面.svg 背面.svg`。个人信息用占位条，这是示意，不是实拍 |

## 最小示例

下面的形只是为了演示写法，不是任何造型建议。

```python
from geom import F, poly, render, svg_doc, bbox

shapes = [F(poly([(0, 0), (100, 0), (100, 100), (0, 100)]), "body")]   # 仅演示 API
colors = {None: "#231F1C", "body": "#231F1C"}
open("mark.svg", "w").write(svg_doc(render(shapes, colors), bbox(shapes), pad=6))
```

```bash
python3 sheet.py sketches.svg c1.svg c2.svg --labels "C1" "C2" --cols 2
./render.sh sketches.svg
python3 review.py board.png p1.svg p2.svg --labels "P1" "P2"   # 图形感与辨识度审看板
```

## 约定

- 形状和颜色分离：形状只标角色（`role`），导出时按色彩版本替换颜色。
- 所有尺寸从一个基准数推出，写在文件顶部。
- 判断好不好看，一律看渲染出的 PNG；第 2 阶段的速写可以、第 3 阶段起的每个原型必须用 `review.py` 出一张审看板。
- 图形优先用填充的面来构造（`F`、`C`、`poly`）；描边只用于确实是线的部分。
- 用了描边的 SVG，正式交付前把描边转成填充路径（见 `references/craft.md`）。
- `hole()` 按 evenodd 规则挖空：几个内轮廓互相重叠时，重叠处会被“抵消”回实心；需要并集时先把内轮廓合成一个。
- `review.py` 在墨迹碰到画布边缘时会提示；有意截取、让形出血的原型可以忽略。

完整的工程示例见各 skill 的 `examples/<案例名>/src/`（只学写法，不复用造型）。
