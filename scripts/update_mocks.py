import json
import os

with open('config/demo_mocks.json', 'r', encoding='utf-8') as f:
    mocks = json.load(f)

mocks['Nintendo Super Famicom Console Boxed CIB Tested Working SFC'] = {
    'title': 'Nintendo Super Famicom Console CIB Tested Working Complete Japan Authentic Retro',
    'itemSpecifics': {
        'Brand': 'Nintendo',
        'Model': 'Super Famicom',
        'UPC': 'Does not apply',
        'Platform': 'Nintendo Super Famicom',
        'Region Code': 'NTSC-J (Japan)',
        'Color': 'Gray',
        'Type': 'Home Console',
        'Storage Capacity': 'Not Applicable',
        'Connectivity': 'AV Multi Out, RF',
        'MPN': 'SHVC-001',
        'Year Manufactured': '1990',
        'Charger Included': 'No',
        'Device Charging Range': 'Not Applicable',
        'Features': 'Tested & Working, CIB, Authentic',
        'Resolution': '256 × 224',
        'California Prop 65 Warning': 'No',
        'Country of Origin': 'Japan',
        'Item Depth': '20.0 cm (7.87 inches)',
        'Item Height': '7.3 cm (2.87 inches)',
        'Item Length': '24.2 cm (9.53 inches)',
        'Item Weight': '0.60 kg (1.32 lb)',
        'Manufacturer Warranty': 'None',
        'Unit Quantity': '1',
        'Unit Type': 'Unit',
        'Materials sourced from': 'Plastic'
    },
    'nested_sections': [
        {
            'header': 'Product Development Background',
            'bullets': [
                'Nintendo developed the Super Famicom as the successor to the Family Computer, introducing a powerful 16-bit architecture.',
                'The console featured advanced graphics and sound capabilities that redefined home gaming in the early 1990s.',
                'Dedicated enhancement chips inside game cartridges expanded hardware performance beyond the base console.',
                'Its ergonomic controller established a design standard later adopted throughout the gaming industry.',
                'The platform became home to many legendary first-party and third-party titles that remain influential today.'
            ]
        },
        {
            'header': 'Rarity',
            'bullets': [
                'Complete in Box (CIB) sets are increasingly difficult to find in well-preserved condition.',
                'Original packaging and manuals significantly enhance collector value.',
                'Japanese-market consoles are sought after for their authenticity and historical significance.',
                'Working units with verified functionality are preferred by both collectors and players.',
                'Demand continues to grow as retro gaming becomes more popular worldwide.'
            ]
        },
        {
            'header': 'Description',
            'bullets': [
                'Genuine Nintendo Super Famicom console released for the Japanese market.',
                'Tested and confirmed to operate properly before shipment.',
                'Complete in Box package ideal for collectors and retro gaming enthusiasts.',
                'Compatible with the extensive Japanese Super Famicom software library.',
                'A timeless piece of gaming history representing Nintendo\'s golden era.'
            ]
        },
        {
            'header': 'Features',
            'bullets': [
                'Authentic Japanese NTSC-J hardware.',
                'Includes original console and complete retail package.',
                '16-bit CPU delivers classic retro gaming performance.',
                'Supports iconic Nintendo franchises and thousands of game titles.',
                'Excellent addition to any retro gaming or Nintendo collection.'
            ]
        }
    ],
    'flat_sections': []
}

mocks['Vintage Alice in Wonderland Japanese 3D Picture Book 1980s'] = {
    'title': 'Vintage Alice in Wonderland 3D Pop-Up Picture Book 1980s Japan Hardcover Rare',
    'itemSpecifics': {
        'ISBN': 'Does not apply',
        'Topic': 'Pop-Up & Interactive Books',
        'Publisher': 'Unknown',
        'Author': 'Based on Lewis Carroll',
        'Binding': 'Hardcover',
        'Subject': 'Children\'s Literature',
        'Special Attributes': '3D Pop-Up',
        'Language': 'Japanese',
        'Character Family': 'Alice in Wonderland',
        'Original/Facsimile': 'Original',
        'Region': 'Japan',
        'Signed': 'No',
        'Illustrator': 'Unknown',
        'Personalized': 'No',
        'Place of Publication': 'Japan',
        'Year Printed': '1980', 
        'Country/Region of Manufacture': 'Japan',
        'California Prop 65 Warning': 'No',
        'Unit Quantity': '1',
        'Unit Type': 'Unit'
    },
    'nested_sections': [
        {
            'header': 'Product Development Background',
            'bullets': [
                'Japanese publishers embraced pop-up and movable book technology during the late 1970s and 1980s to create immersive reading experiences.',
                'Alice in Wonderland was selected because its imaginative world naturally suited three-dimensional paper engineering.',
                'Pop-up books combined traditional printing with precision die-cutting and hand assembly, making production highly specialized.',
                'Japanese editions from this period are appreciated for their high-quality printing and durable paper craftsmanship.',
                'These books were designed to inspire children\'s creativity while appealing to collectors of illustrated literature.'
            ]
        },
        {
            'header': 'Rarity',
            'bullets': [
                'Original Japanese pop-up editions from the 1980s are becoming increasingly difficult to locate in complete condition.',
                'Three-dimensional mechanisms are often damaged over time, making intact examples especially desirable.',
                'Vintage interactive books have gained popularity among collectors of children\'s literature and paper engineering.',
                'Japanese-market editions were produced in relatively limited quantities compared with modern reprints.',
                'Well-preserved copies command premium prices in the international collectible book market.'
            ]
        },
        {
            'header': 'Description',
            'bullets': [
                'Vintage Japanese hardcover edition featuring beautiful three-dimensional pop-up artwork.',
                'Based on the timeless story of Alice in Wonderland by Lewis Carroll.',
                'Carefully crafted paper engineering creates an engaging visual reading experience.',
                'An excellent collectible for vintage book enthusiasts and Alice collectors.',
                'A charming display piece representing classic Japanese illustrated publishing.'
            ]
        },
        {
            'header': 'Features',
            'bullets': [
                'Authentic vintage Japanese edition.',
                'Three-dimensional pop-up paper engineering.',
                'Hardcover construction for long-term preservation.',
                'Colorful illustrations inspired by the classic fantasy story.',
                'Ideal for collectors, display, or nostalgic reading.'
            ]
        }
    ],
    'flat_sections': []
}

