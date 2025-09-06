from flask import render_template, request, jsonify, Blueprint
import random
import urllib.parse

# CREATE BLUEPRINT with correct name
bp = Blueprint('papa_ki_unpaid_internship', __name__, url_prefix='/papa-ki-unpaid-internship')

@bp.route('/')
def index():
    """Papa Ki Unpaid Internship main page - DIY tutorial hub"""
    return render_template('papa_ki_unpaid_internship.html')

# ============= TASK GENERATOR ROUTES =============
@bp.route('/task-generator')
def task_generator():
    """Generate funny tasks for kids and family"""
    return render_template('papa_task_generator.html')

@bp.route('/api/generate-task', methods=['POST'])
def api_generate_task():
    """API to generate a random funny task"""
    try:
        data = request.get_json()
        category = data.get('category', 'all')
        difficulty = data.get('difficulty', 'medium')
        
        task = generate_funny_task(category, difficulty)
        papa_comment = get_papa_comment(task)
        
        return jsonify({
            'success': True,
            'task': task,
            'papa_comment': papa_comment,
            'category': category,
            'difficulty': difficulty
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Papa busy हैं: {str(e)}'
        })

@bp.route('/api/task-categories')
def api_task_categories():
    """Get available task categories"""
    categories = [
        {'id': 'cleaning', 'name': '🧹 सफाई के काम', 'description': 'घर की सफाई के tasks'},
        {'id': 'kitchen', 'name': '🍳 रसोई के काम', 'description': 'खाना बनाने में मदद'},
        {'id': 'organization', 'name': '📦 व्यवस्था के काम', 'description': 'चीजों को व्यवस्थित करना'},
        {'id': 'garden', 'name': '🌱 बागवानी', 'description': 'पौधों की देखभाल'},
        {'id': 'maintenance', 'name': '🔧 छोटी मरम्मत', 'description': 'घर की छोटी-मोटी मरम्मत'},
        {'id': 'creative', 'name': '🎨 रचनात्मक काम', 'description': 'DIY projects और art'},
        {'id': 'all', 'name': '🎲 सभी प्रकार', 'description': 'किसी भी category का task'}
    ]
    
    return jsonify({'categories': categories})

# ============= PROBLEM SOLVER ROUTES =============
@bp.route('/problem-solver')
def problem_solver():
    """Papa's problem solving hub"""
    return render_template('papa_problem_solver.html')

@bp.route('/api/solve-problem', methods=['POST'])
def api_solve_problem():
    """API to get solutions for household problems"""
    try:
        data = request.get_json()
        problem = data.get('problem', '').strip()
        urgency = data.get('urgency', 'normal')  # emergency, normal, can-wait
        category = data.get('category', 'general')  # electrical, plumbing, tech, etc.
        
        if not problem:
            return jsonify({
                'success': False,
                'error': 'Problem तो बताओ भाई! Papa कैसे help करेंगे?'
            })
        
        # Get solutions
        solutions = get_problem_solutions(problem, urgency)
        papa_advice = get_papa_problem_advice(problem)
        youtube_links = search_tutorial_videos(problem)
        
        return jsonify({
            'success': True,
            'problem': problem,
            'urgency': urgency,
            'category': detect_problem_category(problem),
            'solutions': solutions,
            'papa_advice': papa_advice,
            'youtube_tutorials': youtube_links,
            'estimated_time': estimate_fix_time(problem),
            'difficulty': estimate_difficulty(problem),
            'tools_needed': get_required_tools(problem)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Papa के pass solution नहीं मिला: {str(e)}'
        })

