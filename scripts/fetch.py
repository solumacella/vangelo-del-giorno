import urllib.request
import json
import re
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

    match = re.search(r'var\s+speech\s*=\s*(\[.*?\]);', raw, re.DOTALL)
    if not match:
        raise ValueError("Array speech non trovato nel file JS")

    data = json.loads(match.group(1))

    lettura = ""
    vangelo = ""
    commento = ""

    for item in data:
        if item.get("letturaText"):
            lettura = item["letturaText"]
        if item.get("vangeloText"):
            vangelo = item["vangeloText"]
        if item.get("hfwText"):
            commento = item["hfwText"]

    return lettura, vangelo, commento, oggi

def pulisci(testo):
    testo = re.sub(r'<[^>]+>', ' ', testo)
    testo = re.sub(r'\s+', ' ', testo)
    return testo.strip()

def paragrafi(testo):
    righe = ""
    for frase in testo.split('. '):
        frase = frase.strip()
        if frase:
            righe += f"<p>{frase}.</p>\n"
    return righe

def genera_html(lettura, vangelo, commento, oggi):
    data_str = oggi.strftime("%d/%m/%Y")
    l = pulisci(lettura)
    v = pulisci(vangelo)
    c = pulisci(commento)

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
{paragrafi(l)}
<h3>Vangelo</h3>
{paragrafi(v)}
<h3>Commento</h3>
{paragrafi(c)}
</body>
</html>"""

if __name__ == "__main__":
    lettura, vangelo, commento, oggi = fetch_vangelo()
    html = genera_html(lettura, vangelo, commento, oggi)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generato: Vangelo del {oggi.strftime('%d/%m/%Y')}")
