#!/usr/bin/env python3
from pathlib import Path
import requests
BASE='https://cdnstatic.herogame.com/static/duetnightabyss_gw_1_4/resource_assets/'
FILES=[
 'theme1-f0af692d.mp3','BinaryFate-73f0c310.mp3','theme0-5bdc16d3.mp3','theme2-51179355.mp3',
 'theme3-22a27a7c.mp3','theme4-e6c9ae53.mp3','theme5-c33ecb9e.mp3'
]
out=Path('resource_assets'); out.mkdir(exist_ok=True)
s=requests.Session(); s.headers.update({'User-Agent':'Mozilla/5.0','Referer':'https://duetnightabyss.dna-panstudio.com/'})
for f in FILES:
    p=out/f
    if p.exists() and p.stat().st_size>1000:
        print('exists',p); continue
    r=s.get(BASE+f,timeout=60)
    print(r.status_code, f, len(r.content))
    r.raise_for_status(); p.write_bytes(r.content)