@bp.route('/api/common-problems')
def api_common_problems():
    """Get list of common household problems"""
    problems = [
        {'problem': '🌀 Fan नहीं चल रहा है', 'category': 'electrical', 'urgency': 'normal', 'popularity': 'बहुत common'},
        {'problem': '🚿 Tap से पानी leak हो रहा है', 'category': 'plumbing', 'urgency': 'high', 'popularity': 'Daily होता है'},
        {'problem': '📱 WiFi बहुत slow है', 'category': 'tech', 'urgency': 'normal', 'popularity': 'हमेशा problem'},
        {'problem': '❄️ AC ठंडा नहीं कर रहा', 'category': 'appliances', 'urgency': 'high', 'popularity': 'Summer special'},
        {'problem': '🚪 Door properly बंद नहीं हो रहा', 'category': 'general', 'urgency': 'low', 'popularity': 'Monsoon में ज्यादा'},
        {'problem': '🪑 Chair टूट गई है', 'category': 'furniture', 'urgency': 'low', 'popularity': 'Overuse से होता है'},
        {'problem': '💡 Light नहीं जल रही', 'category': 'electrical', 'urgency': 'normal', 'popularity': 'रोज़ का drama'},
        {'problem': '📺 TV remote काम नहीं कर रहा', 'category': 'tech', 'urgency': 'low', 'popularity': 'बच्चों की वजह से'},
        {'problem': '🚽 Toilet flush नहीं हो रहा', 'category': 'plumbing', 'urgency': 'high', 'popularity': 'Common issue'},
        {'problem': '🔌 Socket में plug loose हो गया', 'category': 'electrical', 'urgency': 'medium', 'popularity': 'Safety concern'}
    ]
    
    return jsonify({'common_problems': problems})

# ============= TASK GENERATOR HELPER FUNCTIONS =============
def generate_funny_task(category, difficulty):
    """Generate funny and engaging household tasks"""
    
    tasks_db = {
        'cleaning': [
            '🧹 आज सभी कोनों से spider webs हटाओ - detective बनकर हर spider को ढूंढो!',
            '🧽 Bathroom की tiles पर से soap के निशान हटाओ और shine करके mirror बनाओ',
            '🧺 अपने कमरे के सभी कपड़े organized करके color wise arrange करो',
            '🪟 सभी windows clean करके streak-free shine लाओ',
            '💨 सभी fans की dust हटाओ और blade count करके report दो',
            '🗑️ घर के सभी dustbins empty करके proper segregation करो'
        ],
        'kitchen': [
            '🍳 आज breakfast में कुछ creative बनाओ - leftover ingredients use करके',
            '🧄 Kitchen के सभी masala containers organize करके label लगाओ',
            '🍽️ सभी dishes wash करके perfect shine लाओ',
            '❄️ Fridge clean करके expiry dates check करो',
            '🧊 Ice trays fill करके freezer organize करो',
            '🍅 सभी vegetables fresh रखने के लिए proper storage करो'
        ],
        'organization': [
            '📚 सभी books को height wise arrange करके library बनाओ',
            '👕 Wardrobe को season wise organize करो',
            '📦 Store room clean करके सब कुछ categorize करो',
            '🎮 सभी electronic items के chargers और cables organize करो',
            '💄 Dressing table पर सब कुछ neat और accessible arrange करो',
            '📱 Phone gallery clean करके photos organize करो'
        ],
        'garden': [
            '🌱 सभी plants को पानी दो और soil moisture check करो',
            '🍃 Dead leaves हटाओ और plants की health check करो',
            '🌺 Flower pots rearrange करके सबसे अच्छा display बनाओ',
            '🐛 Plants पर कोई pests तो नहीं - inspection करके report दो',
            '💧 Watering schedule बनाओ और proper drainage check करो',
            '🌿 New plants के लिए suitable locations identify करो'
        ],
        'maintenance': [
            '🔧 घर के सभी loose screws tight करो',
            '🚪 सभी door handles और locks की functioning check करो',
            '💡 सभी bulbs working हैं कि नहीं test करो',
            '🔌 सभी electrical connections check करके loose plugs fix करो',
            '🪟 Windows के hinges में oil लगाओ',
            '🚿 Taps की leakage check करके minor fixes करो'
        ],
        'creative': [
            '🎨 Waste materials use करके कोई useful item बनाओ',
            '📸 घर की सबसे अच्छी photos लेकर wall gallery बनाओ',
            '✂️ Old newspapers से decorative items बनाओ',
            '🖼️ Room को rearrange करके नया look दो',
            '💡 Energy saving के लिए कोई creative solution सोचो',
            '🎭 Family के लिए कोई fun activity organize करो'
        ]
    }
    
    # Select appropriate task pool
    if category == 'all':
        all_tasks = []
        for task_list in tasks_db.values():
            all_tasks.extend(task_list)
        selected_pool = all_tasks
    else:
        selected_pool = tasks_db.get(category, tasks_db['cleaning'])
    
    # Pick random task
    task = random.choice(selected_pool)
    
    # Add difficulty-based modifications
    if difficulty == 'easy':
        task += ' (आराम से करना, जल्दी नहीं है)'
    elif difficulty == 'hard':
        task += ' (जल्दी complete करके time record करना!)'
    
    return task

