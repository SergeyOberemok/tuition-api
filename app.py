import os

from dotenv import load_dotenv
from flask import render_template

from src.db import init_db
from src.flask_app_factory import create_flask_app

load_dotenv()

app, socketio = create_flask_app()
app.config['MONGO_URI'] = os.getenv('DB_URI')
init_db(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/image/<int:digit>')
def fetch_image(digit: int):
    return f'{digit}'


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True, allow_unsafe_werkzeug=True)
