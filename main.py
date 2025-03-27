
import webbrowser
import threading
from app import create_app

app = create_app()


def open_browser():
    """Ouvre automatiquement le navigateur sur l'URL de l'application."""
    webbrowser.open_new("http://0.0.0.0:5001/")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(host="0.0.0.0", port=5001, debug=True)

