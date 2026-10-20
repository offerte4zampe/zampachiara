"""Rebuild social PNG cards locally with Pillow and DejaVu Sans fonts."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'site/assets'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
for name,title,subtitle in [('home','Offerte da fiutare.','Prezzi e offerte per cani e gatti'),('compare','Lo stesso prodotto.','Confronta formato, prezzo e negozio'),('guide','Acquisti più chiari.','Guide e strumenti per risparmiare')]:
 im=Image.new('RGB',(1200,630),'#fffaf2');d=ImageDraw.Draw(im)
 d.rounded_rectangle((44,40,1156,590),radius=38,fill='#eaf3ed')
 d.text((90,80),'Offerte a 4 Zampe',font=ImageFont.truetype(bold,34),fill='#216d68')
 d.text((90,220),title,font=ImageFont.truetype(bold,59),fill='#263f43')
 d.text((90,320),subtitle,font=ImageFont.truetype(font,32),fill='#3d5354')
 d.rounded_rectangle((90,440,560,510),radius=20,fill='#216d68')
 d.text((120,455),'offerte4zampe.it',font=ImageFont.truetype(bold,29),fill='white')
 # A simple paw mark drawn from geometric shapes, matching the site's pet theme.
 d.ellipse((910,405,1040,500),fill='#d97554')
 for box in [(875,345,920,400),(925,315,970,380),(985,315,1030,380),(1035,345,1080,400)]:d.ellipse(box,fill='#d97554')
 im.save(out/('social-'+name+'.png'),optimize=True)
