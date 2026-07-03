import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.chatgpt import build_html_description

def generate_sample():
    ai_output = {
        "description": "This is a dummy description string that is no longer used directly.",
        "nested_sections": [
            {
                "header": "Product Development Background",
                "bullets": [
                    "Bandai developed this Anpanman Theater to provide an immersive storytelling experience for young children and their parents.",
                    "It builds upon the massive popularity of the Anpanman franchise, which has been a staple in Japanese households since the 1970s.",
                    "Designed to be user-friendly, the projector allows for easy operation even in low-light environments."
                ]
            },
            {
                "header": "Rarity",
                "bullets": [
                    "While Anpanman toys are widely produced, this specific theater model is highly sought after by parents.",
                    "Complete working units in good condition have become increasingly difficult to find on the secondary market."
                ]
            },
            {
                "header": "Description",
                "bullets": [
                    "This interactive projector brings the beloved characters of Anpanman to life on your ceiling or wall.",
                    "It features multiple interchangeable discs that tell different classic stories.",
                    "The device includes built-in speakers that play soothing lullabies and narration."
                ]
            },
            {
                "header": "Features",
                "bullets": [
                    "Comes with 3 distinct story discs for varied entertainment.",
                    "Features a sleep timer that automatically turns off the projector after 30 minutes.",
                    "Adjustable focus lens ensures crisp images on surfaces at various distances.",
                    "Battery operated for safe, cord-free use in children's bedrooms."
                ]
            }
        ],
        "flat_sections": [
            {
                "header": "Items Required to Run (Not included)",
                "bullets": [
                    "4x C batteries",
                    "A blank wall or ceiling for projection"
                ]
            },
            {
                "header": "Appearance",
                "bullets": [
                    "Please see the attached photo."
                ]
            },
            {
                "header": "Condition",
                "bullets": [
                    "Used (Good Condition)"
                ]
            },
            {
                "header": "Included Items",
                "bullets": [
                    "Projector Unit",
                    "3 Story Discs",
                    "Instruction Manual (Japanese)"
                ]
            }
        ]
    }
    html = build_html_description(
        title="Anpanman Theater Interactive Projector Bandai Japan",
        ai_output=ai_output,
        condition="Used",
        genre_key="default"
    )
    with open('C:/Users/Piyush Kulkarni/.gemini/antigravity-ide/brain/8d16d481-7bf6-48c6-b67d-0bac0cc34768/sample_description.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Sample generated.")

if __name__ == "__main__":
    generate_sample()
