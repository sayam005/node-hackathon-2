from flask import Blueprint, render_template, request

# define blueprint here (routes module owns the blueprint)
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/good-morning-pineapple')
def good_morning_pineapple():
    return render_template('good_morning_pineapple.html')

@bp.route('/mummy-i-want-pizza-at-home')
def mummy_i_want_pizza_at_home():
    return render_template('mummy_i_want_pizza_at_home.html')

@bp.route('/papa-ki-unpaid-internship')
def papa_ki_unpaid_internship():
    return render_template('papa_ki_unpaid_internship.html')

@bp.route('/better-call-jethalal')
def better_call_jethalal():
    # Redirect to the jethalal blueprint
    from flask import redirect, url_for
    return redirect(url_for('jethalal.index'))