 
<p align="center">
  <img src="assets/logo.svg" width="88" alt="Continuum Logo" />
</p>

<h1 align="center">Continuum</h1>

<p align="center"><strong>Dein Workflow. Ohne Unterbrechung.</strong></p>
<p align="center">Linux · Python 3.10+ · Session Management · SSH Synchronization · In Entwicklung</p>

---

## Die Idee

Ich arbeite regelmäßig an verschiedenen Linux-Rechnern und Laptops. Dabei kommt es oft vor, dass ich meine Arbeit an einem Gerät unterbrechen muss und an einem anderen fortsetzen möchte.

Jedes Mal dieselben Programme öffnen, Verzeichnisse wechseln und die vorherige Arbeitsumgebung wiederherstellen – genau das möchte ich mit Continuum vereinfachen.

**Continuum soll ermöglichen, den eigenen Arbeitskontext zu speichern und auf einem anderen Linux-Gerät wieder aufzunehmen.**

Dafür werden ausgewählte Anwendungen, ihre Startargumente und ihre Arbeitsverzeichnisse erfasst und gespeichert.

Das Projekt befindet sich noch in einer frühen Entwicklungsphase.

## Funktionen

### Session Management

- **Save:** Laufende, ausgewählte Programme und ihre Startinformationen speichern.
- **Restore:** Gespeicherte Anwendungen mit ihren bisherigen Startargumenten und Arbeitsverzeichnissen erneut öffnen.
- **List:** Lokal gespeicherte Prozessinformationen anzeigen.
- **Status:** Aktuelle Prozesse und ihren Status untersuchen.
- **Whitelist:** Selbst bestimmen, welche Programme von Continuum berücksichtigt werden.

### SSH Device Management

Continuum unterstützt die Verwaltung mehrerer Linux-Geräte über SSH.

- SSH-Geräte mit Name, Host, Benutzer und Port registrieren.
- Gespeicherte Geräte anzeigen und entfernen.
- Sessions über SCP an konfigurierte Geräte übertragen.
- Beim Speichern einer Session die Übertragung an alle registrierten Geräte anstoßen.

Die SSH-Übertragung setzt voraus, dass die Zielgeräte erreichbar sind und SSH entsprechend eingerichtet ist.

### Geplante Funktionen

- Automatische Wiederherstellung übertragener Sessions.
- Mehrere benannte Sessions.
- Synchronisation über einen eigenen Server.
- Cloud-Synchronisation als optionale Alternative.
- Erweiterte Wiederherstellung von Arbeitsumgebungen.

---

## Installation

### Voraussetzungen

- Linux
- Python 3.10+
- Git
- OpenSSH-Client für SSH/SCP-Übertragungen

Für die aktuelle Python-Implementierung werden keine zusätzlichen Python-Pakete benötigt.

```bash
git clone https://github.com/urimsu/continuum.git
cd continuum
python3 cli.py --help
```

