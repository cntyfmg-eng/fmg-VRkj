# -*- coding: utf-8 -*-
"""
用 Google Gemini 图片生成 API 批量产出《颐和园》VR 方位图。
依赖：requests（managed venv 已安装）
用法：
  1) 设置密钥：  set GEMINI_API_KEY=你的AI_Studio_Key   (或把 key 写入本目录 .gemini_key)
  2) 运行： python gen_gemini_vr.py
可选环境变量：
  GEMINI_MODEL  (默认 gemini-2.5-flash-image)
  GEMINI_BASE   (默认 https://generativelanguage.googleapis.com)
说明：若想输出 VR 全景，可在下方 PROMPTS 的英文里加
  "360-degree equirectangular panorama, 2:1 aspect ratio" 前缀。
"""
import os, sys, json, base64, time, pathlib
import requests

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-image")
BASE = os.environ.get("GEMINI_BASE", "https://generativelanguage.googleapis.com")
KEY = os.environ.get("GEMINI_API_KEY") or (
    (HERE / ".gemini_key").read_text().strip() if (HERE / ".gemini_key").exists() else None
)
if not KEY:
    sys.exit("未找到 GEMINI_API_KEY，请先设置环境变量或在同目录创建 .gemini_key 文件。")

# (文件名, 提示词)  —— 中文提示 Gemini 也能理解，这里用中英混合更稳
PROMPTS = [
    ("01_长廊内景.png",
     "Interior view of the famous Long Corridor in the Summer Palace, Beijing, eye-level angle, "
     "green-painted pillars and red railings stretching far into the distance, colorful painted beams "
     "with figures flowers and landscapes, lush flowers and trees on both sides, soft daylight, "
     "photorealistic, highly detailed, 8k. 颐和园长廊内景，绿柱红栏，五彩横槛画，写实摄影。"),
    ("02_仰视佛香阁.png",
     "Looking up at the Tower of Buddhist Incense from the foot of Longevity Hill in the Summer Palace, "
     "Beijing, an octagonal three-story pagoda-style structure halfway up the hill, golden glazed tiles "
     "glowing in sunlight, below it the magnificent Hall of Dispelling Clouds, blue sky, photorealistic. "
     "颐和园万寿山仰视佛香阁，八角宝塔形三层，黄琉璃瓦，排云殿金碧辉煌。"),
    ("03_俯瞰昆明湖.png",
     "Aerial downward view of Kunming Lake from the top of Longevity Hill in the Summer Palace, Beijing, "
     "the lake calm like a mirror and green like jade, boats gliding slowly, faint ancient city towers and "
     "a white pagoda in the distance, lush greenery framing vermilion palace walls, wide panorama, "
     "photorealistic. 颐和园佛香阁俯瞰昆明湖全景，静绿如镜玉，远眺白塔。"),
    ("04_东堤远眺十七孔桥.png",
     "View from the east dike of Kunming Lake toward the Seventeen-Arch Bridge in the Summer Palace, "
     "Beijing, the stone bridge with seventeen arches forming a graceful curve, weeping willows along "
     "both banks, a verdant island in the lake center, painted boats, warm dusk light, photorealistic. "
     "颐和园昆明湖东堤远眺十七孔桥，十七个桥洞，垂柳，湖心岛。"),
    ("05_十七孔桥石狮.png",
     "Close-up of the stone railing posts on the Seventeen-Arch Bridge in the Summer Palace, Beijing, "
     "hundreds of white-marble posts each carved with a small lion in a different posture, side light, "
     "macro photorealistic, highly detailed. 颐和园十七孔桥石柱小狮子姿态不一，汉白玉，微距写实。"),
    ("06_石舫.png",
     "Full view of the Marble Boat in the Summer Palace, Beijing, a stone boat moored at the edge of "
     "Kunming Lake, ornate carved beams, with the lake and the Tower of Buddhist Incense in the "
     "background, photorealistic. 颐和园石舫清晏舫全景，背景湖光山色与佛香阁。"),
]

URL = f"{BASE}/v1beta/models/{MODEL}:generateContent?key={KEY}"
HEADERS = {"Content-Type": "application/json"}


def gen_one(fname, prompt):
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(URL, headers=HEADERS, json=body, timeout=180)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:400]}")
    data = r.json()
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for p in parts:
        if p.get("inline_data"):
            b64 = p["inline_data"]["data"]
            (OUT / fname).write_bytes(base64.b64decode(b64))
            return True
    raise RuntimeError("返回中未找到图片数据")


def main():
    OUT.mkdir(exist_ok=True)
    for i, (fname, prompt) in enumerate(PROMPTS, 1):
        print(f"[{i}/{len(PROMPTS)}] 生成 {fname} …", flush=True)
        for attempt in range(3):
            try:
                gen_one(fname, prompt)
                print(f"  ✔ 已保存 {OUT / fname}", flush=True)
                break
            except Exception as e:
                print(f"  ✖ 失败({attempt+1}/3): {e}", flush=True)
                time.sleep(4)
        time.sleep(2)
    print("全部完成，输出目录：", OUT)


if __name__ == "__main__":
    main()
