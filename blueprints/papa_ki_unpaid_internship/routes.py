from flask import render_template, request, jsonify, Blueprint
import random
import urllib.parse

# CREATE BLUEPRINT with correct name
bp = Blueprint('papa_ki_unpaid_internship', __name__, url_prefix='/papa-ki-unpaid-internship')

@bp.route('/')
def index():
    """Papa Ki Unpaid Internship main page"""
    return render_template('papa_ki_unpaid_internship.html')

# ============= WEEKEND TIMER KILLER ROUTES =============
@bp.route('/task-generator')
def task_generator():
    """Weekend Timer Killer - Family entertainment hub"""
    return render_template('papa_task_generator.html')

@bp.route('/api/generate-task', methods=['POST'])
def api_generate_task():
    """API to generate weekend family activities"""
    try:
        data = request.get_json()
        family_member = data.get('family_member', 'everyone')
        mood = data.get('mood', 'normal')
        time_available = data.get('time_available', '30-60')
        
        task = generate_weekend_activity(family_member, mood, time_available)
        harry_comment = get_harry_comment(task)
        
        return jsonify({
            'success': True,
            'task': task,
            'harry_comment': harry_comment,
            'family_member': family_member,
            'mood': mood,
            'time_available': time_available
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Harry busy हैं: {str(e)}'
        })

@bp.route('/api/task-categories')
def api_task_categories():
    """Get available weekend activity options"""
    categories = {
        'family_members': [
            {'value': 'kids', 'label': '👶 बच्चे (5-15 years)', 'description': 'Energy भरपूर, entertainment चाहिए'},
            {'value': 'teenagers', 'label': '🧑‍🎓 Teenagers (15-20)', 'description': 'Mobile से हटाना है'},
            {'value': 'wife', 'label': '👩 Wife/Spouse', 'description': 'Productive या relaxing activities'},
            {'value': 'husband', 'label': '👨 Husband', 'description': 'Easy और entertaining tasks'},
            {'value': 'adults', 'label': '👩‍💼 Adults', 'description': 'General productive activities'},
            {'value': 'elderly', 'label': '👴 बुजुर्ग', 'description': 'Light और enjoyable tasks'},
            {'value': 'everyone', 'label': '👨‍👩‍👧‍👦 पूरा Family', 'description': 'सबके साथ मिलकर'}
        ],
        'mood_types': [
            {'value': 'energetic', 'label': '⚡ Energetic', 'description': 'Energy burn करनी है'},
            {'value': 'lazy', 'label': '😴 Lazy mood', 'description': 'आराम से कुछ करना है'},
            {'value': 'creative', 'label': '🎨 Creative', 'description': 'कुछ नया बनाना है'},
            {'value': 'productive', 'label': '💪 Productive', 'description': 'घर का काम भी हो जाए'},
            {'value': 'fun', 'label': '🎉 Fun time', 'description': 'बस मज़े करने हैं'},
            {'value': 'normal', 'label': '😊 Normal', 'description': 'कुछ भी चलेगा'}
        ],
        'time_options': [
            {'value': '15-30', 'label': '⏰ 15-30 minutes', 'description': 'Quick activity'},
            {'value': '30-60', 'label': '🕐 30-60 minutes', 'description': 'Medium task'},
            {'value': '1-2', 'label': '🕑 1-2 hours', 'description': 'Proper project'},
            {'value': '2+', 'label': '🕕 2+ hours', 'description': 'पूरा दिन निकलेगा'}
        ]
    }
    
    return jsonify(categories)

# ============= HARRY NOHARA'S AVERAGE SUNDAY ROUTES =============
@bp.route('/problem-solver')
def problem_solver():
    """Harry Nohara's Average Sunday - Household problem solver"""
    return render_template('papa_problem_solver.html')

