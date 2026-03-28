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
    import html
    testo = html.unescape(testo)
    testo = re.sub(r'\n{3,}', '\n\n', testo)
    return testo.strip()

def genera_html(lettura, vangelo, commento, oggi):
    data_str = oggi.strftime("%d/%m/%Y")

    def a_paragrafi(testo):
        righe = ""
        for riga in testo.split('\n'):
            riga = riga.strip()
            if riga:
                righe += f"<p>{riga}</p>\n"
        return righe

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

if __name__ == "__main__":
    lettura, vangelo, commento, oggi = fetch_vangelo()
    html_content = genera_html(lettura, vangelo, commento, oggi)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generato: Vangelo del {oggi.strftime('%d/%m/%Y')}")
