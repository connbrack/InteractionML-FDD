from flask import Flask, send_from_directory
import random
from routes import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)