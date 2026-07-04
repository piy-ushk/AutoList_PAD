import json
import os

mock_additions = {
  "TEST-DEMO-6": {
    "title": "Vintage Tin Toy Robot 1960s Japan Wind Up Original Box",
    "description": "This is a rare vintage tin toy robot from the 1960s, manufactured in Japan. Wind-up mechanism works perfectly.",
    "itemSpecifics": {
      "Brand": "Unknown",
      "Theme": "Robots, Monsters & Space",
      "Year": "1960",
      "Material": "Tin",
      "Country/Region of Manufacture": "Japan",
      "Vintage": "Yes",
      "Condition": "Used",
      "UPC": "Does not apply"
    }
  },
  "TEST-DEMO-7": {
    "title": "Hatsune Miku 1/7 Scale Figure Miku Symphony 2019 Ver.",
    "description": "Beautiful 1/7 scale figure of Hatsune Miku from the Symphony 2019 concert. Highly detailed and includes original box.",
    "itemSpecifics": {
      "Brand": "Good Smile Company",
      "Character": "Hatsune Miku",
      "Franchise": "Vocaloid",
      "Type": "Figure",
      "Scale": "1:7",
      "Material": "PVC, ABS",
      "Year Manufactured": "2021",
      "Condition": "New",
      "UPC": "4580416942639"
    }
  },
  "TEST-DEMO-8": {
    "title": "Pokemon Card Pikachu Promo 001/S-P Full Art Holo Mint",
    "description": "Pikachu promo card from the Sword & Shield era. Mint condition, never played, stored in a protective sleeve.",
    "itemSpecifics": {
      "Game": "Pokémon TCG",
      "Character": "Pikachu",
      "Card Name": "Pikachu",
      "Card Type": "Pokémon",
      "Finish": "Holo",
      "Rarity": "Promo",
      "Condition": "Near Mint or Better",
      "Graded": "No",
      "Language": "Japanese",
      "UPC": "Does not apply"
    }
  },
  "TEST-DEMO-9": {
    "title": "Canon EOS 5D Mark IV DSLR Camera Body Only Tested Japan",
    "description": "Canon EOS 5D Mark IV in excellent working condition. Tested and fully functional. Includes battery and charger.",
    "itemSpecifics": {
      "Brand": "Canon",
      "Model": "Canon EOS 5D Mark IV",
      "Type": "Digital SLR",
      "Maximum Resolution": "30.4 MP",
      "Color": "Black",
      "Battery Type": "Lithium-Ion",
      "Connectivity": "USB, HDMI, Wi-Fi",
      "Condition": "Used",
      "UPC": "013803281358"
    }
  },
  "TEST-DEMO-10": {
    "title": "Canon EF 50mm f/1.4 USM Standard Prime Lens Near Mint",
    "description": "Standard prime lens for Canon EF mount. Optics are clean, no scratches, haze, or fungus. Autofocus works perfectly.",
    "itemSpecifics": {
      "Brand": "Canon",
      "Model": "Canon EF 50mm f/1.4 USM",
      "Focal Length": "50mm",
      "Maximum Aperture": "f/1.4",
      "Mount": "Canon EF",
      "Type": "Standard, Prime",
      "Focus Type": "Auto & Manual",
      "Condition": "Used",
      "UPC": "013803105371"
    }
  },
  "TEST-DEMO-11": {
    "title": "Sony Cyber-shot DSC-RX100 VII Digital Camera Black",
    "description": "Compact digital camera with 1.0-type sensor and fast autofocus. Very little wear, mostly kept in a case.",
    "itemSpecifics": {
      "Brand": "Sony",
      "Model": "Sony Cyber-shot DSC-RX100 VII",
      "Type": "Compact",
      "Maximum Resolution": "20.1 MP",
      "Color": "Black",
      "Battery Type": "Lithium-Ion",
      "Optical Zoom": "8x",
      "Condition": "Used",
      "UPC": "027242918861"
    }
  },
  "TEST-DEMO-12": {
    "title": "Sony Alpha a7 III Mirrorless Digital Camera Body ILCE-7M3",
    "description": "Full-frame mirrorless camera body. Low shutter count. Excellent condition inside and out.",
    "itemSpecifics": {
      "Brand": "Sony",
      "Model": "Sony Alpha a7 III",
      "Type": "Mirrorless Interchangeable Lens",
      "Maximum Resolution": "24.2 MP",
      "Color": "Black",
      "Battery Type": "Lithium-Ion",
      "Connectivity": "USB-C, Micro-USB, HDMI, Wi-Fi",
      "Condition": "Used",
      "UPC": "027242911961"
    }
  },
  "TEST-DEMO-13": {
    "title": "Fujifilm QuickSnap Flash 400 Disposable 35mm Camera 27 Exp",
    "description": "Single-use disposable camera with built-in flash. Loaded with ISO 400 film for 27 exposures. Brand new, unexpired.",
    "itemSpecifics": {
      "Brand": "Fujifilm",
      "Model": "Fujifilm QuickSnap Flash 400",
      "Type": "Disposable",
      "Film Format": "35 mm",
      "Color": "Green",
      "Features": "Built-in Flash",
      "Condition": "New",
      "UPC": "074101111663"
    }
  }
}

with open('config/demo_mocks.json', 'r', encoding='utf-8') as f:
    mocks = json.load(f)

mocks.update(mock_additions)

with open('config/demo_mocks.json', 'w', encoding='utf-8') as f:
    json.dump(mocks, f, ensure_ascii=False, indent=2)

print('Added 8 new mock items successfully.')