@bp.route('/api/solve-problem', methods=['POST'])
def api_solve_problem():
    """API to get YouTube solutions for household problems"""
    try:
        data = request.get_json()
        problem = data.get('problem', '').strip()
        urgency = data.get('urgency', 'normal')
        
        if not problem:
            return jsonify({
                'success': False,
                'error': 'Problem तो बताओ! Harry कैसे help करेंगे?'
            })
        
        # Generate YouTube tutorials
        youtube_tutorials = generate_youtube_tutorials(problem, urgency)
        harry_advice = get_harry_wisdom(problem)
        
        return jsonify({
            'success': True,
            'problem': problem,
            'urgency': urgency,
            'category': 'General Solution',
            'estimated_time': '15-30 minutes',
            'difficulty': 'Easy to Medium',
            'youtube_tutorials': youtube_tutorials,
            'papa_advice': harry_advice,
            'solutions': {
                'quick_check': [f'🔍 "{problem}" को carefully observe करो'],
                'diy_steps': [f'📱 YouTube tutorials देखकर step by step follow करो'],
                'safety_tips': ['⚠️ Safety को priority दो'],
                'when_to_call_expert': 'अगर safety risk हो तो expert से पूछो'
            },
            'tools_needed': ['📱 Mobile phone', '🔧 Basic tools']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Technical problem: {str(e)}'
        })

@bp.route('/api/common-problems')
def api_common_problems():
    """Get list of common desi household problems"""
    problems = [
        {'problem': '⚡ Light/Fan नहीं चल रहा', 'category': 'electrical', 'urgency': 'normal'},
        {'problem': '💧 Tap से पानी leak हो रहा', 'category': 'plumbing', 'urgency': 'high'},
        {'problem': '📱 WiFi slow या disconnect', 'category': 'tech', 'urgency': 'normal'},
        {'problem': '❄️ AC ठंडा नहीं कर रहा', 'category': 'appliances', 'urgency': 'high'},
        {'problem': '🚪 Door/Window properly बंद नहीं', 'category': 'general', 'urgency': 'normal'},
        {'problem': '🍳 Gas stove ignition problem', 'category': 'appliances', 'urgency': 'normal'},
        {'problem': '📺 TV remote/cable issue', 'category': 'tech', 'urgency': 'low'},
        {'problem': '🚽 Toilet flush/drainage problem', 'category': 'plumbing', 'urgency': 'high'},
        {'problem': '🔌 Socket loose या sparking', 'category': 'electrical', 'urgency': 'emergency'},
        {'problem': '🧹 Stubborn stains/cleaning', 'category': 'general', 'urgency': 'low'}
    ]
    
    return jsonify({'common_problems': problems})