def get_papa_comment(task):
    """Get Papa's encouraging comment for the task"""
    
    comments = [
        'Wah beta! Ye task perfect है आज के लिए. Papa proud होंगे! 👏',
        'Shabash! Iss task से घर और भी beautiful हो जाएगा! ✨',
        'Good choice! Papa के जमाने में यही सब tasks करके हमने सब kuch सीखा था! 💪',
        'Excellent! Task complete करने के बाद treat mileगी! 🍫',
        'Perfect timing! Ye task करने से बहुत satisfaction मिलेगा! 😊',
        'Bahut achha! Mummy बहुत खुश होंगी जब देखेंगी! 🥰',
        'Smart choice! Aise small tasks से big difference होता है! 🌟',
        'Very good! Sunday को productive बनाने का बेहतरीन तरीका! 👍'
    ]
    
    return random.choice(comments)

# ============= PROBLEM SOLVER HELPER FUNCTIONS =============

def get_problem_solutions(problem, urgency):
    """Get comprehensive step-by-step solutions"""
    
    solutions_db = {
        'fan': {
            'quick_check': [
                '⚡ Main switch on है कि नहीं check करो',
                '🔌 Fan का regulator properly connected है?',
                '💡 दूसरे electrical items काम कर रहे हैं?',
                '🌀 Fan के blades manually घुमाने से चलता है?'
            ],
            'diy_steps': [
                '🔧 Main switch off करके safety ensure करो',
                '🧽 Fan blades को clean करो - dust accumulation check करो', 
                '🔨 All screws और brackets properly tight हैं कि नहीं',
                '⚙️ Capacitor check करो - bulged या burnt smell?',
                '💧 Motor bearings में oil drop करने की जरूरत हो सकती है',
                '🔄 Regulator को different speeds पर test करो'
            ],
            'safety_tips': [
                '⚠️ हमेशा main switch off करके काम करो',
                '🧤 Rubber gloves पहनो electrical work के लिए',
                '🔦 Good lighting में काम करो',
                '👥 Someone को inform करके काम करो'
            ],
            'when_to_call_expert': 'अगर capacitor burnt smell आ रही है या motor से grinding sound आ रहा है या rewiring की जरूरत है'
        },
        'tap': {
            'quick_check': [
                '🚰 Main water supply on है कि नहीं',
                '💧 दूसरे taps से पानी आ रहा है कि नहीं',
                '🔧 Tap handle properly turn हो रहा है?',
                '👀 Visible leak कहाँ से हो रहा है - handle से या base से?'
            ],
            'diy_steps': [
                '🔧 Main water valve बंद करो पहले (very important)',
                '🪛 Tap का handle remove करके rubber washer check करो',
                '🧽 Valve seat को clean करो - sediment हटाओ',
                '🔄 नया washer लगाकर proper तरीके से reassemble करो',
                '💧 Slowly water supply on करके test करो',
                '🔍 कोई leak तो नहीं - thorough check करो'
            ],
            'safety_tips': [
                '💧 Main valve बंद करना बिल्कुल मत भूलो',
                '🧽 Clean cloth से area को dry रखो',
                '🔧 Right size tools use करो - force नहीं लगाओ'
            ],
            'when_to_call_expert': 'अगर main pipe में leak है या pressure issues हैं या multiple taps affected हैं'
        },
        'wifi': {
            'quick_check': [
                '📱 Phone में दूसरे WiFi networks दिख रहे हैं?',
                '🔌 Router का power properly connected है?',
                '💡 Router के lights green हैं कि नहीं?',
                '📶 Router के पास जाकर speed test करो'
            ],
            'diy_steps': [
                '🔄 Router को 30 seconds off करके फिर on करो',
                '📍 Router की position central और elevated रखो',
                '📱 Phone को WiFi forget करके फिर reconnect करो',
                '💻 Speed test different devices पर करो',
                '🌐 ISP के customer care में speed complaint करो',
                '📡 Router antennas को properly position करो'
            ],
            'safety_tips': [
                '⚡ Router को properly ventilated area में रखो',
                '🌡️ Overheating से बचाओ - dust clean करते रहो'
            ],
            'when_to_call_expert': 'अगर hardware damage है या ISP line issue है या multiple devices से कोई connect नहीं हो रहा'
        },
        'ac': {
            'quick_check': [
                '⚡ AC का power on है और display working है?',
                '🌡️ Remote में सही temperature set है?',
                '💨 AC से air आ रहा है लेकिन ठंडी नहीं?',
                '🧊 Ice formation तो नहीं outdoor unit पर?'
            ],
            'diy_steps': [
                '🧽 Indoor filter को remove करके clean करो',
                '💨 Outdoor unit के around clean करो - leaves हटाओ',
                '🌡️ Thermostat setting check करो',
                '⏰ AC को 30 minutes run करके देखो',
                '📏 Proper distance maintain करो furniture से',
                '🚪 Room properly sealed है - doors/windows check करो'
            ],
            'safety_tips': [
                '⚡ Main power off करके filter cleaning करो',
                '🧤 Gloves पहनकर outdoor unit clean करो'
            ],
            'when_to_call_expert': 'अगर gas refill की जरूरत है या compressor issues हैं या electrical problems हैं'
        }
    }
    
    # Detect problem type and return relevant solution
    problem_lower = problem.lower()
    
    for key, solution in solutions_db.items():
        if key in problem_lower:
            return solution
    
    # Generic solution for unknown problems
    return {
        'quick_check': [
            '🔍 Problem को exactly identify करने की कोशिश करो',
            '📖 Manual या warranty card check करो',
            '🔌 Power supply और connections verify करो',
            '👀 Visual inspection करो - कुछ obvious damage?'
        ],
        'diy_steps': [
            '📖 Product manual पढ़ो अगर available है',
            '🎥 YouTube पर similar problem search करो',
            '🔧 Basic cleaning और tightening try करो',
            '📞 Manufacturer helpline पर call करो',
            '💬 Online forums में similar cases ढूंढो'
        ],
        'safety_tips': [
            '⚠️ अगर electrical item है तो power off करो',
            '🧤 Safety gear use करो',
            '👥 किसी को inform करके काम करो'
        ],
        'when_to_call_expert': 'अगर safety concern है या warranty void हो सकती है या complex repair चाहिए'
    }

