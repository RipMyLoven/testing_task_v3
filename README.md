# Todo List Rakendus

Lihtne todo list veebirakendus, mis kasutab Python Flask-i backend-ina ja HTML/CSS/JavaScript-i frontend-ina.

## Funktsioonid

- **Kasutaja autentimine**: Registreerimine ja sisselogimine
- **Todo ülesanded**: Ülesannete lisamine, vaatamine, muutmine ja kustutamine
- **Prioriteedid**: Madal, keskmine, kõrge prioriteet
- **Tähtaeg**: Ülesannetele saab määrata tähtaja
- **Parooli muutmine**: Sisselogitud kasutajad saavad oma parooli muuta
- **Eraldi kasutajad**: Iga kasutaja näeb ainult oma ülesandeid

## Paigaldamine ja käivitamine

1. **Paigalda Python sõltuvused:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Käivita rakendus:**
   ```bash
   python app.py
   ```

3. **Ava brauseris:**
   ```
   http://localhost:5000
   ```

## Andmebaas

Rakendus kasutab SQLite andmebaasi (`todo.db`), mis luuakse automaatselt esimesel käivitamisel.

## Struktuur

- `app.py` - Python Flask backend
- `templates/index.html` - HTML fail JavaScript-iga
- `static/style.css` - CSS stiilid
- `requirements.txt` - Python sõltuvused

## Turvalisus

- Paroolid on krüpteeritud (Werkzeug hash)
- Kasutajad näevad ainult oma ülesandeid
- XSS kaitse HTML-i sisendi puhul