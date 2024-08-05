import os

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
)


load_dotenv()
app = Flask(__name__)
app.config.from_object(
    {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DATABASE_URI': os.getenv('DATABASE_URI')
    }
)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
