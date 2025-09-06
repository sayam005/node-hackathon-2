from flask import Blueprint, render_template, request, jsonify
import requests
import random
import os

# define blueprint here (routes module owns the blueprint)
bp = Blueprint('main', __name__)

# WhatsApp family group style quotes
FAMILY_QUOTES = [
    "🌅 Good Morning! Life is like a cup of tea... it's all about how you make it! ☕✨",
    "🌞 Rise and shine! Remember: You're never too old to set new goals! 💪🎯",
    "🌸 Good Morning dear! May your coffee be strong and your Monday be short! ☕😊",
    "🌺 A beautiful day begins with a beautiful mindset! Think positive! 🌈💭",
    "🌻 Good Morning! Don't count the days, make the days count! 📅✨",
    "🌹 Every morning is a fresh start! Yesterday is history, tomorrow is mystery! 🔮⏰",
    "🌷 Good Morning! Life is 10% what happens to you and 90% how you react! 😄💯",
    "🌼 Smile! It's the key that fits the lock of everybody's heart! 😊💝",
    "🌺 Today is a gift, that's why it's called the present! 🎁✨"
]

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/good-morning-pineapple')
def good_morning_pineapple():
    return render_template('good_morning_pineapple.html')

@bp.route('/api/generate-wish')
def generate_wish():
    # Get a random quote
    quote = random.choice(FAMILY_QUOTES)
    
    # Get a random image from Unsplash (nature/motivational)
    try:
        unsplash_response = requests.get(
            "https://source.unsplash.com/600x400/?nature,sunrise,flowers,motivation",
            timeout=5
        )
        image_url = unsplash_response.url
    except:
        image_url = "https://via.placeholder.com/600x400/ff6b6b/ffffff?text=Beautiful+Morning+Image"
    
    return jsonify({
        'quote': quote,
        'image_url': image_url,
        'status': 'success'
    })

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