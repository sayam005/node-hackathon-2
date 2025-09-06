from flask import Flask
from config import Config

# Initialize the app and tell it where to find templates
app = Flask(__name__, template_folder='blueprints/templates')
app.config.from_object(Config)

# Import and register the main blueprint
from blueprints.main import bp as main_bp
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run()