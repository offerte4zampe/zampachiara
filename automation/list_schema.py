"""Represent only visible list links; no ratings or product equivalence inferred."""
import json
import re


def append_list_schema(html, name, items):
    html = re.sub(r'<script id="o4z-itemlist" type="application/ld\+json">.*?</script>','',html,flags=re.S)
    rows = [{'@type':'ListItem','position':i+1,'name':label,'url':url} for i,(label,url) in enumerate(items) if isinstance(url,str) and url.startswith('https://')]
    for i,row in enumerate(rows):
        row['position'] = i+1
    if not rows:
        return html
    data = {'@context':'https://schema.org','@type':'ItemList','name':name,'itemListElement':rows}
    content = json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    return html.replace('</head>','<script id="o4z-itemlist" type="application/ld+json">'+content+'</script></head>')