def get_papa_problem_advice(problem):
    """Papa's specific wisdom for different problems"""
    
    advice_db = {
        'fan': 'बेटा, fan की 90% problems capacitor या dust में होती हैं। गर्मी में fan repair करना बहुत जरूरी है। Safety के लिए हमेशा main switch off रखो। Capacitor ₹50 का है, electrician ₹500 लेता है!',
        'tap': 'Tap leakage mostly rubber washer (₹5) की वजह से होती है। Main valve location पहले से पता कर लो, emergency में काम आएगा। पानी बंद करना बिल्कुल मत भूलो - flooding हो सकती है!',
        'wifi': 'WiFi problems में 80% router restart से solve हो जाती हैं। Router को corner में मत रखो, heat और dust से बचाओ। Speed slow है तो ISP को complaint करना पड़ेगा, data backup रखो।',
        'ac': 'AC की filter monthly clean करते रहो, gas filling से बच जाएगी। Summer शुरू होने से पहले service करवा लो. Emergency में fan + AC together chalao, jaldi ठंडक मिलेगी।',
        'door': 'Door problems में WD-40 या coconut oil magic करता है. Monsoon में wood swelling होती है, normal है। Hinges की proper lubrication करते रहो।',
        'light': 'Light problems में पहले bulb change करके देखो। Switch और holder loose तो नहीं? Electrical items में हमेशा right wattage use करो।'
    }
    
    problem_lower = problem.lower()
    
    for key, advice in advice_db.items():
        if key in problem_lower:
            return advice
    
    return 'बेटा, हर problem का solution होता है। Google और YouTube Papa के बाद सबसे अच्छे teachers हैं। Safety first, patience second, और जब doubt हो तो expert से पूछ लो। DIY में 70% problems solve हो जाती हैं!'

