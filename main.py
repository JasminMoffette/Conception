import webbrowser
import threading
from app import create_app

app = create_app()


def open_browser():
    """Ouvre automatiquement le navigateur sur l'URL de l'application."""
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
