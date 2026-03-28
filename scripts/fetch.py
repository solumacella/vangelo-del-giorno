import urllib.request
import json
import re
import html
from datetime import datetime

def fetch_vangelo():
    oggi = datetime.now()
    anno = oggi.strftime("%Y")
    mese = oggi.strftime("%m")
    giorno = oggi.strftime("%d")
    url = f"https://www.vaticannews.va/it/vangelo-del-giorno-e-parola-del-giorno/{anno}/{mese}/{giorno}.speech.js"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
        "Referer": "https://www.vaticannews.va/"
    })
    with urllib.request.urlopen(req, timeout=15) as response:
        raw = response.read().decode("utf-8")
    data = json.loads(raw)
    item = data["speech"][0]
    lettura = item.get("letturaText", "")
    vangelo = item.get("vangeloText", "")
    commento = item.get("hfwText", "")
    return lettura, vangelo, commento, oggi

def pulisci(testo):
    testo = re.sub(r'<br\s*/?>', '\n', testo, flags=re.IGNORECASE)
    testo = re.sub(r'<p[^>]*>', '\n', testo, flags=re.IGNORECASE)
    testo = re.sub(r'</p>', '\n', testo, flags=re.IGNORECASE)
    testo = re.sub(r'<[^>]+>', '', testo)
    testo = html.unescape(testo)
    testo = re.sub(r'\n{3,}', '\n\n', testo)
    return testo.strip()

def a_paragrafi(testo):
    righe = ""
    for riga in testo.split('\n'):
        riga = riga.strip()
        if riga:
            righe += f"<p>{riga}</p>\n"
    return righe

def genera_html(lettura, vangelo, commento, oggi):
    data_str = oggi.strftime("%d/%m/%Y")
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vangelo del {data_str}</title>
</head>
<body>
<h2>Vangelo del {data_str}</h2>
<h3>Prima Lettura e Salmo</h3>
{a_paragrafi(pulisci(lettura))}
<h3>Vangelo</h3>
{a_paragrafi(pulisci(vangelo))}
<h3>Commento</h3>
{a_paragrafi(pulisci(commento))}
</body>
</html>"""

def genera_rss(lettura, vangelo, commento, oggi):
    data_str = oggi.strftime("%d/%m/%Y")
    data_rss = oggi.strftime("%a, %d %b %Y 06:00:00 +0100")
    contenuto = pulisci(lettura) + "\n\n" + pulisci(vangelo) + "\n\n" + pulisci(commento)
    contenuto_escaped = contenuto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Vangelo del Giorno</title>
    <link>https://solumacella.github.io/vangelo-del-giorno/</link>
    <description>Vangelo quotidiano da Vatican News</description>
    <item>
      <title>Vangelo del {data_str}</title>
      <link>https://solumacella.github.io/vangelo-del-giorno/</link>
      <guid>{oggi.strftime("%Y-%m-%d")}</guid>
      <pubDate>{data_rss}</pubDate>
      <description>{contenuto_escaped}</description>
    </item>
  </channel>
</rss>"""

if __name__ == "__main__":
    lettura, vangelo, commento, oggi = fetch_vangelo()
    html_content = genera_html(lettura, vangelo, commento, oggi)
    rss_content = genera_rss(lettura, vangelo, commento, oggi)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_content)
    print(f"Generato: Vangelo del {oggi.strftime('%d/%m/%Y')}")
