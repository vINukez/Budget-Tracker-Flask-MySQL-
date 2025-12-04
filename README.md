# 💰 Budget Tracker - Flask & MySQL

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Eine moderne Webanwendung zur Verwaltung persönlicher Finanzen**

[Features](#-features) • [Installation](#-installation) • [API](#-rest-api) • [Screenshots](#-screenshots)

</div>

---

## 📋 Über das Projekt

Dieses Projekt ist eine Webanwendung zur Verwaltung persönlicher Ausgaben und wurde im Rahmen des Moduls **Datenbanken und Webentwicklung (DBWE)** an der **ipso Bildung** entwickelt. Die Applikation erfüllt die Vorgaben der Praxisarbeit: eine Flask-Webapplikation mit relationaler Datenbank, Benutzerverwaltung, Geschäftslogik und REST-API.

### 🎯 Projektziele

- Entwicklung einer vollständigen Full-Stack-Webanwendung
- Implementierung eines sicheren Authentifizierungssystems
- Datenvisualisierung mit Chart.js
- RESTful API-Entwicklung
- Modernes, responsives Frontend-Design

---

## ✨ Features

### 🔐 Benutzerverwaltung
- ✅ Registrierung mit eindeutigem Benutzernamen und E-Mail
- ✅ Sicheres Login/Logout-System
- ✅ Passwörter werden mit Werkzeug gehasht und sicher gespeichert
- ✅ Session-basierte Authentifizierung

### 💸 Budget- und Ausgabenverwaltung
- ✅ Erfassen von Ausgaben (Betrag, Kategorie, Datum, Beschreibung)
- ✅ Bearbeiten und Löschen von bestehenden Ausgaben
- ✅ Kategorisierung (Miete, Food, Transport, Freizeit, etc.)
- ✅ Persönliche Ausgabenübersicht pro Benutzer

### 📊 Dashboard mit Visualisierung
- ✅ Moderner Dashboard-Screen nach Login
- ✅ Interaktives Kuchendiagramm (Pie Chart) der Ausgaben nach Kategorie
- ✅ Liniendiagramm für monatlichen Verlauf
- ✅ Echtzeit-Statistiken (Einnahmen, Ausgaben, Saldo)
- ✅ Transaktionsliste mit Icons und Kategorien

### 🌐 REST-API
- ✅ JSON-basierte Endpunkte für externe Zugriffe
- ✅ Authentifizierte API-Anfragen
- ✅ CRUD-Operationen über API
- ✅ Kompatibel mit Tools wie Postman, curl, etc.

---

## 🛠️ Technologie-Stack

### Backend
- **Python 3.9+** - Programmiersprache
- **Flask 3.0.0** - Webframework
- **mysql-connector-python** - MySQL Datenbank-Connector
- **Werkzeug** - Passwort-Hashing und Sicherheit

### Datenbank
- **MySQL 8.0+** - Relationale Datenbank
- Alternativ: **MariaDB** (kompatibel)

### Frontend
- **HTML5 & CSS3** - Modernes, responsives Design
- **Jinja2** - Template-Engine
- **Chart.js** - Datenvisualisierung (via CDN)
- **Inter Font** - Moderne Typografie
- **Glassmorphism & Gradients** - Zeitgemäßes UI-Design

### Deployment
- Entwicklung: `python app.py`
- Produktion: `gunicorn` (optional)

---

## 📁 Projektstruktur

```
Budget-Tracker-Flask-MySQL-/
├── app.py                  # Hauptapplikation (Flask-Routen, Logik)
├── db_config.py           # Datenbankkonfiguration
├── setup_db.py            # Skript zum Erstellen der DB und Tabellen
├── requirements.txt       # Python-Abhängigkeiten
├── templates/             # HTML-Templates (Jinja2)
│   ├── index.html         # Landing Page / Startseite
│   ├── login.html         # Login-Formular
│   ├── register.html      # Registrierungsformular
│   └── dashboard.html     # Dashboard mit Visualisierung
├── static/                # Statische Dateien
│   └── style.css          # CSS-Styling
└── README.md              # Projektdokumentation
```

---

## 🚀 Installation

### Voraussetzungen

Stelle sicher, dass folgende Software installiert ist:

- **Python 3.9 oder höher** ([Download](https://www.python.org/downloads/))
- **MySQL Server 8.0+** ([Download](https://dev.mysql.com/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))

### Schritt 1: Repository klonen

```bash
git clone https://github.com/zerosploit-0/Budget-Tracker-Flask-MySQL-.git
cd Budget-Tracker-Flask-MySQL-
```

### Schritt 2: Virtuelle Umgebung erstellen (empfohlen)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Schritt 3: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Schritt 4: MySQL konfigurieren

Erstelle eine MySQL-Datenbank und passe die Datei `db_config.py` an:

```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="dein_user",
        password="dein_passwort",
        database="budget_tracker"
    )
```

### Schritt 5: Datenbank und Tabellen erstellen

```bash
python setup_db.py
```

Dieses Skript erstellt automatisch:
- Die Datenbank `budget_tracker`
- Tabelle `users` (Benutzerverwaltung)
- Tabelle `transactions` (Ausgaben/Einnahmen)

### Schritt 6: Anwendung starten

```bash
python app.py
```

Die Anwendung läuft nun unter: **http://127.0.0.1:5000**

---

## 🌐 Verwendung

### Weboberfläche

1. **Startseite:** http://127.0.0.1:5000/
2. **Registrierung:** http://127.0.0.1:5000/register
3. **Login:** http://127.0.0.1:5000/login
4. **Dashboard:** http://127.0.0.1:5000/dashboard (nur nach Login)

### Erste Schritte

1. Erstelle ein neues Benutzerkonto über `/register`
2. Logge dich ein mit deinen Credentials
3. Füge deine erste Transaktion im Dashboard hinzu
4. Beobachte die automatische Aktualisierung der Charts

---

## 🔌 REST-API

Die Anwendung bietet eine RESTful API für externen Zugriff auf Daten.

### API-Endpunkte

#### 1. **Registrierung**
```http
POST /api/register
Content-Type: application/json

{
  "username": "max_mustermann",
  "password": "sicheres_passwort"
}
```

**Response:**
```json
{
  "message": "User registered successfully!"
}
```

#### 2. **Login**
```http
POST /api/login
Content-Type: application/json

{
  "username": "max_mustermann",
  "password": "sicheres_passwort"
}
```

**Response:**
```json
{
  "message": "Login successful!"
}
```

#### 3. **Transaktionen abrufen**
```http
GET /api/transactions
Cookie: session=<session_cookie>
```

**Response:**
```json
[
  {
    "id": 1,
    "amount": 50.00,
    "type": "expense",
    "description": "Einkaufen",
    "date": "2024-12-04"
  }
]
```

#### 4. **Transaktion hinzufügen**
```http
POST /api/transactions
Content-Type: application/json
Cookie: session=<session_cookie>

{
  "amount": 100.00,
  "type": "income",
  "description": "Gehalt"
}
```

**Response:**
```json
{
  "message": "Transaction added successfully!"
}
```

### API mit curl testen

```bash
# Registrierung
curl -X POST http://127.0.0.1:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'

# Login
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}' \
  -c cookies.txt

# Transaktionen abrufen
curl -X GET http://127.0.0.1:5000/api/transactions \
  -b cookies.txt
```

---

## 🧪 Tests

### Manuelle Testfälle

| Test | Schritte | Erwartetes Ergebnis | Status |
|------|----------|---------------------|--------|
| **Registrierung** | Neues Konto mit E-Mail anlegen | Benutzer erstellt, Passwort gehasht | ✅ Bestanden |
| **Login** | Mit gültigen Credentials einloggen | Erfolgreicher Login, Weiterleitung | ✅ Bestanden |
| **Fehlerhafter Login** | Falsches Passwort eingeben | Fehlermeldung angezeigt | ✅ Bestanden |
| **Ausgabe erfassen** | Neue Ausgabe mit Daten hinzufügen | Eintrag in DB und UI sichtbar | ✅ Bestanden |
| **Ausgabe löschen** | Bestehende Ausgabe entfernen | Entfernung in DB und UI | ✅ Bestanden |
| **API-Zugriff** | GET /api/transactions | JSON-Response mit Daten | ✅ Bestanden |

**Hinweis:** Alle Tests wurden erfolgreich durchgeführt. Die Webseite ist vollständig getestet und funktionsfähig.

---

## 📸 Screenshots

### Landing Page
![Landing Page](https://github.com/zerosploit-0/Budget-Tracker-Flask-MySQL-/blob/main/Landing-Page.png)

### Login
![Login](https://github.com/zerosploit-0/Budget-Tracker-Flask-MySQL-/blob/main/Login.png)

### Dashboard
![Dashboard](https://github.com/zerosploit-0/Budget-Tracker-Flask-MySQL-/blob/main/Dashboard.png)

*Ersetze die Platzhalter mit echten Screenshots deiner Anwendung*

---

## 🔒 Sicherheit

- ✅ Passwörter werden mit **Werkzeug** gehasht (PBKDF2-SHA256)
- ✅ Session-basierte Authentifizierung mit Secret Key
- ✅ SQL-Injection-Schutz durch Prepared Statements
- ✅ XSS-Schutz durch Jinja2 Auto-Escaping

### Wichtig für Produktion:

```python
# In app.py den Secret Key ändern!
app.secret_key = 'ÄNDERE_DIESEN_SCHLÜSSEL_IN_PRODUKTION'
```

Generiere einen sicheren Key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🐛 Bekannte Probleme & Lösungen

### Problem: MySQL Connection Error

**Lösung:** Stelle sicher, dass der MySQL-Server läuft und die Credentials in `db_config.py` korrekt sind.

```bash
# MySQL-Server starten (Windows)
net start MySQL80

# MySQL-Server starten (macOS/Linux)
sudo systemctl start mysql
```

### Problem: ModuleNotFoundError

**Lösung:** Installiere alle Dependencies:
```bash
pip install -r requirements.txt
```

---

## 📚 Weitere Ressourcen

- [Flask Dokumentation](https://flask.palletsprojects.com/)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)
- [Chart.js Dokumentation](https://www.chartjs.org/docs/latest/)
- [Jinja2 Template Guide](https://jinja.palletsprojects.com/)

---

## 👨‍💻 Autor

**zerosploit-0**
- GitHub: [@zerosploit-0](https://github.com/zerosploit-0)
- Projekt: Budget Tracker Flask & MySQL

---

## 🎓 Projektkontext

**Schule:** ipso Bildung  
**Modul:** Datenbanken und Webentwicklung (DBWE)  
**Typ:** Praxisarbeit  
**Semester:** 2025/2026

Dieses Projekt dient als Praxisarbeit und demonstriert die praktische Anwendung von:
- Webentwicklung mit Flask
- Datenbankdesign und SQL
- REST-API-Entwicklung
- Frontend-Design und UX
- Sicherheitskonzepte in Webanwendungen

---

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) Datei für Details.


<div align="center">

**⭐ Wenn dir dieses Projekt gefällt, gib ihm einen Stern! ⭐**

Made by zerosploit-0

</div>
