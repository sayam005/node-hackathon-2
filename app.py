from flask import Flask
from config import Config

# Initialize the app and tell it where to find templates
app = Flask(__name__, template_folder='blueprints/templates')
app.config.from_object(Config)

# Import and register blueprints
from blueprints.main.routes import bp as main_bp
from blueprints.good_morning_pineapple.routes import bp as good_morning_bp
from blueprints.better_call_jethalal.routes import bp as jethalal_bp
from blueprints.mummy_I_want_pizza_at_home.routes import bp as mummy_pizza_bp

app.register_blueprint(main_bp)
app.register_blueprint(good_morning_bp)
app.register_blueprint(jethalal_bp)
app.register_blueprint(mummy_pizza_bp)

if __name__ == '__main__':
    app.run(debug=True)