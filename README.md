# FlaskApp / Note App

## Überblick
Diese Webanwendung ermöglicht es Benutzern, sich zu registrieren, anzumelden und Notizen zu erstellen und zu löschen.  
Die App basiert auf Flask (Python) und MySQL und verfügt über eine einfache Benutzeroberfläche.  

---

## Features
- Benutzerverwaltung (Registrierung, Login, Logout)  
- Notizen erstellen und löschen  
- Maximale Benutzeranzahl: 6
- Account-Sperre nach 3 falschen Login-Versuchen (24 Stunden Sperre) 
- RESTful API für Notizenverwaltung (GET, POST, DELETE)  

---

## Installation & Einrichtung

### 1. Projekt klonen und virtuelle Umgebung erstellen

git clone https://github.com/username/yourrepo.git
cd yourrepo
python3 -m venv venv

source venv/bin/activate  # Mac/Linux
venv\Scriptsctivate  # Windows

### 2. Abhängigkeiten installieren

pip install -r requirements.txt

### 3. Datenbank einrichten
# Die Zugangsdaten für die Datenbank wurden entfernt. Deshalb muss diese manuell erstellt werden.
Falls du MySQL verwendest, erstelle zuerst eine Datenbank:
CREATE DATABASE flaskapp_db;

Dann führe die Migrationen aus:

flask db migrate -m "Initial setup"
flask db upgrade


### 4. App im Entwicklungsmodus starten

#python main.py

Die App läuft dann unter:
**http://127.0.0.1:5000**