# ============= WEEKEND ACTIVITY GENERATOR =============
def generate_weekend_activity(family_member, mood, time_available):
    """Enhanced activity generator with more variety"""
    
    mega_activities = {
        'kids_energetic': [
            {'title': '🏃‍♂️ घर में Obstacle Course', 'description': 'Pillows, chairs, रस्सी से obstacle course बनाओ!', 'fun_factor': '2 घंटे energy burn guaranteed!', 'items_needed': 'Pillows, chairs, rope', 'bonus': 'Winner को special treat!'},
            {'title': '🕺 Dance Battle', 'description': 'YouTube dance videos follow करके competition!', 'fun_factor': 'Exercise भी हो जाएगी!', 'items_needed': 'Phone, speaker, energy', 'bonus': 'Video बनाकर relatives को भेजो!'},
            {'title': '🎯 Target Practice', 'description': 'Paper balls से dustbin में target practice!', 'fun_factor': 'Accuracy improve होगी!', 'items_needed': 'Waste paper, dustbin', 'bonus': 'House cleaning भी हो जाएगी!'},
            {'title': '🏠 House Treasure Hunt', 'description': 'घर में items ढूंढने का game!', 'fun_factor': 'पूरा घर explore करेंगे!', 'items_needed': 'Paper, pen for clues', 'bonus': 'Hidden things भी मिल जाएंगे!'}
        ],
        'kids_lazy': [
            {'title': '📚 Story Creation', 'description': 'Family members के साथ मिलकर story बनाओ!', 'fun_factor': 'Creativity develop होगी!', 'items_needed': 'Imagination, paper', 'bonus': 'Story book बना सकते हो!'},
            {'title': '🎬 Movie Marathon', 'description': 'Old family favorite movies देखो!', 'fun_factor': 'Cozy family time!', 'items_needed': 'Snacks, blankets', 'bonus': 'Childhood memories refresh!'},
            {'title': '🧩 Puzzle Challenge', 'description': 'जितने puzzles हैं सब solve करो!', 'fun_factor': 'Brain exercise quietly!', 'items_needed': 'Puzzles, patience', 'bonus': 'Problem solving skills!'}
        ],
        'teenagers_productive': [
            {'title': '📷 Photography Project', 'description': 'घर के हर corner की artistic photos लो!', 'fun_factor': 'Instagram content ready!', 'items_needed': 'Phone camera, creativity', 'bonus': 'Portfolio बना सकते हो!'},
            {'title': '💻 Skill Learning', 'description': 'YouTube से नया skill सीखो - coding, guitar, art!', 'fun_factor': 'Future investment!', 'items_needed': 'Internet, dedication', 'bonus': 'Resume में add कर सकते हो!'},
            {'title': '📝 Room Makeover Planning', 'description': 'अपने room का complete makeover plan करो!', 'fun_factor': 'Interior design skills!', 'items_needed': 'Paper, measuring tape', 'bonus': 'Parents को impress करके budget मांग सकते हो!'}
        ],
        'adults_productive': [
            {'title': '📊 Financial Planning', 'description': 'Monthly budget review और next month planning!', 'fun_factor': 'Money management clarity!', 'items_needed': 'Calculator, bills, notebook', 'bonus': 'Savings plan बन जाएगा!'},
            {'title': '🗂️ Document Organization', 'description': 'सारे important documents organize करो!', 'fun_factor': 'Future में time बचेगा!', 'items_needed': 'Files, labels', 'bonus': 'Emergency में documents ready होंगे!'},
            {'title': '🌱 Garden Planning', 'description': 'Balcony/terrace में plants arrange करने का plan!', 'fun_factor': 'Green environment!', 'items_needed': 'Pots, soil, seeds', 'bonus': 'Fresh vegetables घर में!'}
        ],
        'everyone_fun': [
            {'title': '🎭 Family Drama Performance', 'description': 'TV serial का scene recreate करो!', 'fun_factor': 'Acting skills discover होंगे!', 'items_needed': 'Costumes, phone for recording', 'bonus': 'Viral video बन सकता है!'},
            {'title': '🍳 Mystery Ingredient Cooking', 'description': 'Random ingredients से dish बनाने का challenge!', 'fun_factor': 'New recipes discover!', 'items_needed': 'Kitchen ingredients', 'bonus': 'Next week के लिए new dish!'},
            {'title': '🎨 Family Art Gallery', 'description': 'सभी अपना artwork बनाकर घर में gallery setup करो!', 'fun_factor': 'Creative family bonding!', 'items_needed': 'Paper, colors, tape', 'bonus': 'Guests को impress करने के लिए!'},
            {'title': '📱 Family TikTok Challenge', 'description': 'Trending challenges try करके videos बनाओ!', 'fun_factor': 'Modern family bonding!', 'items_needed': 'Phone, creativity', 'bonus': 'Social media content ready!'}
        ],
        'wife_productive': [
            {'title': '🍳 Kitchen Organization', 'description': 'Spices arrange करके labels लगाओ, expired items निकालो!', 'fun_factor': 'Cooking time save होगा!', 'items_needed': 'Labels, containers', 'bonus': 'Husband impressed होगा!'},
            {'title': '👗 Wardrobe Declutter', 'description': 'Purane clothes sort करके donation bag बनाओ!', 'fun_factor': 'Space मिल जाएगी नए clothes के लिए!', 'items_needed': 'Boxes, donation bags', 'bonus': 'Shopping justification ready!'},
            {'title': '📱 Photo Organization', 'description': 'Phone की photos organize करके family albums बनाओ!', 'fun_factor': 'Memories refresh होंगी!', 'items_needed': 'Phone, Google Photos', 'bonus': 'Social media content ready!'}
        ],
        'wife_fun': [
            {'title': '💄 DIY Beauty Session', 'description': 'Ghar के ingredients से face pack और hair mask बनाओ!', 'fun_factor': 'Parlor का paisa bach जाएगा!', 'items_needed': 'Kitchen ingredients, creativity', 'bonus': 'Natural glow guaranteed!'},
            {'title': '🎵 Bollywood Dance Session', 'description': 'Favorite songs पर solo dance करके videos बनाओ!', 'fun_factor': 'Fitness + entertainment!', 'items_needed': 'Phone, speaker, energy', 'bonus': 'Husband को impress करने के लिए!'},
            {'title': '☕ Tea Tasting Adventure', 'description': 'Different types की chai try करके rating करो!', 'fun_factor': 'Perfect chai recipe discover करो!', 'items_needed': 'Various tea types, notebook', 'bonus': 'Family के लिए signature chai!'}
        ],
        'husband_lazy': [
            {'title': '📺 Sports Highlights Marathon', 'description': 'Week के सारे sports highlights देखो!', 'fun_factor': 'Sports knowledge update!', 'items_needed': 'TV, snacks, remote', 'bonus': 'Friends के साथ discussion ready!'},
            {'title': '📱 Investment Research', 'description': 'Mutual funds और stocks research करके notes बनाओ!', 'fun_factor': 'Financial planning without effort!', 'items_needed': 'Phone, notepad', 'bonus': 'Wife को responsible husband lag रहे हो!'},
            {'title': '🛋️ Furniture Rearrangement', 'description': 'Room का layout change करके photos लो!', 'fun_factor': 'Interior designer बनने का feel!', 'items_needed': 'Existing furniture, creativity', 'bonus': 'Wife खुश हो जाएगी!'}
        ],
        'elderly_fun': [
            {'title': '📻 Classic Songs Session', 'description': 'Purane zamane के songs सुनके memories share करो!', 'fun_factor': 'Nostalgia और family stories!', 'items_needed': 'Music player, comfortable seating', 'bonus': 'Young generation को history मिलेगा!'},
            {'title': '🌱 Indoor Gardening', 'description': 'Small plants care करके gardening tips share करो!', 'fun_factor': 'Nature connection और knowledge sharing!', 'items_needed': 'Plants, water, love', 'bonus': 'House की air quality improve!'},
            {'title': '📚 Story Narration', 'description': 'बचपन की stories बताकर family को entertain करो!', 'fun_factor': 'Wisdom sharing + entertainment!', 'items_needed': 'Memory, comfortable spot', 'bonus': 'Family bonding strengthen होगी!'}
        ]
    }
    
    # Create key
    key = f"{family_member}_{mood}"
    
    # Get activities or fallback
    activities = mega_activities.get(key, mega_activities.get('everyone_fun', []))
    if not activities:
        activities = [{'title': '🎉 Family Fun Time', 'description': 'कुछ भी मज़ेदार करो together!', 'fun_factor': 'Always works!', 'items_needed': 'Good mood', 'bonus': 'Family happiness!'}]
    
    activity = random.choice(activities)
    
    # Add time note
    if time_available == '15-30':
        activity['time_note'] = 'Quick version - highlights only!'
    elif time_available == '2+':
        activity['time_note'] = 'Extended version - full experience!'
    
    return activity

