from flask import Flask
from config import Config

# Initialize the app and tell it where to find templates
app = Flask(__name__, template_folder='blueprints/templates')
app.config.from_object(Config)

# Import and register the main blueprint directly from routes (no code in __init__.py)
from blueprints.main.routes import bp as main_bp
app.register_blueprint(main_bp)

# Import and register the jethalal blueprint
from blueprints.jethalal.routes import bp as jethalal_bp
app.register_blueprint(jethalal_bp)

if __name__ == '__main__':
    app.run(debug=True)