Alternativ kann der [Quellcode als ZIP](https://github.com/urimsu/continuum/archive/refs/heads/main.zip) heruntergeladen werden.

Ein systemweiter `continuum`-Befehl ist geplant.

---

## Verwendung

### Session speichern

Zunächst können Programme zur Whitelist hinzugefügt werden.

```bash
python3 cli.py whitelist add nvim
python3 cli.py whitelist add btop
```

Anschließend lässt sich der aktuelle Arbeitskontext untersuchen und speichern.

```bash
python3 cli.py status
python3 cli.py save
```

Die gespeicherten Programme können angezeigt und erneut gestartet werden.

```bash
python3 cli.py list
python3 cli.py restore
```

### SSH-Geräte hinzufügen

Damit Continuum Sessions an andere Linux-Geräte übertragen kann, müssen diese zunächst registriert werden.

```bash
python3 cli.py ssh new \
  --name macbook \
  --host 192.168.0.27 \
  --user urimsu \
  --port 22
```

Dabei ist `--port` optional und verwendet standardmäßig Port 22.

Registrierte Geräte anzeigen:

```bash
python3 cli.py ssh
```

Ein Gerät entfernen:

```bash
python3 cli.py ssh remove macbook
```

Alternativ kann ein Gerät anhand seiner Host-Adresse entfernt werden.

```bash
python3 cli.py ssh remove 192.168.0.27
```

### Sessions übertragen

Beim Speichern kann Continuum die lokale Session automatisch an alle registrierten SSH-Geräte senden.

```bash
python3 cli.py save
```

Der Ablauf:

1. Laufende Programme werden untersucht.
2. Erlaubte Prozesse werden lokal gespeichert.
3. Continuum liest die konfigurierten SSH-Geräte.
4. Die Session-Datei wird per SCP an erreichbare Geräte übertragen.
5. Das Ergebnis der Übertragungen wird ausgegeben.

Ein nicht erreichbares Gerät verhindert nicht grundsätzlich die Übertragung an andere Geräte.

**Wichtig:** Diese direkte Synchronisation funktioniert nur, wenn die jeweiligen Zielgeräte eingeschaltet und über SSH erreichbar sind.

---

## Konfiguration

Continuum verwendet lokale JSON-Dateien für Sessions und Gerätekonfigurationen.

### Session-Datei

```text
~/.local/state/continuum/processes.json
```

Hier werden die erfassten Prozessinformationen gespeichert.

### SSH-Geräte

```text
~/.config/continuum/devices.json
```

Beispiel:

```json
{
  "devices": [
    {
      "name": "macbook",
      "host": "192.168.0.27",
      "user": "urimsu",
      "port": 22
    },
    {
      "name": "desktop",
      "host": "192.168.0.20",
      "user": "urimsu",
      "port": 22
    }
  ]
}
```

Für die Übertragung verwendet Continuum den systemseitig installierten OpenSSH-Client. SSH-Schlüssel können zur passwortlosen Authentifizierung eingerichtet werden.

---

## Technischer Aufbau

Continuum wird mit Python entwickelt und nutzt überwiegend Funktionen der Standardbibliothek.

- `argparse` für die Kommandozeilenschnittstelle.
- `pathlib` für Dateipfade.
- `json` zur Speicherung der Konfiguration.
- `subprocess` zum Starten von Programmen und für SSH/SCP.
- `/proc` zur Untersuchung laufender Prozesse unter Linux.

Die CLI ist konfigurationsbasiert aufgebaut. Commands, Subcommands und Argumente werden zentral definiert und anschließend generisch registriert.

Die eigentliche Programmlogik bleibt von der CLI getrennt.

---

## Roadmap

- [x] Laufende Prozesse unter Linux erfassen
- [x] Prozessinformationen lokal als JSON speichern
- [x] Whitelist-Verwaltung
- [x] CLI mit Subcommands und Argumenten
- [x] SSH-Geräte registrieren und verwalten
- [x] SCP-Übertragung implementieren
- [ ] SSH-Synchronisation vollständig testen
- [ ] Wiederherstellung auf anderen Linux-Geräten verbessern
- [ ] Mehrere benannte Sessions verwalten
- [ ] Installation als ausführbarer `continuum`-Befehl
- [ ] Self-hosted Synchronisationsserver
- [ ] Optionale Cloud-Synchronisation

---

## Langfristige Vision

Continuum soll verschiedene Möglichkeiten bieten, Arbeitsumgebungen zwischen Linux-Geräten zu übertragen.

**1. Direct SSH**

Die einfachste Variante: Sessions werden direkt zwischen Geräten übertragen. Kein zusätzlicher Server notwendig, solange beide Geräte erreichbar sind.

**2. Self-hosted**

Ein eigener Server speichert mehrere Sessions zentral. Dadurch kann ein Gerät ausgeschaltet werden, während ein anderes später die zuletzt gespeicherte Session abruft.

**3. Cloud**

Eine optionale gehostete Lösung für Nutzer, die keinen eigenen Server betreiben möchten.

Die lokale Nutzung soll weiterhin unabhängig von einem Cloud-Dienst möglich bleiben.

---

## Aktueller Entwicklungsstand

Continuum ist ein experimentelles Open-Source-Projekt.

Die grundlegende Erfassung und Speicherung von Prozessen sowie die SSH-Geräteverwaltung sind implementiert. Die geräteübergreifende Synchronisation und Wiederherstellung werden weiterentwickelt.

Continuum startet Anwendungen anhand gespeicherter Informationen neu. **Es stellt keine vollständigen Prozesszustände, ungespeicherten Dokumente oder den Arbeitsspeicher laufender Anwendungen wieder her.**

---

<p align="center">
  <sub>Gebaut von <a href="https://github.com/urimsu">urimsu</a> · Keep your flow.</sub>
</p>
