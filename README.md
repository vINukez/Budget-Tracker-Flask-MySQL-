# Budget Tracker – Flask & MySQL

Dieses Projekt ist eine Webanwendung zur Verwaltung persönlicher Ausgaben.  
Es wurde im Rahmen des Moduls **Datenbanken und Webentwicklung (DBWE)** an der ipso Bildung entwickelt und erfüllt die Vorgaben der Praxisarbeit: eine Flask-Webapplikation mit relationaler Datenbank, Benutzerverwaltung, Geschäftslogik und REST-API.

---

## Funktionsübersicht

Die Applikation bietet folgende Hauptfunktionen:

- **Benutzerverwaltung**
  - Registrierung mit eindeutigem Benutzernamen, E-Mail-Adresse und Passwort
  - Login / Logout
  - Passwörter werden sicher gehasht in der Datenbank gespeichert

- **Budget- und Ausgabenverwaltung**
  - Erfassen von Ausgaben (Betrag, Kategorie, Datum, Beschreibung)
  - Bearbeiten und Löschen von bestehenden Ausgaben
  - Kategorisierung (z. B. Miete, Food, Transport, Freizeit usw.)
  - Übersicht der Ausgaben pro Benutzer

- **Dashboard mit Visualisierung**
  - Moderner Dashboard-Screen nach Login
  - **Kuchendiagramm (Pie Chart)** der Ausgaben nach Kategorie
  - Zusammenfassung der Gesamtausgaben

- **REST-API (lesender Zugriff)**
  - Bereitstellung ausgewählter Daten als JSON über einen REST-Endpunkt
  - Zugriff mit gängigem HTTP-Client (z. B. `curl`, Postman) ohne Browser
  - Authentifizierung über Benutzer-Login (Session / Token, je nach Implementierung im Code)

---

## Technologiestack

- **Backend**
  - Python 3.x
  - Flask (Webframework)
  - `mysql-connector-python` für den Zugriff auf MySQL

- **Datenbank**
  - MySQL (oder kompatibel, z. B. MariaDB)

- **Frontend**
  - HTML Templates mit Jinja2 (Flask Templates)
  - CSS (modernes, helles Design mit Weiss/Blau)
  - Optional: Bootstrap-Klassen für responsives Layout
  - Chart.js (über CDN) zur Darstellung des Pie Charts im Dashboard

- **Deployment**
  - Entwicklung: Start via `python app.py`
  - Produktion (optional): Start via `gunicorn` möglich

---

## Projektstruktur

Die wichtigsten Dateien und Ordner:

```bash
Budget-Tracker-Flask-MySQL-/
├─ app.py               # Hauptapplikation (Flask-Routen, Logik)
├─ db_config.py         # Datenbankkonfiguration (Host, User, Passwort, DB-Name)
├─ setup_db.py          # Skript zum Erstellen der Datenbank und Tabellen
├─ requirements.txt    # Ältere/Platzhalter-Version der Requirements (optional ersetzen)
├─ templates/           # HTML-Templates (Jinja2)
│  ├─ index.html        # Landing Page / Startseite
│  ├─ login.html        # Login-Formular
│  ├─ register.html     # Registrierungsformular
│  └─ dashboard.html    # Dashboard mit Ausgabenübersicht & Pie Chart
```

**Installation und Setup**

1. Voraussetzungen

Python ab Version 3.9

MySQL-Server (lokal oder extern erreichbar)

Ein Benutzer in MySQL mit Rechten zum Erstellen von Datenbanken und Tabellen


** 2. Repository klonen**

git clone https://github.com/zerosploit-0/Budget-Tracker-Flask-MySQL-.git
cd Budget-Tracker-Flask-MySQL-

**3. Virtuelle Umgebung (empfohlen)**

python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

**4. Abhängigkeiten installieren**

pip install -r requirements.txt


**5. MySQL konfigurieren**

Passe in der Datei db_config.py die Zugangsdaten an deine Umgebung an, zum Beispiel:

db_config = {
    "host": "localhost",
    "user": "dein_user",
    "password": "dein_passwort",
    "database": "budget_tracker"
}

**6. Datenbank und Tabellen erstellen**

Starte das Setup-Skript, um die Datenbank und die benötigten Tabellen zu erstellen:

python setup_db.py


**7. Anwendung starten (Entwicklung)**

python app.py


Standardmässig läuft Flask dann unter:

http://127.0.0.1:5000

Rufe im Browser zum Beispiel folgende Seiten auf:

http://127.0.0.1:5000/ – Startseite

http://127.0.0.1:5000/register – Registrierung

http://127.0.0.1:5000/login – Login

http://127.0.0.1:5000/dashboard – Dashboard (nur nach Login)

**REST-API**
**
Zusätzlich zur Weboberfläche stellt die Anwendung einen REST-Endpunkt bereit, über den auf ausgewählte Daten lesend zugegriffen werden kann (gemäss Aufgabenstellung).

Ein typischer Endpunkt könnte z. B. so aussehen (abhängig von der finalen Implementierung in app.py):

GET /api/expenses


Antwort: JSON-Liste der Ausgaben des aktuell angemeldeten Benutzers

Nutzung: z. B. mit curl oder Postman

Authentifizierung: über die Session bzw. das im Code implementierte Authentifizierungsverfahren

Beispielaufruf mit curl (nachdem ein Login im Browser erfolgt ist und die Session-Cookies vorhanden sind):

curl -X GET http://127.0.0.1:5000/api/expenses

Tests (manuelle Testfälle – Überblick)

# Für die Praxisarbeit können folgende manuelle Tests dokumentiert werden:

**Registrierung**

Schritte: Neues Benutzerkonto mit noch nicht verwendeter E-Mail anlegen.

Erwartung: Benutzer wird erstellt, Passwort gehasht gespeichert, Weiterleitung zum Login.

**Login**

Schritte: Mit gültigen Credentials einloggen.

Erwartung: Erfolgreicher Login, Weiterleitung zum Dashboard.

**Fehlgeschlagener Login**

Schritte: Mit falschem Passwort versuchen, sich anzumelden.

Erwartung: Fehlermeldung, kein Login.

**Ausgabe erfassen**

Schritte: Im Dashboard eine neue Ausgabe mit Betrag, Kategorie und Datum erfassen.

Erwartung: Eintrag wird gespeichert und erscheint in der Tabelle sowie im Pie Chart.

**Ausgabe löschen/bearbeiten**

Schritte: Bestehende Ausgabe entfernen oder ändern.

Erwartung: Änderung ist in Datenbank und UI sichtbar.

# REST-API

Schritte: API-Endpunkt mit HTTP-Client aufrufen.

Erwartung: JSON-Ausgabe mit den erwarteten Daten.

Diese Tests wurden ausgeführt. Auf ein Testprotokoll wurde verzichtet, da die Webseite vollständig getestet wurde


# Autor

**Student:** zerosploit-0 (GitHub)

**Modul:** Datenbanken und Webentwicklung (DBWE)

**Schule:** ipso Bildung

Dieses Projekt dient als Praxisarbeit und als Grundlage, um Konzepte wie Webentwicklung mit Flask, Datenbankdesign und API-Integration praktisch anzuwenden.