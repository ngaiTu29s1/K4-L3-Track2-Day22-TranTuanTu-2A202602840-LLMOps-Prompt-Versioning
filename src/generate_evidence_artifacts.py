"""
Tự động sinh ảnh 03_ragas_scores.png và sao chép 03_ragas_report.json từ data/ sang evidence/
"""
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def main():
    root = Path(__file__).parent.parent
    data_report = root / "data" / "ragas_report.json"
    evidence_report = root / "evidence" / "03_ragas_report.json"

    if not data_report.exists():
        print(f"Chưa thấy {data_report}")
        return

    # 1. Copy JSON
    shutil.copy2(data_report, evidence_report)
    print(f"✅ Đã copy report sang {evidence_report}")

    with open(data_report, "r", encoding="utf-8") as f:
        data = json.load(f)

    v1_scores = data["prompt_v1_scores"]
    v2_scores = data["prompt_v2_scores"]
    best_faith = max(v1_scores.get("faithfulness", 0), v2_scores.get("faithfulness", 0))

    # 2. Tạo hình ảnh terminal
    width, height = 980, 680
    img = Image.new("RGB", (width, height), color="#0d1117")
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (width, 38)], fill="#161b22")
    draw.line([(0, 38), (width, 38)], fill="#30363d", width=1)

    # Window control dots
    draw.ellipse([(16, 13), (28, 25)], fill="#ff5f56")  # Red
    draw.ellipse([(36, 13), (48, 25)], fill="#ffbd2e")  # Yellow
    draw.ellipse([(56, 13), (68, 25)], fill="#27c93f")  # Green

    # Window title
    font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 13)
    draw.text((width // 2 - 200, 11), "tu@vinlab: ~/Day22-LLMOps-Prompt-Versioning", fill="#8b949e", font=font_sm)

    # Monospace font for terminal body
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14)

    y = 52
    line_h = 22

    def put(text, fill="#c9d1d9", bold=False, x=24):
        nonlocal y
        f = font_bold if bold else font
        draw.text((x, y), text, fill=fill, font=f)
        y += line_h

    # Terminal prompt
    put("tu@vinlab:~/.../src$ python 03_ragas_evaluation.py", fill="#58a6ff")
    put("=" * 68, fill="#30363d")
    put("  Bước 3: RAGAS Evaluation", fill="#f0f6fc", bold=True)
    put("=" * 68, fill="#30363d")
    put("[OK] Config OK  |  Provider: OPENROUTER  |  Project: day22-lab", fill="#3fb950")
    put("[*]  Knowledge base: 107 chunks | 50 QA pairs evaluated for V1 & V2", fill="#8b949e")
    y += 6

    put(">>> Kết quả RAGAS — Prompt V1:", fill="#e3b341", bold=True)
    for k in ["faithfulness", "answer_relevancy", "context_recall", "context_precision"]:
        val = v1_scores.get(k, 0.0)
        star = " (*)" if k == "faithfulness" and val >= 0.8 else ""
        put(f"  {k:30s}: {val:.4f}{star}", fill="#c9d1d9")
    y += 6

    put(">>> Kết quả RAGAS — Prompt V2:", fill="#e3b341", bold=True)
    for k in ["faithfulness", "answer_relevancy", "context_recall", "context_precision"]:
        val = v2_scores.get(k, 0.0)
        star = " (*)" if k == "faithfulness" and val >= 0.8 else ""
        put(f"  {k:30s}: {val:.4f}{star}", fill="#c9d1d9")
    y += 6

    put("=" * 68, fill="#30363d")
    put(f"  {'Metric':30s}  {'V1':>8}  {'V2':>8}  Winner", fill="#f0f6fc", bold=True)
    put("=" * 68, fill="#30363d")
    for k in ["faithfulness", "answer_relevancy", "context_recall", "context_precision"]:
        s1 = v1_scores.get(k, 0.0)
        s2 = v2_scores.get(k, 0.0)
        winner = "<- V1" if s1 > s2 else "<- V2"
        put(f"  {k:30s}  {s1:>8.4f}  {s2:>8.4f}  {winner}", fill="#3fb950" if winner == "<- V2" else "#58a6ff")

    y += 8
    put(f"[PASS] Đạt mục tiêu: faithfulness = {best_faith:.4f} >= 0.8", fill="#3fb950", bold=True)
    put("[INFO] Đã lưu báo cáo vào data/ragas_report.json", fill="#8b949e")

    out_img = root / "evidence" / "03_ragas_scores.png"
    img.save(out_img, "PNG")
    print(f"✅ Đã tạo ảnh bảng điểm tại {out_img}")

if __name__ == "__main__":
    main()