def get_harry_comment(task):
    """Get Harry's encouraging comment for weekend activities"""
    
    comments = [
        'Perfect! Sunday को productive बनाने का बेहतरीन तरीका! Family time + fun! 👨‍👩‍👧‍👦',
        'Excellent choice! Weekends ऐसे ही utilize करने चाहिए - no boring time! 🎉',
        'Harry approved! ये activity करने के बाद सबको satisfaction मिलेगा! ✨',
        'Brilliant! घर में entertainment, family bonding, और memories - सब एक साथ! 🏆',
        'Great idea! Sunday evening में सबके पास share करने के लिए stories होंगी! 😊',
        'Wonderful! ऐसे activities से family bond strong होता है! Keep it up! 💪',
        'Amazing! Bore होने का chance ही नहीं है - full entertainment package! 🎪',
        'Superb! Sunday well spent - productive भी, fun भी! Harry style! 👍'
    ]
    
    return random.choice(comments)

def get_harry_wisdom(problem):
    """Get Harry's practical wisdom for household problems"""
    
    wisdom_quotes = [
        'Sunday को कोई problem नहीं रोक सकती! DIY spirit से sab solve हो जाता है! 💪',
        'Ghar के छोटे problems खुद handle करना आना चाहिए - confidence बढ़ता है! 🔧',
        'Emergency में panic नहीं करना, step by step solution try करना - Harry mantra! 😌',
        'Most household problems simple हैं, बस patience और right approach चाहिए! 🧠',
        'Safety first, solution second - यह हमेशा याद रखना family के लिए! ⚠️',
        'DIY solutions से पैसा भी बचता है और skill भी develop होती है! 💡',
        'Family के साथ मिलकर problems solve करना बेहतर - teamwork! 👨‍👩‍👧‍👦',
        'हर problem एक learning opportunity है - next time अपने आप handle कर सकोगे! 📚'
    ]
    
    return random.choice(wisdom_quotes)

