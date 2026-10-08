"""Deterministic editorial artwork. Optional authoring tool: pip install Pillow beautifulsoup4.
Committed outputs are served directly by GitHub Pages; no deployment build required.
Does not modify or synthesize any photograph. Titles are sourced from site HTML/data.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import os

ROOT = Path(__file__).resolve().parent.parent
NAVY = '#102c44'; DEEP = '#0c2234'; TEAL = '#77cabb'; CREAM = '#f4f3ed'; MUTED = '#a9c6cb'
FONT_DIR = Path(os.environ.get('EDITORIAL_FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
BOLD = FONT_DIR / 'DejaVuSans-Bold.ttf'
SERIF = FONT_DIR / 'DejaVuSerif.ttf'
def font(path, size):
    if not path.exists():
        raise FileNotFoundError(f'{path} missing; install DejaVu fonts or set EDITORIAL_FONT_DIR')
    return ImageFont.truetype(str(path), size)
def lines(draw, text, f, max_width):
    out = []; current = ''
    for word in text.split():
        proposed = (current + ' ' + word).strip()
        if draw.textbbox((0, 0), proposed, font=f)[2] > max_width and current:
            out.append(current); current = word
        else: current = proposed
    if current: out.append(current)
    return out

def geometry(d, cx, cy, scale=1):
    # Access nodes and a documented route: a motif, not a diagram of platform infrastructure.
    nodes = [(cx-165*scale, cy-115*scale, 42*scale), (cx+90*scale, cy-50*scale, 60*scale), (cx-65*scale, cy+125*scale, 48*scale)]
    for a,b in ((0,1),(1,2)):
        x,y,_=nodes[a]; xx,yy,_=nodes[b]
        d.line((x,y,xx,yy), fill='#408484', width=max(2, round(3*scale)))
    for idx,(x,y,r) in enumerate(nodes):
        d.ellipse((x-r,y-r,x+r,y+r), outline=TEAL if idx==2 else '#447982', width=max(2,round(3*scale)))
        rr=8*scale
        d.ellipse((x-rr,y-rr,x+rr,y+rr), fill=TEAL if idx==2 else CREAM)
    d.arc((cx-255*scale,cy-245*scale,cx+255*scale,cy+245*scale), 220, 80, fill='#2f6170', width=max(2,round(2*scale)))

cases = json.loads((ROOT/'data/case-studies.json').read_text())['caseStudies']
labels = ['PAGE ACCESS', 'OWNERSHIP REVIEW', 'ADMIN ACCESS', 'BUSINESS VERIFICATION', 'MULTI-ASSET SUPPORT']
banner_dir=ROOT/'assets/generated/banners'
for i,c in enumerate(cases,1):
    image=Image.new('RGB',(1600,600),DEEP); d=ImageDraw.Draw(image)
    d.rectangle((0,0,14,600),fill=TEAL)
    d.text((90,64),f'CASE STUDY   /   {i:02d}',font=font(BOLD,23),fill=TEAL)
    title=c['title'].replace(': Case Study','').replace(' Case Study','')
    f=font(SERIF,59)
    textlines=lines(d,title,f,800)
    for j,line in enumerate(textlines[:3]): d.text((86,145+82*j),line,font=f,fill=CREAM)
    d.line((90,480,800,480),fill='#3a6875',width=2)
    d.text((90,509),labels[i-1]+'  /  '+(c.get('platform') or 'META PLATFORM'),font=font(BOLD,19),fill=MUTED)
    geometry(d,1270,300,.9)
    slug='zero-idea' if c['slug']=='zero-idea-facebook-page-recovery' else c['slug']
    image.save(banner_dir/f'case-study-banner-{slug}.webp',quality=83,method=6)

# Preview cards: type and title, no synthetic portraits and no unsourced success metrics.
from bs4 import BeautifulSoup
pages = [ROOT/'index.html'] + sorted(ROOT.glob('*/index.html')) + sorted(ROOT.glob('*/*/index.html'))
for p in pages:
    html=p.read_text()
    if 'og:image' not in html: continue
    s=BeautifulSoup(html,'html.parser')
    og=s.find('meta',attrs={'property':'og:image'})
    if not og: continue
    destination=ROOT/og['content'].split('atikulislam.me/')[-1]
    title=(s.find('meta',attrs={'property':'og:title'}) or s.title)['content'] if s.find('meta',attrs={'property':'og:title'}) else s.title.get_text(' ',strip=True)
    # Shorter case titles fit comfortably inside social safe zones.
    title=title.split(' | Atikul Islam Rabbi')[0].split(' — Founder & CEO')[0]
    im=Image.new('RGB',(1200,630),DEEP); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1200,16),fill=TEAL)
    d.text((80,72),'ATIKUL ISLAM RABBI  /  CYBER INFINITY',font=font(BOLD,20),fill=TEAL)
    d.line((80,125,1120,125),fill='#386276',width=2)
    f=font(SERIF,54)
    title_lines=lines(d,title,f,800)
    if len(title_lines)>3:
        f=font(SERIF,46); title_lines=lines(d,title,f,800)
    for j,line in enumerate(title_lines[:4]): d.text((78,186+j*72),line,font=f,fill=CREAM)
    d.text((80,546),'SOCIAL MEDIA SECURITY  &  RECOVERY',font=font(BOLD,20),fill=MUTED)
    geometry(d,1030,340,.46)
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.suffix=='.png': im.save(destination,optimize=True)
    else: im.save(destination,quality=85,optimize=True,progressive=True)

# Tab icon = brand monogram; portrait stays a portrait, never a 16px tab symbol.
icons=ROOT/'assets/generated/favicon'; icons.mkdir(parents=True,exist_ok=True)
for size,name in [(16,'favicon-16.png'),(32,'favicon-32.png'),(180,'apple-touch-icon.png'),(192,'android-chrome-192x192.png'),(512,'android-chrome-512x512.png')]:
    im=Image.new('RGB',(size,size),NAVY); d=ImageDraw.Draw(im)
    # Center a distinct A at the small sizes. Favicon contains no identity photograph.
    f=font(BOLD,round(size*.62))
    box=d.textbbox((0,0),'A',font=f); x=(size-(box[2]-box[0]))/2-box[0]; y=(size-(box[3]-box[1]))/2-box[1]
    d.text((x,y),'A',font=f,fill=CREAM)
    d.rectangle((round(size*.72),round(size*.73),round(size*.84),round(size*.85)),fill=TEAL)
    im.save(icons/name,optimize=True)
images=[Image.open(icons/x).convert('RGBA') for x in ['favicon-16.png','favicon-32.png']]
images[-1].save(icons/'favicon.ico',format='ICO',sizes=[(16,16),(32,32)])
images[-1].save(ROOT/'favicon.ico',format='ICO',sizes=[(16,16),(32,32)])
