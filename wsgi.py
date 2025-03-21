from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

# Hierdurch kann Gunicorn app als WSGI-Anwendung verwenden
# Jetzt kann mit cmd: gunicorn --bind 0.0.0.0:8000 "wsgi:app" app gestartet werden (falls Addresse nicht "already in use" ist)
