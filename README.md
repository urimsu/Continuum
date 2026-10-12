<p align="center">
  <img src="assets/logo.svg" width="88" alt="Continuum Logo" />
</p>

<h1 align="center">Continuum</h1>

<p align="center"><strong>Dein Workflow. Ohne Unterbrechung.</strong></p>
<p align="center">Linux · Python 3.10+ · Lokale Sessions · In Entwicklung</p>

---

Continuum hält deinen Arbeitskontext fest: ausgewählte Anwendungen, ihre Startargumente und ihr Arbeitsverzeichnis. Starte sie später wieder dort, wo du aufgehört hast — direkt aus dem Terminal.

- **Speichern:** Prozessinformationen lokal als JSON ablegen.
- **Wieder starten:** Anwendungen mit ihrem bisherigen Aufruf und Verzeichnis öffnen.
- **Selbst bestimmen:** Mit einer Whitelist auswählen, welche Programme dazugehören.

## Herunterladen & starten

Du brauchst **Linux**, **Python 3.10+** und **Git**. Keine zusätzlichen Python-Pakete, kein Build-Schritt.

```bash
git clone https://github.com/urimsu/continuum.git
cd continuum
python3 cli.py --help
```

Alternativ: [Quellcode als ZIP herunterladen](https://github.com/urimsu/continuum/archive/refs/heads/main.zip) und entpacken.

## Dein erster Workflow

```bash
# Programme auswählen
python3 cli.py whitelist add nvim
python3 cli.py whitelist add btop

# Kontext ansehen und speichern
python3 cli.py status
python3 cli.py save

# Gespeicherte Programme ansehen und neu starten
python3 cli.py list
python3 cli.py restore
```

> **Prototyp:** Im aktuellen lokalen Stand benötigt `save` noch eine Korrektur: In `commands.py` muss der Aufruf innerhalb von `save()` auf `config.whitelist.get_allowed_programs()` geändert werden. Terminal-Starts sind noch in Arbeit. Continuum startet Programme neu; ungespeicherte Inhalte und vollständige Prozesszustände werden nicht wiederhergestellt.

<p align="center"><sub>Gebaut von <a href="https://github.com/urimsu">urimsu</a> · Keep your flow.</sub></p>
