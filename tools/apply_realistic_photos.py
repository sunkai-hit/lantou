from pathlib import Path
import base64
import urllib.request

p = Path('index.html')
s = p.read_text(encoding='utf-8')

URLS = {
    'leak': 'https://images.pexels.com/photos/11017418/pexels-photo-11017418.jpeg?auto=compress&cs=tinysrgb&w=600',
    'repair': 'https://images.pexels.com/photos/32588548/pexels-photo-32588548.jpeg?auto=compress&cs=tinysrgb&w=600',
    'after': 'https://images.pexels.com/photos/35758721/pexels-photo-35758721.jpeg?auto=compress&cs=tinysrgb&w=600',
}

def data_uri(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
        ctype = r.headers.get_content_type() or 'image/jpeg'
    return f'data:{ctype};base64,' + base64.b64encode(data).decode('ascii')

leak = data_uri(URLS['leak'])
repair = data_uri(URLS['repair'])
after = data_uri(URLS['after'])

old_css = '.photoGrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.fakePhoto{height:91px;border-radius:13px;background:linear-gradient(145deg,#D2E1EF,#F7FBFF 55%,#BFD4E7);position:relative;overflow:hidden}.fakePhoto:after{content:"💧";position:absolute;font-size:34px;right:20%;bottom:10px;opacity:.65}.fakePhoto.ok{background:linear-gradient(145deg,#D8EFE6,#FAFFFC)}.fakePhoto.ok:after{content:"✓";color:var(--green)}.submitBar{position:absolute;bottom:0;left:0;right:0;background:#fff;padding:10px 14px 14px;border-top:1px solid var(--line);z-index:8}'
new_css = f'''.photoGrid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.fakePhoto{{height:91px;border-radius:13px;background-image:url({leak});background-size:cover;background-position:center;position:relative;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(21,34,59,.08)}}.fakePhoto:before{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,.03),rgba(15,23,42,.08));pointer-events:none}}.fakePhoto:after{{content:"漏水现场";position:absolute;left:9px;top:9px;padding:3px 7px;border-radius:999px;background:rgba(255,255,255,.9);color:#35506f;font-size:9px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,.06)}}.fakePhoto.leak2{{background-position:center 72%}}.fakePhoto.leak2:after{{content:"积水区域"}}.fakePhoto.repair{{background-image:url({repair});background-position:center}}.fakePhoto.repair:after{{content:"维修处理中"}}.fakePhoto.ok{{background-image:url({after});background-position:center}}.fakePhoto.ok:after{{content:"修复完成";color:#177e58}}.submitBar{{position:absolute;bottom:0;left:0;right:0;background:#fff;padding:10px 14px 14px;border-top:1px solid var(--line);z-index:8}}'''

if old_css not in s:
    raise SystemExit('photo css block not found; abort to avoid damaging current prototype')
s = s.replace(old_css, new_css, 1)

# 居民上报：两张同一现场不同视角/裁切
s = s.replace('<div class="photoGrid"><div class="fakePhoto"></div><div class="fakePhoto"></div></div>', '<div class="photoGrid"><div class="fakePhoto"></div><div class="fakePhoto leak2"></div></div>', 1)

# PC 工单详情：居民上报的两张现场图
s = s.replace('<div class="photoGrid"><div class="fakePhoto" style="height:140px"></div><div class="fakePhoto" style="height:140px"></div></div>', '<div class="photoGrid"><div class="fakePhoto" style="height:140px"></div><div class="fakePhoto leak2" style="height:140px"></div></div>', 1)

# 工作人员端：增加维修处理中照片
s = s.replace('<div class="formLabel">处理前照片</div><div class="fakePhoto"></div>', '<div class="formLabel">现场照片</div><div class="photoGrid"><div class="fakePhoto"></div><div class="fakePhoto repair"></div></div>', 1)

# 集团穿透证据链：中间一张改为维修处理中
s = s.replace('<div><div class="fakePhoto" style="height:150px"></div><div class="strong small" style="margin-top:6px">维修到场照片</div>', '<div><div class="fakePhoto repair" style="height:150px"></div><div class="strong small" style="margin-top:6px">维修处置照片</div>', 1)

p.write_text(s, encoding='utf-8')
print('realistic photos embedded into index.html')