def search_tutorial_videos(problem):
    """Generate YouTube tutorial links for the problem"""
    
    # Enhanced search queries for better results
    search_queries = {
        'fan': 'ceiling fan not working repair hindi tutorial',
        'tap': 'tap leaking repair plumbing hindi',
        'wifi': 'wifi slow speed fix router hindi',
        'ac': 'air conditioner not cooling repair hindi',
        'door': 'door repair hinges hindi tutorial',
        'light': 'light bulb holder repair electrical hindi'
    }
    
    problem_lower = problem.lower()
    
    # Find relevant search query
    search_query = None
    for key, query in search_queries.items():
        if key in problem_lower:
            search_query = query
            break
    
    if not search_query:
        search_query = f"{problem} repair hindi tutorial DIY"
    
    # Generate multiple search variations
    tutorials = []
    
    base_url = "https://www.youtube.com/results?search_query="
    
    search_variations = [
        f"{search_query} step by step",
        f"{search_query} DIY home repair",
        f"{search_query} professional vs DIY"
    ]
    
    for i, variation in enumerate(search_variations):
        tutorials.append({
            'title': f"Tutorial {i+1}: {problem} - Hindi Solution",
            'description': f"Step by step repair guide in Hindi",
            'search_link': base_url + urllib.parse.quote(variation),
            'estimated_duration': f"{random.randint(5,15)} minutes",
            'papa_rating': random.choice(["⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐"]),
            'difficulty_level': random.choice(["Beginner", "Intermediate", "Advanced"]),
            'channel_type': random.choice(["DIY Expert", "Professional", "Home Repair"])
        })
    
    return tutorials

def detect_problem_category(problem):
    """Automatically detect problem category"""
    
    categories = {
        'electrical': ['fan', 'light', 'bulb', 'socket', 'switch', 'wiring', 'electrical'],
        'plumbing': ['tap', 'pipe', 'water', 'leak', 'toilet', 'flush', 'drain'],
        'tech': ['wifi', 'internet', 'router', 'phone', 'computer', 'tv', 'remote'],
        'appliances': ['ac', 'air conditioner', 'fridge', 'washing machine', 'microwave'],
        'furniture': ['chair', 'table', 'bed', 'cabinet', 'drawer'],
        'general': ['door', 'window', 'wall', 'paint', 'clean']
    }
    
    problem_lower = problem.lower()
    
    for category, keywords in categories.items():
        if any(keyword in problem_lower for keyword in keywords):
            return category
    
    return 'general'

def estimate_fix_time(problem):
    """Estimate repair time based on problem type"""
    
    time_estimates = {
        'fan': '45-90 minutes (including cleaning)',
        'tap': '20-45 minutes (washer replacement)', 
        'wifi': '10-30 minutes (mostly settings)',
        'ac': '30-60 minutes (filter cleaning only)',
        'door': '15-30 minutes (lubrication/adjustment)',
        'light': '5-20 minutes (bulb/holder replacement)',
        'toilet': '30-60 minutes (flush mechanism)',
        'socket': '20-40 minutes (replacement work)'
    }
    
    problem_lower = problem.lower()
    
    for key, time in time_estimates.items():
        if key in problem_lower:
            return time
    
    return '30-90 minutes (depends on complexity)'

def estimate_difficulty(problem):
    """Estimate difficulty level with Papa's perspective"""
    
    difficulty_levels = {
        'fan': 'Medium - Electrical जानकारी helpful होगी',
        'tap': 'Easy - Basic tools काफी हैं',
        'wifi': 'Easy - Settings change करना है',
        'ac': 'Easy (cleaning) / Hard (gas refill)',
        'door': 'Easy - Maintenance work है',
        'light': 'Easy - Simple replacement',
        'toilet': 'Medium - Plumbing basics जानना चाहिए',
        'socket': 'Hard - Electrical expertise जरूरी'
    }
    
    problem_lower = problem.lower()
    
    for key, difficulty in difficulty_levels.items():
        if key in problem_lower:
            return difficulty
    
    return 'Medium - Basic DIY skills और patience जरूरी'

def get_required_tools(problem):
    """List tools needed for the repair"""
    
    tools_db = {
        'fan': ['Screwdriver set', 'Multimeter (optional)', 'Clean cloth', 'Oil/WD-40', 'Ladder/stool'],
        'tap': ['Adjustable wrench', 'Screwdriver', 'New rubber washer', 'Plumber tape', 'Clean cloth'],
        'wifi': ['No tools needed', 'Just phone/laptop', 'Router manual (optional)'],
        'ac': ['Clean cloth', 'Vacuum cleaner', 'Mild detergent', 'Water spray'],
        'door': ['Screwdriver', 'Oil/WD-40', 'Sandpaper (optional)', 'Clean cloth'],
        'light': ['Screwdriver', 'New bulb/holder', 'Voltage tester', 'Wire stripper (if needed)']
    }
    
    problem_lower = problem.lower()
    
    for key, tools in tools_db.items():
        if key in problem_lower:
            return tools
    
    return ['Basic toolkit', 'Screwdriver set', 'Clean cloth', 'Flashlight', 'Patience और common sense']
