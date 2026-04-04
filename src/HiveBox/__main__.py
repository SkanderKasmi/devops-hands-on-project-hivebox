'''Main entry point for the HiveBox application. Initializes and runs the Flask app.'''
from .app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
    __version__ = "0.1.0"
