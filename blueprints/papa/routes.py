from flask import render_template, request, jsonify, Blueprint
import requests
import json
import random

bp = Blueprint('papa', __name__, url_prefix='/papa')

@bp.route('/')
def index():
    """Papa Ki Unpaid Internship main page - DIY tutorial hub"""
    return render_template('papa_ki_unpaid_internship.html')

@bp.route('/search-tutorials', methods=['POST'])
def search_tutorials():
    """Search for DIY tutorials based on problem description"""
    try:
        data = request.get_json()
        problem = data.get('problem', '').strip()
        category = data.get('category', 'general')
        
        if not problem:
            return jsonify({
                'success': False,
                'error': 'कुछ तो problem बताओ भाई!'
            })
        
        # Generate tutorial suggestions based on common Indian household problems
        tutorials = generate_tutorial_suggestions(problem, category)
        
        return jsonify({
            'success': True,
            'problem': problem,
            'category': category,
            'tutorials': tutorials,
            'papa_advice': get_papa_advice(category)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@bp.route('/tutorial-categories')
def tutorial_categories():
    """Show different categories of tutorials"""
    categories = {
        'electrical': {
            'name': '⚡ बिजली का काम',
            'description': 'switches, fans, lights की problems',
            'common_issues': ['Fan नहीं चल रहा', 'Switch खराब है', 'Light नहीं जल रही']
        },
        'plumbing': {
            'name': '🚿 पानी का काम', 
            'description': 'pipes, taps, bathroom की problems',
            'common_issues': ['Tap से पानी leak', 'Toilet flush problem', 'Pipe block']
        },
        'furniture': {
            'name': '🪑 फर्नीचर repair',
            'description': 'chair, table, almirah की problems', 
            'common_issues': ['Chair टूट गई', 'Table हिल रही है', 'Drawer नहीं खुल रहा']
        },
        'appliances': {
            'name': '📱 घरेलू सामान',
            'description': 'TV, AC, fridge की problems',
            'common_issues': ['TV की picture problem', 'AC ठंडा नहीं कर रहा', 'Fridge में पानी']
        },
        'general': {
            'name': '🔧 सामान्य मरम्मत',
            'description': 'घर की छोटी-मोटी problems',
            'common_issues': ['दीवार में छेद', 'दरवाजा बंद नहीं हो रहा', 'खिड़की अटक गई']
        }
    }
    
    return render_template('papa_ki_unpaid_internship.html')

# ============= TASK GENERATOR ROUTES =============

@bp.route('/diy-tools')
def diy_tools():
    """Show essential DIY tools every papa should have"""
    tools = {
        'basic': {
            'name': 'बेसिक टूल्स',
            'tools': [
                {'name': 'हथौड़ा (Hammer)', 'use': 'कील ठोकने के लिए', 'price': '₹50-100'},
                {'name': 'स्क्रू ड्राइवर सेट', 'use': 'पेंच कसने-ढीले करने के लिए', 'price': '₹100-200'},
                {'name': 'प्लायर्स', 'use': 'तार पकड़ने के लिए', 'price': '₹80-150'},
                {'name': 'टेप मेजर', 'use': 'माप के लिए', 'price': '₹50-100'}
            ]
        },
        'electrical': {
            'name': 'इलेक्ट्रिकल टूल्स',
            'tools': [
                {'name': 'टेस्टर', 'use': 'करंट चेक करने के लिए', 'price': '₹30-50'},
                {'name': 'वायर स्ट्रिपर', 'use': 'तार छीलने के लिए', 'price': '₹100-200'},
                {'name': 'इंसुलेशन टेप', 'use': 'जोड़ को ढकने के लिए', 'price': '₹20-40'}
            ]
        },
        'plumbing': {
            'name': 'प्लंबिंग टूल्स',
            'tools': [
                {'name': 'मंकी रेंच', 'use': 'पाइप के जोड़ के लिए', 'price': '₹150-300'},
                {'name': 'प्लंजर', 'use': 'टॉयलेट/सिंक block के लिए', 'price': '₹100-200'},
                {'name': 'पाइप कटर', 'use': 'पाइप काटने के लिए', 'price': '₹200-400'}
            ]
        }
    }
    
    return render_template('papa_diy_tools.html', tools=tools)

@bp.route('/emergency-fixes')
def emergency_fixes():
    """Quick emergency fixes for common problems"""
    fixes = [
        {
            'problem': '💡 Light नहीं जल रही',
            'quick_fix': '1. Bulb check करो\n2. Switch off-on करो\n3. MCB check करो',
            'tools_needed': 'टेस्टर, नया bulb',
            'safety': '⚠️ Main switch off करके करो!'
        },
        {
            'problem': '🚿 Tap से पानी leak',
            'quick_fix': '1. Main valve बंद करो\n2. Tap का handle tight करो\n3. Rubber washer change करो',
            'tools_needed': 'मंकी रेंच, नया washer',
            'safety': '⚠️ पानी का main बंद करो!'
        },
        {
            'problem': '🪑 Chair हिल रही है',
            'quick_fix': '1. सभी screws tight करो\n2. टूटे parts को glue करो\n3. Support लगाओ',
            'tools_needed': 'स्क्रू ड्राइवर, fevicol',
            'safety': '✅ आसान और safe!'
        },
        {
            'problem': '🚪 Door properly बंद नहीं हो रहा',
            'quick_fix': '1. Hinges में oil डालो\n2. Door frame check करो\n3. Lock mechanism clean करो',
            'tools_needed': 'oil, cleaning cloth',
            'safety': '✅ बिल्कुल safe!'
        }
    ]
    
    return render_template('papa_emergency_fixes.html', fixes=fixes)

# ============= TASK GENERATOR ROUTES =============
@bp.route('/task-generator')
def task_generator():
    """Generate funny tasks for kids and family"""
    return render_template('papa_task_generator.html')

@bp.route('/api/generate-task', methods=['POST'])
def api_generate_task():
    """API to generate witty household tasks"""
    try:
        data = request.get_json()
        person = data.get('person', 'बच्चे')  # बच्चे, wife, मम्मी, etc.
        mood = data.get('mood', 'normal')  # boring, energetic, lazy, मस्ती
        time_available = data.get('time', '30')  # minutes
        
        # Generate task based on inputs
        task = generate_funny_task(person, mood, time_available)
        
        return jsonify({
            'success': True,
            'task': task,
            'person': person,
            'estimated_fun': random.choice(['😂 Guaranteed Laughter', '🎉 Family Entertainment', '😄 Time-Pass Champion']),
            'papa_comment': get_papa_task_comment()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Papa confused हो गए: {str(e)}'
        })

@bp.route('/api/task-categories')
def api_task_categories():
    """Get available task categories"""
    categories = {
        'person_types': [
            {'value': 'बच्चे', 'label': '👶 बच्चे (Kids)', 'description': 'Fun tasks for children'},
            {'value': 'Wife', 'label': '👩 Wife', 'description': 'Creative tasks for partner'},
            {'value': 'मम्मी', 'label': '👵 मम्मी (Mom)', 'description': 'Engaging tasks for mom'},
            {'value': 'Papa', 'label': '👨 Papa (Self)', 'description': 'Tasks when Papa is free'}
        ],
        'mood_types': [
            {'value': 'boring', 'label': '😴 Boring (रोज़ का सा)', 'description': 'When feeling dull'},
            {'value': 'energetic', 'label': '⚡ Energetic (एनर्जी भरपूर)', 'description': 'When full of energy'},
            {'value': 'lazy', 'label': '😅 Lazy (आलसी मूड)', 'description': 'When feeling lazy'},
            {'value': 'masti', 'label': '🎉 Masti (मस्ती का मूड)', 'description': 'When want to have fun'}
        ],
        'time_options': [
            {'value': '15', 'label': '15 minutes - Quick task'},
            {'value': '30', 'label': '30 minutes - Standard task'}, 
            {'value': '60', 'label': '1 hour - Detailed task'},
            {'value': '120', 'label': '2 hours - Project task'}
        ]
    }
    return jsonify(categories)

# ============= TASK GENERATOR HELPER FUNCTIONS =============
def generate_funny_task(person, mood, time_available):
    """Generate hilarious household tasks"""
    
    # Expanded task database based on person and mood
    task_database = {
        'बच्चे': {
            'boring': [
                {
                    'task': '🕵️ घर में सभी remote controls ढूंढ कर एक जगह रखना',
                    'description': 'Detective बनकर सारे गायब remotes को ढूंढना है',
                    'reward': 'TV remote का मुख्यमंत्री बन जाओगे',
                    'fun_factor': 'Mystery solving + treasure hunt',
                    'papa_tricks': 'Sofa के नीचे, bed के बीच में, kitchen counter पर check करो'
                },
                {
                    'task': '📱 Papa के phone की सारी blurry photos delete करना',
                    'description': 'Tech expert बनकर Papa का phone clean करना',
                    'reward': 'Photo gallery manager का title',
                    'fun_factor': 'Papa के weird photos देखने को मिलेंगे',
                    'papa_tricks': 'Screenshots folder भी check करना, वहां duplicate होते हैं'
                },
                {
                    'task': '🧦 सारे बिखरे हुए मोज़े जोड़े बनाकर arrange करना',
                    'description': 'Matching game खेलते हुए सारे socks को pair करना',
                    'reward': 'Sock matching champion',
                    'fun_factor': 'Color coordination सीखोगे',
                    'papa_tricks': 'अकेले मोज़े अलग रखो, शायद बाद में partner मिल जाए'
                }
            ],
            'energetic': [
                {
                    'task': '🏃‍♂️ हर कमरे में जाकर 10-10 jumping jacks करना',
                    'description': 'Fitness trainer बनकर घर का tour करते हुए exercise',
                    'reward': 'Family का fitness coach बन जाओगे',
                    'fun_factor': 'Energy burn + house exploration',
                    'papa_tricks': 'हर room में अलग-अलग exercise करो - push-ups, sit-ups'
                },
                {
                    'task': '🎵 हर room में जाकर अलग-अलग song पर dance करना',
                    'description': 'Mobile entertainer बनकर घर के हर कोने में performance',
                    'reward': 'Family का डांसर + DJ',
                    'fun_factor': 'Music + dance + movement',
                    'papa_tricks': 'हर room के लिए उस room के suitable song choose करो'
                }
            ],
            'lazy': [
                {
                    'task': '🛋️ Sofa पर बैठे-बैठे TV channels count करना',
                    'description': 'Remote control के साथ research project',
                    'reward': 'TV channel encyclopedia',
                    'fun_factor': 'आराम से बैठकर useful काम',
                    'papa_tricks': 'अच्छे channels का list भी बना देना'
                }
            ],
            'masti': [
                {
                    'task': '🎭 Family के हर member का 2-minute mimicry show',
                    'description': 'Comedy show करना जिसमें सबकी नकल करनी है',
                    'reward': 'Family comedian title',
                    'fun_factor': 'Acting + entertainment + laughter',
                    'papa_tricks': 'Papa की morning routine की mimicry सबसे funny होगी'
                }
            ]
        },
        'Wife': {
            'boring': [
                {
                    'task': '💄 सारे beauty products को expiry date wise arrange करना',
                    'description': 'Beauty inventory manager बनना',
                    'reward': 'New cosmetic shopping budget approved',
                    'fun_factor': 'Organization + future shopping planning',
                    'papa_tricks': 'Expired ones का list बनाकर Papa को dikhana'
                }
            ],
            'energetic': [
                {
                    'task': '🌱 सारे plants को nए pots में shift करना',
                    'description': 'Garden makeover project',
                    'reward': 'New plants buying approved',
                    'fun_factor': 'Gardening + home beautification',
                    'papa_tricks': 'Before-after photos लेना for social media'
                }
            ],
            'masti': [
                {
                    'task': '🤳 हर room का Instagram-worthy photoshoot',
                    'description': 'Interior designer + photographer बनना',
                    'reward': 'Social media bragging rights',
                    'fun_factor': 'Creativity + social media content',
                    'papa_tricks': 'Different lighting और angles try करना'
                }
            ]
        },
        'मम्मी': [
            {
                'task': '🥘 Kitchen के सारे masala containers को alphabetical order में arrange करना',
                'description': 'Spice library manager बनना',
                'reward': 'Kitchen queen crown',
                'fun_factor': 'Organization + cooking efficiency',
                'papa_tricks': 'Labels भी लगा देना for easy identification',
                'mood': 'boring'
            }
        ],
        'Papa': [
            {
                'task': '🔧 घर के सारे loose screws find करके tight करना',
                'description': 'Professional maintenance engineer बनना',
                'reward': 'Household engineer title',
                'fun_factor': 'Practical work + problem solving',
                'papa_tricks': 'Tool box organize भी हो जाएगा',
                'mood': 'boring'
            }
        ]
    }
    
    # Get tasks for the person
    person_tasks = task_database.get(person, task_database['बच्चे'])
    
    # If person_tasks is a dict with moods, get mood-specific tasks
    if isinstance(person_tasks, dict) and mood in person_tasks:
        available_tasks = person_tasks[mood]
    elif isinstance(person_tasks, dict):
        # Get first available mood for that person
        available_tasks = list(person_tasks.values())[0]
    else:
        # If person_tasks is a list, filter by mood if available
        available_tasks = [task for task in person_tasks if task.get('mood', 'any') in [mood, 'any']]
        if not available_tasks:
            available_tasks = person_tasks
    
    # Select random task
    selected_task = random.choice(available_tasks)
    
    # Add time and difficulty estimates
    selected_task['estimated_time'] = f"{time_available} minutes"
    selected_task['difficulty'] = random.choice(['बिल्कुल आसान', 'आसान है', 'थोड़ा challenge', 'मज़ेदार'])
    selected_task['completion_probability'] = random.choice(['95% success rate', '100% fun guaranteed', '90% effective'])
    
    return selected_task

def get_papa_task_comment():
    """Get Papa's witty comment on the task"""
    comments = [
        "अरे वाह! यह तो genius idea है! दो काम एक साथ! 🤓",
        "इससे घर भी clean हो जाएगा और बोरियत भी भाग जाएगी! 😄",
        "Papa approved task! Entertainment + productivity = Perfect combo! 👏",
        "बच्चे खुश, घर भी साफ! यही तो चाहिए था! 🎉",
        "यह task तो family bonding भी बना देगा! सबको involve करो! ❤️",
        "Creative parenting level: Expert! IIT में admission confirm! 🏆",
        "घर का काम + मनोरंजन = Papa का jugaad strikes again! 💡",
        "इसे करने के बाद बच्चा tired होकर सो जाएगा! Bonus point! 😴",
        "यह करके देखो, फिर बताना कितना मज़ा आया! 🤩",
        "Perfect Sunday activity! Productive + entertaining! 🌟"
    ]
    return random.choice(comments)


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
    import urllib.parse
    
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