# ============= HOUSEHOLD PROBLEM SOLVER =============
def get_household_solution(problem, urgency):
    """Get practical desi household solutions with dynamic YouTube tutorials"""
    
    problem_lower = problem.lower()
    
    # Generate dynamic YouTube tutorials based on problem
    youtube_tutorials = generate_youtube_tutorials(problem, urgency)
    
    # Electrical problems
    if any(word in problem_lower for word in ['light', 'fan', 'switch', 'electrical', 'current']):
        return {
            'category': 'Electrical Issue',
            'estimated_time': '15-30 minutes' if urgency != 'emergency' else '5-15 minutes',
            'difficulty': 'Easy to Medium',
            'solutions': {
                'quick_check': [
                    '🔌 Main switch on है कि नहीं check करो',
                    '💡 Other lights/fans working हैं कि नहीं verify करो',
                    '🔧 Switch को properly on/off करके try करो',
                    '👀 Visible damage, burning smell तो नहीं?'
                ],
                'diy_steps': [
                    '⚡ Main supply off करके safety ensure करो',
                    '🧽 Switch/connection points clean करो (dust हटाओ)',
                    '🔩 Loose connections tight करो (if accessible)',
                    '💡 Bulb/tube light को remove करके फिर properly fix करो',
                    '🔄 Slowly main switch on करके test करो'
                ],
                'safety_tips': [
                    '⚠️ Electrical काम से पहले हमेशा main switch off करो',
                    '🧤 Dry hands रखो, wet hands से कभी न छुओ',
                    '👀 अगर sparking या burning smell आए तो तुरंत रोको',
                    '👨‍🔧 Major electrical issues में expert को call करो'
                ],
                'when_to_call_expert': 'अगर burning smell, sparking, या multiple devices affected हों'
            },
            'tools_needed': [
                '🔧 Basic screwdriver set',
                '🧽 Cleaning cloth',
                '💡 Replacement bulb (if needed)',
                '🔦 Torch/mobile flashlight'
            ],
            'youtube_tutorials': youtube_tutorials
        }
    
    # Plumbing problems
    elif any(word in problem_lower for word in ['tap', 'water', 'leak', 'pipe', 'toilet', 'flush']):
        return {
            'category': 'Plumbing Issue',
            'estimated_time': '20-45 minutes' if urgency != 'emergency' else '10-20 minutes',
            'difficulty': 'Easy to Medium',
            'solutions': {
                'quick_check': [
                    '💧 Main water supply on है कि नहीं',
                    '🚿 Other taps से water आ रहा है?',
                    '👀 Leak कहाँ से हो रहा है exactly?',
                    '🔧 Handle/valve properly move हो रहा है?'
                ],
                'diy_steps': [
                    '🛑 Main water valve बंद करो (very important!)',
                    '🧽 Area को clean और dry करो',
                    '🔧 Loose joints/screws को carefully tight करो',
                    '🔄 Rubber washers check करके replace करो (₹5-10)',
                    '💧 Slowly water supply on करके test करो'
                ],
                'safety_tips': [
                    '🛑 पानी का main valve पहले बंद करो',
                    '🧽 Area को dry रखो slip न जाओ',
                    '⚠️ Hot water के साथ careful रहो',
                    '💧 Major leakage में तुरंत main supply बंद करो'
                ],
                'when_to_call_expert': 'अगर main pipe damage या pressure issues हों'
            },
            'tools_needed': [
                '🔧 Adjustable wrench',
                '🧽 Cleaning cloths',
                '💍 Rubber washers (₹5-10)',
                '🧰 Basic toolkit'
            ],
            'youtube_tutorials': youtube_tutorials
        }
    
    # Tech problems  
    elif any(word in problem_lower for word in ['wifi', 'internet', 'tv', 'remote', 'phone', 'tech']):
        return {
            'category': 'Tech Issue',
            'estimated_time': '10-30 minutes' if urgency != 'emergency' else '5-15 minutes',
            'difficulty': 'Easy',
            'solutions': {
                'quick_check': [
                    '🔌 Device का power properly connected है?',
                    '📶 Other devices working हैं same network पर?',
                    '🔋 Remote की battery check करो',
                    '📡 Router/modem के lights green हैं?'
                ],
                'diy_steps': [
                    '🔄 Device को off करके 30 seconds wait, फिर on करो',
                    '🧽 Remote के buttons clean करो, battery change करो',
                    '📱 WiFi को forget करके reconnect करो',
                    '🌐 Router को restart करो (2 minutes off रखो)',
                    '📞 Service provider को call करके complaint करो'
                ],
                'safety_tips': [
                    '⚡ Power connections properly check करो',
                    '🔋 Battery को सही direction में लगाओ',
                    '💧 Electronics को water से दूर रखो',
                    '🌡️ Overheating को avoid करो'
                ],
                'when_to_call_expert': 'अगर hardware damage या line issue हो'
            },
            'tools_needed': [
                '🔋 Replacement batteries',
                '🧽 Cleaning cloth',
                '📱 Mobile phone (for testing)',
                '📞 Service provider number'
            ],
            'youtube_tutorials': youtube_tutorials
        }
    
    # Generic solution
    else:
        return {
            'category': 'General Household Issue',
            'estimated_time': '15-60 minutes' if urgency != 'emergency' else '10-30 minutes',
            'difficulty': 'Varies',
            'solutions': {
                'quick_check': [
                    '🔍 Problem को carefully observe करो',
                    '📖 Manual/warranty check करो',
                    '🔌 Power supply और basic connections verify करो',
                    '👥 Family members से similar experience पूछो'
                ],
                'diy_steps': [
                    '🧽 Basic cleaning और maintenance try करो',
                    '🔧 Visible loose parts को carefully tight करो',
                    '📱 YouTube पर similar problem search करो',
                    '💬 Neighbors या friends से advice लो',
                    '📞 Customer care helpline पर call करो'
                ],
                'safety_tips': [
                    '⚠️ Safety को priority दो',
                    '🔌 Power off करके काम करो',
                    '📚 Manual पढ़ो पहले',
                    '👨‍🔧 Doubt हो तो expert से पूछो'
                ],
                'when_to_call_expert': 'अगर safety risk हो या warranty void हो सकती हो'
            },
            'tools_needed': [
                '🔧 Basic toolkit',
                '🧽 Cleaning materials',
                '📱 Mobile for research',
                '📚 Product manual'
            ],
            'youtube_tutorials': youtube_tutorials
        }


