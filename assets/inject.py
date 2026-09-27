# -*- coding: utf-8 -*-
"""fmg-VRkj 打包脚本
把 three.js 库 + 6 张 VR 场景图（+ 可选二维码 / 背景音乐）注入模板，
产出“单文件、可离线、双击即用”的 VR 互动课件 HTML。

用法：
  python inject.py --img-dir VR场景 --out 第18课颐和园VR互动课件.html
可选参数：
  --qr        gate-qr.jpg        公众号二维码（不传则尝试同目录 gate-qr.jpg，再否则留空）
  --mp3       1.mp3              背景音乐文件名（默认 1.mp3，需与成品同目录）
  --lecturer  "授课人：冯萌刚"    首页可编辑署名（默认）
  --title     "18 颐和园 · VR游园课堂"
依赖：仅标准库。图片自动压缩到 1600 宽 q72 需 Pillow（已自带则更好）。
"""
import argparse, base64, glob, pathlib, sys, io

HERE = pathlib.Path(__file__).resolve().parent
TRANSPARENT = ("data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M8AAAMBAQDJ/pLvAAAAAElFTkSuQmCC")

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def compress(src, max_w=1600, q=72):
    """尽量用 Pillow 压缩；没有 Pillow 就原样返回字节(base64 体积略大)。"""
    try:
        from PIL import Image
        im = Image.open(src).convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, int(im.height*max_w/im.width)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
        return buf.getvalue()
    except Exception:
        return pathlib.Path(src).read_bytes()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img-dir", default="VR场景")
    ap.add_argument("--out", required=True)
    ap.add_argument("--qr")
    ap.add_argument("--mp3", default="1.mp3")
    ap.add_argument("--lecturer", default="授课人：冯萌刚")
    ap.add_argument("--title", default="18 颐和园 · VR游园课堂")
    a = ap.parse_args()

    tpl = (HERE/"template.html").read_text(encoding="utf-8")
    three = (HERE/"three.min.js").read_text(encoding="utf-8")
    if "</script" in three.lower():
        three = three.replace("</script", "<\\/script").replace("</SCRIPT", "<\\/SCRIPT")

    # 场景顺序固定：s1长廊 s2万寿山脚下 s3万寿山 s4昆明湖 s5十七孔桥 s6石舫
    imgdir = pathlib.Path(a.img_dir)
    for i in range(1, 7):
        found = None
        for pat in [f"{i:02d}_*.jpg", f"{i:02d}_*.png", f"{i:02d}.jpg", f"{i:02d}.png"]:
            fl = sorted(glob.glob(str(imgdir/pat)))
            if fl: found = fl[0]; break
        if not found:
            sys.exit(f"❌ 缺少第{i}张场景图：期望 {imgdir}/{i:02d}_*.jpg")
        ph = f"__IMG_s{i}__"
        if ph not in tpl: sys.exit("模板缺少占位符 "+ph)
        data = compress(found)
        tpl = tpl.replace(ph, "data:image/jpeg;base64," + base64.b64encode(data).decode())

    # 二维码
    qr = a.qr
    if not qr:
        for c in [imgdir/"gate-qr.jpg", pathlib.Path("gate-qr.jpg")]:
            if c.exists(): qr = str(c); break
    if qr and pathlib.Path(qr).exists():
        qrdata = "data:image/jpeg;base64," + b64(qr)
        print("✓ 已嵌入二维码：", qr)
    else:
        qrdata = TRANSPARENT
        print("⚠ 未找到二维码，更多资源弹窗将显示空白图（可在课件内替换）")
    if "__IMG_QR__" not in tpl: sys.exit("模板缺少 __IMG_QR__ 占位符")
    tpl = tpl.replace("__IMG_QR__", qrdata)

    # three.js
    if "__THREE_JS__" not in tpl: sys.exit("模板缺少 __THREE_JS__ 占位符")
    tpl = tpl.replace("__THREE_JS__", three)

    # 可配置项
    tpl = tpl.replace("授课人：冯萌刚", a.lecturer)
    tpl = tpl.replace("18 颐和园 · VR游园课堂", a.title)
    tpl = tpl.replace("'1.mp3'", f"'{a.mp3}'")

    out = pathlib.Path(a.out)
    out.write_text(tpl, encoding="utf-8")
    print("✅ 已生成：", out, f"（{out.stat().st_size/1024/1024:.2f} MB）")

if __name__ == "__main__":
    main()