mocks['おやこでいっしょにアンパンマンシアター'] = {
    'title': 'Bandai Anpanman Theater Playset Vintage Used Japan Original Collectible Toy',
    'itemSpecifics': {
        'Type': 'Playset',
        'UPC': 'Does not apply',
        'Franchise': 'Anpanman',
        'Character': 'Anpanman',
        'Brand': 'Bandai',
        'Movie': 'Does Not Apply',
        'TV Show': 'Soreike! Anpanman',
        'Featured Person/Artist': 'Does Not Apply',
        'Material': 'Plastic',
        'Scale': 'Not to Scale',
        'Theme': 'Anime & Manga',
        'Model': 'Anpanman Theater',
        'Grade': 'Ungraded',
        'Professional Grader': 'Not Professionally Graded',
        'Certification Number': 'Does Not Apply',
        'Sport': 'Does Not Apply',
        'Convention/Event': 'Does Not Apply',
        'Original/Licensed Reproduction': 'Original',
        'Vintage': 'Yes',
        'Time Period Manufactured': '1990-1999',
        'MPN': 'Does Not Apply',
        'Series': 'Anpanman Toys',
        'Year Manufactured': '1990s',
        'Color': 'Multicolor',
        'Animal Species': 'Does Not Apply',
        'Items Included': 'Main Unit',
        'Features': 'Original Bandai Release, Interactive Playset',
        'Animation Studio': 'TMS Entertainment',
        'Vehicle Type': 'Does Not Apply',
        'Country/Region of Manufacture': 'Japan',
        'Item Height': '18.5 cm (7.28 inches)',
        'Signed': 'No',
        'Signed By': 'Does Not Apply',
        'Autograph Format': 'Does Not Apply',
        'Personalize': 'No',
        'Personalization Instructions': 'Does Not Apply',
        'Age Level': '3+',
        'Transformer Faction': 'Does Not Apply',
        'Item Length': '24.5 cm (9.65 inches)',
        'Item Width': '11.5 cm (4.53 inches)',
        'Item Weight': '0.55 kg (1.21 lb)',
        'California Prop 65 Warning': 'No',
        'Unit Quantity': '1',
        'Unit Type': 'Unit',
        'Customized': 'No',
        'Custom Bundle': 'No',
        'Number in Pack': '1',
        'Packaging': 'Without Original Box',
        'Genre': 'Animation'
    },
    'nested_sections': [
        {
            'header': 'Product Development Background',
            'bullets': [
                'Bandai developed the Anpanman Theater series to recreate scenes from the beloved children\'s television program through interactive play.',
                'The playset encourages imaginative storytelling by combining familiar characters with movable play features.',
                'Produced during the peak popularity of Soreike! Anpanman, these toys reflected Bandai\'s emphasis on safe and durable children\'s products.',
                'The colorful design faithfully captures the artwork and atmosphere established by creator Takashi Yanase.',
                'Japanese domestic releases are recognized for their high molding quality and long-lasting construction.'
            ]
        },
        {
            'header': 'Rarity',
            'bullets': [
                'Original Japanese Bandai releases become increasingly difficult to find complete after years of children\'s play.',
                'Many surviving examples are missing accessories, making well-preserved sets more desirable.',
                'Vintage Anpanman toys have gained steady popularity among collectors of Japanese character merchandise.',
                'Early domestic releases are valued for their nostalgic design and authentic production quality.',
                'Complete or functional examples command stronger prices in the international collector market.'
            ]
        },
        {
            'header': 'Description',
            'bullets': [
                'Authentic Bandai Anpanman Theater playset released for the Japanese market.',
                'Features colorful details inspired by the classic television series.',
                'A nostalgic collectible representing one of Japan\'s most beloved children\'s franchises.',
                'Suitable for display, collection, or vintage toy enthusiasts.',
                'Carefully designed to deliver imaginative play and lasting appeal.'
            ]
        },
        {
            'header': 'Features',
            'bullets': [
                'Genuine Bandai Japanese release.',
                'Interactive playset with colorful molded details.',
                'Durable plastic construction designed for repeated play.',
                'Popular Anpanman collectible with nostalgic appeal.',
                'Excellent addition to Japanese character toy collections.'
            ]
        }
    ],
    'flat_sections': []
}

with open('config/demo_mocks.json', 'w', encoding='utf-8') as f:
    json.dump(mocks, f, ensure_ascii=False, indent=2)