def generate_youtube_tutorials(problem, urgency):
    """Generate 2-3 YouTube tutorials based on the specific problem and urgency"""
    
    # Clean and prepare search terms
    problem_clean = problem.lower().strip()
    
    # Create different search queries based on urgency
    urgency_modifiers = {
        'emergency': ['quick fix', 'immediate solution', 'urgent repair'],
        'high': ['easy fix', 'step by step', 'diy repair'],
        'normal': ['detailed tutorial', 'complete guide', 'how to fix'],
        'low': ['maintenance', 'prevention', 'tips and tricks']
    }
    
    modifiers = urgency_modifiers.get(urgency, urgency_modifiers['normal'])
    
    # Generate 3 different YouTube search URLs
    tutorials = []
    
    # Tutorial 1: Direct problem search with Hindi
    search_1 = f"{problem_clean} fix hindi home solution"
    tutorials.append({
        'title': f'🎯 {problem} - Hindi Solution',
        'search_link': f'https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_1)}',
        'description': f'"{problem}" की direct solution Hindi में',
        'estimated_duration': '8-15 minutes',
        'papa_rating': '⭐⭐⭐⭐⭐',
        'urgency_type': f'{urgency.title()} Priority'
    })
    
    # Tutorial 2: Problem + urgency modifier
    search_2 = f"{problem_clean} {modifiers[0]} hindi tutorial"
    tutorials.append({
        'title': f'⚡ {modifiers[0].title()} Method - {urgency.title()} Level',
        'search_link': f'https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_2)}',
        'description': f'{urgency.title()} urgency के लिए {modifiers[0]} approach',
        'estimated_duration': '5-12 minutes' if urgency == 'emergency' else '10-20 minutes',
        'papa_rating': '⭐⭐⭐⭐',
        'urgency_type': f'Best for {urgency} situations'
    })
    
    # Tutorial 3: Alternative approach + prevention
    search_3 = f"{problem_clean} {modifiers[1]} troubleshooting hindi"
    tutorials.append({
        'title': f'🔧 Alternative Method + Prevention Tips',
        'search_link': f'https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_3)}',
        'description': f'Different approach और future prevention के tips',
        'estimated_duration': '12-25 minutes',
        'papa_rating': '⭐⭐⭐⭐',
        'urgency_type': 'Complete understanding'
    })
    
    return tutorials
