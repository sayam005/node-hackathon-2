from flask import render_template, request, redirect, url_for, flash, jsonify
from . import bp
import json
import os
from datetime import datetime

# File to store hisab kitab data
DATA_FILE = 'jethalal_hisab_data.json'

@bp.route('/')
def index():
    """Better Call Jethalal main page with all features"""
    return render_template('better_call_jethalal.html')

@bp.route('/hisab-kitab')
def hisab_kitab():
    """Hisab Kitab dashboard - shows all entries"""
    entries = load_hisab_data()
    
    # Calculate totals
    total_to_pay = sum(entry['amount'] for entry in entries if not entry.get('paid', False))
    total_paid = sum(entry['amount'] for entry in entries if entry.get('paid', False))
    
    return render_template('jethalal_hisab_kitab.html', 
                         entries=entries, 
                         total_to_pay=total_to_pay, 
                         total_paid=total_paid)

@bp.route('/add-entry', methods=['GET', 'POST'])
def add_entry():
    """Add new hisab kitab entry"""
    if request.method == 'POST':
        # Create new entry
        entry = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'person': request.form['person'],
            'amount': float(request.form['amount']),
            'reason': request.form['reason'],
            'due_date': request.form['due_date'],
            'comments': request.form.get('comments', ''),
            'paid': False,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'paid_date': None
        }
        
        # Save entry
        save_hisab_entry(entry)
        flash('नया हिसाब जोड़ दिया गया! Jethalal approved! 🎉', 'success')
        return redirect(url_for('jethalal.hisab_kitab'))
    
    return render_template('jethalal_add_entry.html')

@bp.route('/mark-paid/<entry_id>')
def mark_paid(entry_id):
    """Mark an entry as paid"""
    entries = load_hisab_data()
    
    # Find and update the entry
    for entry in entries:
        if entry['id'] == entry_id:
            entry['paid'] = True
            entry['paid_date'] = datetime.now().strftime('%Y-%m-%d')
            break
    
    # Save updated data
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    flash('पैसा चुका दिया! Jethalal khush! 💰✅', 'success')
    return redirect(url_for('jethalal.hisab_kitab'))

@bp.route('/delete-entry/<entry_id>')
def delete_entry(entry_id):
    """Delete an entry"""
    entries = load_hisab_data()
    
    # Remove the entry
    entries = [entry for entry in entries if entry['id'] != entry_id]
    
    # Save updated data
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    flash('Entry delete हो गया! Jethalal ne clear कर दिया! 🗑️', 'info')
    return redirect(url_for('jethalal.hisab_kitab'))

@bp.route('/calculator')
def calculator():
    """Smart calculator page"""
    return render_template('jethalal_calculator.html')

@bp.route('/calculate', methods=['POST'])
def calculate():
    """API endpoint for calculations"""
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        
        # Basic calculation
        result = eval(expression)  # Note: In production, use a safer eval alternative
        
        return jsonify({
            'success': True,
            'result': result,
            'expression': expression
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@bp.route('/bill-splitter')
def bill_splitter():
    """Bill splitting calculator - Jethalal style"""
    return render_template('jethalal_bill_splitter.html')

@bp.route('/api/split-bill', methods=['POST'])
def api_split_bill():
    """API for bill splitting with Indian jugaad features"""
    try:
        data = request.get_json()
        total_amount = float(data.get('total_amount', 0))
        people_count = int(data.get('people_count', 1))
        tip_percentage = float(data.get('tip_percentage', 0))
        rounding_option = data.get('rounding_option', '5')  # Round to nearest 5 or 10
        
        # Calculate tip and total
        tip_amount = total_amount * (tip_percentage / 100)
        total_with_tip = total_amount + tip_amount
        
        # Basic per person amount
        per_person_exact = total_with_tip / people_count
        
        # Indian Jugaad - Smart Rounding
        rounding_value = int(rounding_option)
        per_person_rounded = round(per_person_exact / rounding_value) * rounding_value
        
        # Calculate totals after rounding
        total_after_rounding = per_person_rounded * people_count
        extra_amount = total_after_rounding - total_with_tip
        
        # Who pays extra logic
        if extra_amount > 0:
            who_pays_extra = "पहले वाला भाई"
            extra_per_person = per_person_rounded + extra_amount
        else:
            who_pays_extra = "कोई नहीं"
            extra_per_person = per_person_rounded
        
        return jsonify({
            'success': True,
            'original_amount': total_amount,
            'tip_percentage': tip_percentage,
            'tip_amount': round(tip_amount, 2),
            'total_with_tip': round(total_with_tip, 2),
            'people_count': people_count,
            'per_person_exact': round(per_person_exact, 2),
            'per_person_rounded': per_person_rounded,
            'total_after_rounding': total_after_rounding,
            'extra_amount': round(extra_amount, 2),
            'who_pays_extra': who_pays_extra,
            'extra_per_person': extra_per_person
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Helper functions
def load_hisab_data():
    """Load hisab kitab data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_hisab_entry(entry):
    """Save new hisab kitab entry"""
    entries = load_hisab_data()
    entries.append(entry)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
