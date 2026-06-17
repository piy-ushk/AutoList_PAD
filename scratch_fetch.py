import urllib.request, re, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_ebay(kw):
    url = 'https://www.ebay.com/sch/i.html?_nkw=' + kw.replace(' ', '+')
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8', errors='ignore')
        m = re.findall(r'itm/(\d{12})', html)
        return m[0] if m else None
    except Exception as e:
        return str(e)

def get_mercari(kw):
    url = 'https://neokyo.com/en/search/mercari?keyword=' + kw.replace(' ', '%20')
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8', errors='ignore')
        m = re.findall(r'm\d{11}', html)
        return m[0] if m else None
    except Exception as e:
        return str(e)

cats = {
  'pokemon_card': ('pokemon card singles', 'pokemon card'),
  'figure': ('anime figure boxed', 'anime figure'),
  'plastic_model': ('tamiya 1/24 model kit', 'tamiya 1/24'),
  'vintage_toy': ('chogokin vintage', 'chogokin'),
  'rc_related': ('tamiya rc buggy kit', 'tamiya rc'),
  'game_related': ('super famicom console japan', 'super famicom')
}

res = {}
for k, (ek, mk) in cats.items():
    res[k] = {'ebay': get_ebay(ek), 'mercari': get_mercari(mk)}

print(json.dumps(res, indent=2))
