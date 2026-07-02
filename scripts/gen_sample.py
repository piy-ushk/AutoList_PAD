import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.chatgpt import build_html_description

def generate_sample():
    ai_output = {
        "description": "<p>This Megahouse NARUTO Gals DX Hinata Hyuga Ver.3 PVC figure brings the beloved kunoichi to life with breathtaking detail, standing as a beautiful centerpiece for any dedicated Naruto collection.</p><p>Megahouse is a Japanese manufacturer renowned for its exceptionally high-quality figures, and their Gals DX line is particularly famous for capturing dynamic, powerful poses that perfectly represent the character's spirit.</p>"
    }
    html = build_html_description(
        title="Megahouse NALUTO Gals DX Hinata Hyuga Ver.3 PVC figure Statue With Box",
        ai_output=ai_output,
        condition="Used - Like New",
        genre_key="default"
    )
    with open('C:/Users/Piyush Kulkarni/.gemini/antigravity-ide/brain/8d16d481-7bf6-48c6-b67d-0bac0cc34768/sample_description.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Sample generated.")

if __name__ == "__main__":
    generate_sample()
