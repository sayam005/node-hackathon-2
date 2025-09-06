from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import random
import json
from datetime import datetime

# Create blueprint
bp = Blueprint('mummy_pizza', __name__, url_prefix='/mummy-pizza')

# Enhanced Desi Recipe Data with Mom's Touch! 👩‍🍳
RANDOM_RECIPES = [
    {
        "name": "Aloo ke Parathe (Love Wale)",
        "description": "Mummy ka special! Jab ghar mein kuch nahi hai toh ye magic hai! ✨",
        "difficulty": "Easy Peasy",
        "time": "25 minutes",
        "ingredients": ["aloo 4-5 (boiled)", "atta 2 cup", "namak", "oil", "hari mirch", "adrak", "haldi", "dhania"],
        "steps": [
            "Aloo ko mash karo pyaar se, lumps nahi chahiye!",
            "Atta mein thoda sa oil aur namak daalke soft dough banao",
            "Aloo mein namak, hari mirch, adrak paste mix karo",
            "Dough ki roti banao, aloo bharke band karo",
            "Tave pe oil lagake golden brown tak sekiye",
            "Dahi aur pickle ke saath serve karo! Mummy ki guarantee!"
        ],
        "mom_approval": "100% ❤️",
        "taste_rating": "10/10",
        "category": "comfort food",
        "video_search": "aloo paratha recipe hindi",
        "youtube_channels": ["Kabita's Kitchen", "Cook with Nisha", "Rajshri Food"],
        "mom_tips": "Beta, rolling mein patient raho! Jaldi mein phate toh sab aloo bahar aa jayega!",
        "angry_mom_mode": "Agar mummy naraz hai toh extra ghee lagao aur unko tea bhi bana do! ☕",
        "secret_ingredient": "Thoda sa jeera powder - mummy ko pata nahi chalega but taste badh jayega!",
        "backup_plan": "Agar fail ho jaye toh bol do 'Mummy main experiment kar raha tha nutrition ke liye!'"
    },
    {
        "name": "Maggi Bhel (Fusion Master)",
        "description": "Jab normal Maggi se bore ho jao toh ye jugaad try karo! 🔥",
        "difficulty": "Super Easy",
        "time": "15 minutes",
        "ingredients": ["maggi 2 packets", "onion chopped", "tomato chopped", "cucumber", "sev", "lemon", "chaat masala", "hari chutney"],
        "steps": [
            "Maggi banao but extra crispy - paani kam rakho",
            "Thanda hone do, refrigerator mein 10 min rakho",
            "Onion, tomato, cucumber chop karo fine",
            "Maggi ko break karo, vegetables mix karo",
            "Sev, lemon juice, chaat masala daalke mix karo",
            "Hari chutney ke saath serve karo! Instagram ready! 📸"
        ],
        "mom_approval": "75% (kyunki Maggi hai 😅)",
        "taste_rating": "9/10",
        "category": "snacks",
        "video_search": "maggi bhel recipe street style",
        "youtube_channels": ["Street Food India", "Cook with Parul", "Sanjeev Kapoor"],
        "mom_tips": "Beta Maggi kam khaya karo, lekin ye better hai normal se!",
        "angry_mom_mode": "Bol do 'Mummy maine vegetables add kiye hain, healthy banaya hai!'",
        "secret_ingredient": "Thoda sa chat masala extra - tasty lagega!",
        "backup_plan": "Friends ko serve karo, woh impress ho jayenge!"
    },
    {
        "name": "Dahi Wale Aloo (Comfort King)",
        "description": "Mummy ki favorite! Rice ke saath perfect combination! 🍚",
        "difficulty": "Easy",
        "time": "20 minutes",
        "ingredients": ["aloo 5-6 medium", "dahi 1 cup", "jeera", "hing", "haldi", "lal mirch", "namak", "oil", "hari mirch"],
        "steps": [
            "Aloo ko cubes mein cut karo, fry karo light golden tak",
            "Dahi ko beat karo smooth, haldi mix karo",
            "Pan mein jeera, hing ka tadka lagao",
            "Aloo daalke 2 min mix karo",
            "Dahi slowly add karo, curdle nahi hona chahiye!",
            "5-7 min simmer karo, hari mirch garnish karo"
        ],
        "mom_approval": "95% ❤️",
        "taste_rating": "9.5/10",
        "category": "main course",
        "video_search": "dahi aloo recipe simple",
        "youtube_channels": ["Hebbar's Kitchen", "Vahchef", "Cook with Monika"],
        "mom_tips": "Dahi room temperature pe rakho pehle, warna curdle ho jayega!",
        "angry_mom_mode": "Bol do 'Mummy protein aur carbs dono mil rahe hain, balanced diet!'",
        "secret_ingredient": "Last mein thoda sa garam masala - restaurant taste milega!",
        "backup_plan": "Paratha ke saath bhi chalega agar rice nahi hai!"
    },
    {
        "name": "Bread Pizza (Tawa Special)",
        "description": "Oven nahi hai? Koi baat nahi! Tawa pe banayenge! 🍕",
        "difficulty": "Easy",
        "time": "18 minutes",
        "ingredients": ["bread slices 4", "tomato sauce", "cheese grated", "onion", "capsicum", "tomato", "oregano", "chilli flakes"],
        "steps": [
            "Bread slices ko lightly toast karo tawa pe",
            "Tomato sauce evenly spread karo",
            "Onion, capsicum, tomato rings rakhiye",
            "Cheese generously daalo (mummy dekh nahi rahi toh extra!)",
            "Oregano aur chilli flakes sprinkle karo",
            "Tawa pe cover karne cheese melt tak - 5-7 min"
        ],
        "mom_approval": "80% (bread waste nahi hua!)",
        "taste_rating": "8.5/10",
        "category": "snacks",
        "video_search": "tawa bread pizza recipe",
        "youtube_channels": ["Cook with Nisha", "Tarla Dalal", "CookingShooking"],
        "mom_tips": "Bread fresh nahi hai toh pehle sprinkle water karo!",
        "angry_mom_mode": "Bol do 'Mummy creative cooking seekh raha hun, skill development!'",
        "secret_ingredient": "Thoda sa butter tawa pe - taste aur smell amazing!",
        "backup_plan": "Domino's se compare karo, ghar ka better bolo! 😎"
    },
    {
        "name": "Curd Rice (South Style)",
        "description": "Ghar mein curd zyada hai? Perfect solution! Stomach ko bhi theek lagega! 🥄",
        "difficulty": "Super Easy",
        "time": "12 minutes",
        "ingredients": ["rice cooked 2 cups", "dahi 1 cup", "namak", "rai", "jeera", "curry patta", "hing", "hari mirch", "oil"],
        "steps": [
            "Rice ko thoda sa mash karo, smooth paste nahi banana",
            "Dahi beat karo, namak mix karo",
            "Pan mein oil, rai, jeera, curry patta ka tadka",
            "Hing aur hari mirch add karo",
            "Rice mein dahi mix karo, tadka pour karo",
            "Mix karke serve karo - instant comfort food!"
        ],
        "mom_approval": "90% (healthy hai!)",
        "taste_rating": "8/10",
        "category": "comfort food",
        "video_search": "curd rice recipe south indian",
        "youtube_channels": ["Hebbar's Kitchen", "Amma's Kitchen", "Cook with Monika"],
        "mom_tips": "Dahi fresh use karo, khatta wala nahi!",
        "angry_mom_mode": "Bol do 'Mummy probiotic hai, health ke liye banaya!'",
        "secret_ingredient": "Thoda sa grated ginger - digestion improve hoga!",
        "backup_plan": "Pickle ke saath serve karo, taste badh jayega!"
    },
    {
        "name": "Egg Curry (Protein Power)",
        "description": "Quick dinner solution! Rice aur roti dono ke saath perfect! 🥚",
        "difficulty": "Medium",
        "time": "25 minutes",
        "ingredients": ["eggs 4", "onion 2", "tomato 2", "adrak-lahsun paste", "haldi", "lal mirch", "garam masala", "oil", "hari mirch"],
        "steps": [
            "Eggs hard boil karo, shell remove karke aside rakho",
            "Onion fry karo golden tak, adrak-lahsun paste add karo",
            "Tomato chop karke daalke cook karo mushy tak",
            "Masale add karo - haldi, lal mirch, garam masala",
            "Thoda paani add karo, gravy consistency banao",
            "Eggs gently add karo, 5 min simmer karo"
        ],
        "mom_approval": "85% (protein bharpur!)",
        "taste_rating": "9/10",
        "category": "main course",
        "video_search": "egg curry recipe restaurant style",
        "youtube_channels": ["Sanjeev Kapoor", "Cook with Nisha", "Vahchef"],
        "mom_tips": "Eggs ko carefully handle karo, toot nahi jaane chahiye!",
        "angry_mom_mode": "Bol do 'Mummy non-veg expensive hai, eggs economical protein source!'",
        "secret_ingredient": "Last mein kasuri methi - restaurant taste milega!",
        "backup_plan": "Chapati ke saath roll banake khao, mobile mein video dekh ke!"
    },
    {
        "name": "Rajma Chawal (Comfort Ultimate)",
        "description": "Sunday special! Mummy ki favorite aur sabki demand! ❤️",
        "difficulty": "Medium",
        "time": "45 minutes (if rajma ready)",
        "ingredients": ["rajma boiled 1 cup", "rice", "onion 2", "tomato 2", "adrak-lahsun", "jeera", "bay leaves", "garam masala"],
        "steps": [
            "Pressure cooker mein rajma overnight soak karke boil karo",
            "Pan mein jeera, bay leaves, onion fry karo",
            "Adrak-lahsun paste, tomato add karke cook karo",
            "Boiled rajma with water add karo",
            "Masale daalke 15 min simmer karo thick tak",
            "Rice ke saath serve karo - Sunday vibes! 🍽️"
        ],
        "mom_approval": "100% (mummy ka favorite!)",
        "taste_rating": "10/10",
        "category": "main course",
        "video_search": "rajma chawal recipe punjabi style",
        "youtube_channels": ["Kabita's Kitchen", "Cook with Nisha", "Punjabi Zaika"],
        "mom_tips": "Rajma overnight soak karna zaroori hai, warna hard rahega!",
        "angry_mom_mode": "Bol do 'Mummy Sunday special banaya hai, family time!' Family time magic word hai!",
        "secret_ingredient": "Thoda sa cream last mein - rich taste milega!",
        "backup_plan": "Extra bana ke next day lunch mein le jao office/college!"
    },
    {
        "name": "Poha (Morning Champion)",
        "description": "Breakfast ka king! 10 min mein ready, nutrition full! 🌅",
        "difficulty": "Easy",
        "time": "15 minutes",
        "ingredients": ["poha 2 cups", "onion 1", "aloo 1 small", "hari mirch", "jeera", "hing", "haldi", "namak", "lemon", "sev"],
        "steps": [
            "Poha ko paani mein wash karo, drain karo properly",
            "Pan mein oil, jeera, hing, hari mirch fry karo",
            "Onion add karo, golden tak fry karo",
            "Aloo cubes add karo, soft tak cook karo",
            "Poha daalke mix karo, haldi namak add karo",
            "Lemon squeeze karo, sev garnish karo - ready!"
        ],
        "mom_approval": "95% (healthy breakfast!)",
        "taste_rating": "9/10",
        "category": "breakfast",
        "video_search": "poha recipe maharashtrian style",
        "youtube_channels": ["Hebbar's Kitchen", "Cook with Monika", "Marathi Zaika"],
        "mom_tips": "Poha quality good lena, patla nahi thick wala!",
        "angry_mom_mode": "Bol do 'Mummy healthy breakfast banaya, energy full day ke liye!'",
        "secret_ingredient": "Roasted peanuts add karo - crunch aur taste dono!",
        "backup_plan": "Dabba mein pack karke office le jao, healthy lunch!"
    }
]

# Enhanced YouTube Channel Data
YOUTUBE_COOKING_CHANNELS = {
    "hindi": [
        {
            "name": "Kabita's Kitchen",
            "specialty": "Ghar jaisa khana, simple recipes",
            "subscriber_count": "8.2M",
            "mom_favorite": True,
            "search_tip": "Sabse easy recipes yahan milenge!"
        },
        {
            "name": "Cook with Nisha Madhulika",
            "specialty": "Traditional recipes with modern touch",
            "subscriber_count": "12.1M", 
            "mom_favorite": True,
            "search_tip": "Mummy ki generation ki favorite!"
        },
        {
            "name": "Hebbar's Kitchen",
            "specialty": "Step by step, fool-proof recipes",
            "subscriber_count": "6.8M",
            "mom_favorite": True,
            "search_tip": "Beginners ke liye perfect!"
        },
        {
            "name": "Sanjeev Kapoor Khazana",
            "specialty": "Restaurant style recipes",
            "subscriber_count": "7.5M",
            "mom_favorite": False,
            "search_tip": "Professional chef tips!"
        },
        {
            "name": "Rajshri Food",
            "specialty": "Traditional Indian recipes",
            "subscriber_count": "4.2M",
            "mom_favorite": True,
            "search_tip": "Authentic desi recipes!"
        }
    ],
    "trending": [
        "CookingShooking",
        "Cook with Parul", 
        "Vahchef",
        "Tarla Dalal",
        "Cook with Monika"
    ]
}

# Desi Cooking Tips & Mom Psychology 😄
COOKING_TIPS = [
    "Namak kam se kaam chalega, zyada ho gaya toh aloo add karo!",
    "Oil bach raha hai? Fridge mein store karo, next time use karo!",
    "Masala burn ho gaya? Thoda paani add karo, bach jayega!",
    "Mummy ki mood check karo pehle, phir kitchen mein ghuso!",
    "Gas bill kam karna hai? Pressure cooker use karo, time bhi bachega!",
    "Kitchen clean rakho, mummy khush rahegi, compliments milenge!",
    "Leftover ko creative way mein use karo, waste nahi!"
]

ANGRY_MOM_EMERGENCY_PROTOCOLS = [
    {
        "situation": "Kitchen mess kar diya",
        "solution": "Immediately clean karo, sorry bolke hug do!",
        "backup": "Bol do 'Mummy main cooking passion develop kar raha hun!'"
    },
    {
        "situation": "Recipe fail ho gayi",
        "solution": "Order pizza, but bol do 'experimental cooking thi!'",
        "backup": "Next time mummy ke saath banayenge promise!"
    },
    {
        "situation": "Ingredients waste kar diye",
        "solution": "Immediately market ja ke same cheez la do!",
        "backup": "Math karo kitna waste hua, pocket money se de do!"
    }
]

# ADD BACK THE MISSING EXCUSE DATA! 😈
DESI_EXCUSES = {
    'ordering_food': [
        "Mummy, mere dost ka birthday hai, treat dena padega! 🎂",
        "Aaj office mein bahut kaam tha, haath dukh rahe hain cooking karne se 😫", 
        "Doctor ne kaha hai ki variety khana chahiye health ke liye! 👨‍⚕️",
        "Mummy aaj tum rest karo, main order kar deta hun! ❤️",
        "Gas cylinder khatam ho gaya hai, refill aane mein time lagega 🔥",
        "Neighbor aunty ne recommend kiya hai ye restaurant, try karna chahiye! 👵",
        "Mummy, kal se ghar ka khana khaunga, today cheat day! 😅",
        "Office ke colleagues ke saath team dinner hai, jana padega! 👔",
        "Mummy, bhai/sister ne saara achha khana kha liya! It's not fair! 😤",
        "I'm too weak from studying to cook, I might faint! Main toh gir jaunga! 🤒",
        "Cooking gas smells funny, safety first mummy! Better safe than sorry! ⚠️",
        "I was saving money by not eating lunch, so technically this is economical! 💰",
        "But Muuuum, everyone at work/college orders food on weekends! 😭",
        "It's educational - I'm studying different cuisines for... uh... general knowledge! 🌍"
    ],
    'going_out': [
        "Mummy, dost ke papa hospital mein hain, unke saath jana hai! 🏥",
        "Important project ka discussion hai, coffee shop mein meeting hai! ☕",
        "Bank ka kaam urgent tha, late ho gaya! 🏦", 
        "Traffic bahut zyada tha, isliye delay hua! 🚗",
        "Dost ka bike puncture ho gaya, help karne gaya tha! 🏍️",
        "Library mein group study thi, time ka pata nahi chala! 📚",
        "Festival shopping karne jana tha, crowd ki vajah se late hua! 🛍️",
        "Gym trainer ne extra session rakha tha! 💪",
        "Sibling said they saw my friend crying at the park, I need to check! 😢",
        "It's a character building exercise - independence training! 💪",
        "I'm conducting a social experiment for psychology class! 🧠",
        "Mummy, I was being responsible and checking the route for tomorrow's work! 🗺️",
        "Sibling dared me to come home early, I can't let them win! 😈",
        "I was helping an old aunty with her shopping, it took longer than expected! 👵",
        "But Muuuum, you always say I should be more social! 🤝",
        "I was walking really slowly to process all the important things I learned today! 🚶‍♂️"
    ],
    'late_night': [
        "Mummy, night shift mein overtime mila, extra paise! 💰",
        "Friend ka emergency tha, hospital drop karna pada! 🚨",
        "Last metro miss ho gayi, auto nahi mil rahi thi! 🚇",
        "Client call tha US se, time zone different hai! 🌍",
        "Project submission tomorrow hai, team ke saath kaam kar rahe the! 💻",
        "Cousin ki engagement surprise planning kar rahe the! 💍",
        "Phone battery dead ho gayi thi, call nahi kar saka! 🔋",
        "Ghar ke paas road block tha, construction work! 🚧",
        "Sibling locked me out as a prank! I had to wait for them to sleep! 😠",
        "I lost track of time because I was having such intellectual conversations! 🤓",
        "The clock at friend's house was broken, I didn't realize how late it was! ⏰",
        "There was a cat stuck in a tree, I couldn't just leave it there! 🐱",
        "Mummy, the sunset was so beautiful I got distracted appreciating nature! 🌅",
        "I was practicing mindful walking like you told me to! 🧘‍♂️",
        "But Muuuum, time flies when you're being a good friend! ⏰",
        "Office party thi, boss ke samne jane se mana nahi kar sakte the! 🎉"
    ],
    'buying_games': [
        "Mummy, ye educational game hai, programming sikhane ke liye! 💻",
        "Office stress kam karne ke liye doctor ne recommend kiya hai! 🧠",
        "Dost ke saath multiplayer khel kar communication skills badhenge! 🎮",
        "Ye game puzzle solving sikhata hai, brain development ke liye! 🧩",
        "Christmas offer hai, normal price se 70% kam! 💸",
        "Ye game reviews mein top rated hai, investment hai! ⭐",
        "Cousin ke birthday gift ke liye research kar raha tha! 🎁",
        "Ye strategy game hai, planning skills improve hote hain! 📈",
        "It's not fair! Everyone else has this game except me! 😤",
        "But mummy, this will teach me valuable life skills! 💡",
        "Sibling already has 5 games, I only have 2! Equal treatment please! ⚖️",
        "This game teaches teamwork and leadership qualities! 👥"
    ],
    'movie_date': [
        "Mummy, ye educational documentary hai, knowledge ke liye! 🎬",
        "Dost ka farewell hai, last time milne ja raha hun! 👋",
        "Office team building activity hai, compulsory attendance! 🏢",
        "Cultural program hai college mein, participate karna hai! 🎭",
        "Neighbor uncle ke ladke ki engagement hai, family function! 💒",
        "Library band hai, group study cafe mein kar rahe hain! 📖",
        "Blood donation camp mein volunteer kar raha hun! 🩸",
        "Photography exhibition dekh raha hun, hobby development! 📸",
        "It's a foreign language film, very educational for cultural understanding! 🌍",
        "The movie has historical significance, it's basically homework! 📚",
        "But mummy, you always say I should appreciate art and culture! 🎨"
    ],
    'gf_bf_date': [
        "Mummy, tuition padha raha hun junior ko, extra income! 📚💰",
        "Library partner ke saath assignment complete kar rahe hain! 👫",
        "Office colleague ka project help kar raha hun, networking! 🤝",
        "Cousin sister ke shopping mein help kar raha hun! 🛍️",
        "Friend ka interview hai, moral support ke liye saath gaya! 💼",
        "Group project presentation ki practice kar rahe hain! 👥",
        "Neighbor aunty ki beti ko career guidance de raha hun! 💡",
        "Study buddy ke saath competitive exam preparation! 📝",
        "We're working on a very important academic research project! 🔬",
        "It's a study group, mummy! Very serious academic discussions! 🤓",
        "I'm mentoring a junior student, building leadership skills! 👨‍🏫"
    ],
    'student_excuses': [
        "Mummy, teacher ne extra class rakhi hai, important topic! 👩‍🏫",
        "Library mein reference books chahiye the, submission tomorrow! 📚",
        "Group assignment ka discussion tha, marks important hain! 📊",
        "Lab practical complete karna tha, attendance compulsory! 🔬",
        "Scholarship form submit karna tha, deadline today! 📋",
        "Senior se notes lene gaya tha, exam preparation ke liye! 📖",
        "College fest ki meeting thi, participation zaroori hai! 🎪",
        "Placement training session attend karna tha! 💼",
        "Professor ne doubt clearing session rakha tha! 🤔",
        "Computer lab mein project work complete karna tha! 💻",
        "But mummy, education is the most important thing, right? 📚",
        "I was being a responsible student and helping my classmates! 🤝",
        "The teacher specifically asked for extra dedication from top students! ⭐",
        "I'm trying to be the best student I can be, just like you taught me! 💪"
    ]
}

GUILT_TRIP_RESPONSES = [
    "Haan mummy, aap right ho! Next time se aisa nahi hoga! 🙏",
    "Sorry mummy, main aapka precious beta hun na! 😇",
    "Mummy, aapne bachpan mein bhi aise hi mujhe sambhala hai! ❤️",
    "Main lucky hun ki aap jaisi mummy mili! 🍀",
    "Aap tension mat lo, main responsible ho gaya hun! 💪",
    "Mummy, aap bina toh main kuch nahi! You're the best! 👑",
    "Promise, ab se pehle batakar jaunga! 🤝",
    "Aapki baat always right hoti hai mummy! 💯",
    "Fine, but sibling never gets in trouble for anything! It's not fair! 😤",
    "I was just trying to be helpful! Next time I'll ask first! 🙏",
    "I promise I'm learning important life skills from these experiences! 💡",
    "You're the best mummy ever, that's why I feel safe telling you everything! ❤️",
    "I'll make it up to you by being extra good tomorrow! Starting after breakfast! 😇",
    "But mummy, you raised me to think for myself! I'm just being independent! 🤷‍♂️",
    "I was channeling all the good values you taught me! 📚",
    "Next time I'll bring sibling as my witness so you believe me! 👫",
    "But muuuum, I was just trying to be responsible! 😊"
]

# Enhanced Recipe Suggestions based on ingredients
RECIPE_SUGGESTIONS = [
    {
        "name": "Aloo Pyaz Ki Sabzi",
        "ingredients": ["aloo", "onion", "tomato", "oil", "namak", "haldi"],
        "difficulty": "Easy Peasy",
        "time": "20 minutes",
        "description": "Classic combination! Roti rice dono ke saath perfect!",
        "video_search": "aloo pyaz ki sabzi recipe",
        "mom_approval": "90%",
        "mom_tip": "Aloo ko cover karke pakao, jaldi soft ho jayega!"
    },
    {
        "name": "Egg Bhurji",
        "ingredients": ["eggs", "onion", "tomato", "hari mirch", "oil"],
        "difficulty": "Super Easy", 
        "time": "10 minutes",
        "description": "Quick protein fix! Bread ke saath amazing!",
        "video_search": "egg bhurji recipe indian style",
        "mom_approval": "85%",
        "mom_tip": "Slow flame pe banao, creamy texture milega!"
    },
    {
        "name": "Vegetable Maggi",
        "ingredients": ["maggi", "onion", "tomato", "capsicum", "corn"],
        "difficulty": "Beginner",
        "time": "12 minutes",
        "description": "Maggi with vegetables = guilt-free indulgence!",
        "video_search": "vegetable maggi recipe healthy",
        "mom_approval": "70%",
        "mom_tip": "Vegetables add karne se healthy lagta hai mummy ko!"
    },
    {
        "name": "Paneer Bhurji",
        "ingredients": ["paneer", "onion", "tomato", "hari mirch", "adrak"],
        "difficulty": "Medium",
        "time": "15 minutes",
        "description": "Restaurant style! Chapati ke saath royal feeling!",
        "video_search": "paneer bhurji recipe restaurant style",
        "mom_approval": "95%",
        "mom_tip": "Paneer fresh use karo, taste mein fark lagega!"
    },
    {
        "name": "Dal Tadka",
        "ingredients": ["dal", "onion", "tomato", "jeera", "hing", "haldi"],
        "difficulty": "Easy",
        "time": "25 minutes",
        "description": "Comfort food supreme! Rice ke saath heaven!",
        "video_search": "dal tadka recipe dhaba style",
        "mom_approval": "100%",
        "mom_tip": "Dal ko pressure cooker mein banao, time bachega!"
    },
    {
        "name": "Fried Rice",
        "ingredients": ["leftover rice", "eggs", "onion", "capsicum", "corn", "soy sauce"],
        "difficulty": "Easy",
        "time": "15 minutes",
        "description": "Leftover rice ka best use! Chinese restaurant feel!",
        "video_search": "egg fried rice recipe indian style",
        "mom_approval": "80%",
        "mom_tip": "Rice cold rakhke use karo, sticky nahi hoga!"
    },
    {
        "name": "Cheese Omelette",
        "ingredients": ["eggs", "cheese", "milk", "oil", "namak"],
        "difficulty": "Easy",
        "time": "8 minutes",
        "description": "Breakfast ka king! Bread ke saath perfect!",
        "video_search": "cheese omelette recipe fluffy",
        "mom_approval": "85%",
        "mom_tip": "Thoda milk add karo, fluffy banegi!"
    },
    {
        "name": "Aloo Paratha",
        "ingredients": ["aloo", "atta", "oil", "namak", "hari mirch"],
        "difficulty": "Medium",
        "time": "30 minutes",
        "description": "North Indian breakfast champion! Dahi ke saath epic!",
        "video_search": "aloo paratha recipe punjabi style",
        "mom_approval": "100%",
        "mom_tip": "Aloo mein jeera powder add karo, taste badh jayega!"
    },
    {
        "name": "Vegetable Pulao",
        "ingredients": ["rice", "onion", "tomato", "capsicum", "corn", "jeera"],
        "difficulty": "Medium",
        "time": "25 minutes",
        "description": "One pot wonder! Raita ke saath complete meal!",
        "video_search": "veg pulao recipe one pot",
        "mom_approval": "90%",
        "mom_tip": "Rice ko 15 min soak karo pehle!"
    },
    {
        "name": "Bread Upma",
        "ingredients": ["bread", "onion", "tomato", "hari mirch", "jeera"],
        "difficulty": "Easy",
        "time": "12 minutes",
        "description": "Leftover bread ka jugaad! South meets North!",
        "video_search": "bread upma recipe quick",
        "mom_approval": "75%",
        "mom_tip": "Bread ko small pieces mein cut karo!"
    },
    {
        "name": "Masala Chai",
        "ingredients": ["milk", "sugar", "adrak", "tea leaves"],
        "difficulty": "Easy",
        "time": "8 minutes",
        "description": "Mood fresh karne ka magic! Biscuit mandatory!",
        "video_search": "masala chai recipe perfect",
        "mom_approval": "100%",
        "mom_tip": "Adrak fresh use karo, powder nahi!"
    },
    {
        "name": "Poha",
        "ingredients": ["rice flakes", "onion", "aloo", "hari mirch", "jeera"],
        "difficulty": "Easy",
        "time": "15 minutes",
        "description": "Maharashtrian breakfast superstar! Light aur tasty!",
        "video_search": "poha recipe maharashtrian style",
        "mom_approval": "95%",
        "mom_tip": "Poha ko gently wash karo, toot nahi jaane chahiye!"
    },
    {
        "name": "Dahi Rice",
        "ingredients": ["leftover rice", "dahi", "namak", "jeera", "curry patta"],
        "difficulty": "Super Easy",
        "time": "10 minutes",
        "description": "South Indian comfort! Stomach ko cooling effect!",
        "video_search": "curd rice recipe south indian",
        "mom_approval": "90%",
        "mom_tip": "Dahi room temperature pe lao pehle!"
    },
    {
        "name": "Stuffed Paratha",
        "ingredients": ["atta", "aloo", "onion", "oil", "namak"],
        "difficulty": "Medium",
        "time": "35 minutes",
        "description": "Any stuffing works! Creativity ki limit nahi!",
        "video_search": "stuffed paratha recipe variety",
        "mom_approval": "95%",
        "mom_tip": "Rolling mein patient raho, jaldi nahi!"
    },
    {
        "name": "Vegetable Sandwich",
        "ingredients": ["bread", "onion", "tomato", "cucumber", "cheese"],
        "difficulty": "Beginner",
        "time": "10 minutes",
        "description": "Healthy aur quick! Office lunch ka perfect option!",
        "video_search": "veg sandwich recipe healthy",
        "mom_approval": "80%",
        "mom_tip": "Butter ki jagah olive oil use karo!"
    },
    {
        "name": "Simple Khichdi",
        "ingredients": ["rice", "dal", "haldi", "namak", "oil"],
        "difficulty": "Easy",
        "time": "20 minutes",
        "description": "Comfort food ultimate! Sick ho ya healthy, sab time perfect!",
        "video_search": "khichdi recipe simple moong dal",
        "mom_approval": "100%",
        "mom_tip": "Ghee daalke serve karo, taste double!"
    },
    {
        "name": "Instant Noodles Upgrade",
        "ingredients": ["maggi", "eggs", "onion", "capsicum", "cheese"],
        "difficulty": "Easy",
        "time": "15 minutes",
        "description": "Regular Maggi ko restaurant level banao!",
        "video_search": "maggi recipe restaurant style",
        "mom_approval": "60%",
        "mom_tip": "Vegetables add karo, mummy ko healthy lagega!"
    },
    {
        "name": "Mixed Vegetable Curry",
        "ingredients": ["onion", "tomato", "aloo", "capsicum", "corn"],
        "difficulty": "Medium",
        "time": "25 minutes",
        "description": "Sabzi leftover finish karne ka perfect way!",
        "video_search": "mix veg curry recipe indian",
        "mom_approval": "90%",
        "mom_tip": "Har sabzi ko alag time pe add karo!"
    },
    {
        "name": "Spicy Omelette",
        "ingredients": ["eggs", "onion", "hari mirch", "tomato", "dhania"],
        "difficulty": "Easy",
        "time": "10 minutes",
        "description": "Protein packed breakfast! Roti wrap banao!",
        "video_search": "masala omelette recipe indian",
        "mom_approval": "85%",
        "mom_tip": "Medium flame pe banao, burn nahi hona chahiye!"
    },
    {
        "name": "Quick Pasta",
        "ingredients": ["pasta", "onion", "tomato", "cheese", "oil"],
        "difficulty": "Easy",
        "time": "18 minutes",
        "description": "Italian meets Indian! Fusion ka magic!",
        "video_search": "pasta recipe indian style",
        "mom_approval": "70%",
        "mom_tip": "Pasta ko properly drain karo!"
    }
]

# ROUTES - Clean and no duplicates

@bp.route('/')
def index():
    """Main Mummy Pizza dashboard"""
    return render_template('mummy_i_want_pizza_at_home.html')

@bp.route('/recipes')
def recipes():
    """All-in-one recipe hub"""
    return render_template('mummy_pizza_recipes.html')

@bp.route('/horrid-henry-excuse-academy')
def horrid_henry_excuse_academy():
    """Horrid Henry's Excuse Academy"""
    return render_template('horrid_henry_excuse_academy.html')

# Redirect routes for backward compatibility
@bp.route('/bahana-generator')
def bahana_generator():
    """Redirect to Horrid Henry's Excuse Academy"""
    return redirect(url_for('mummy_pizza.horrid_henry_excuse_academy'))

@bp.route('/random-recipe')
def random_recipe_redirect():
    """Redirect to unified recipes page"""
    return redirect(url_for('mummy_pizza.recipes'))

@bp.route('/fridge-check')
def fridge_check_redirect():
    """Redirect to unified recipes page"""
    return redirect(url_for('mummy_pizza.recipes'))

@bp.route('/emergency-recipes')
def emergency_recipes_redirect():
    """Redirect to unified recipes page"""
    return redirect(url_for('mummy_pizza.recipes'))

# API ROUTES

@bp.route('/api/random-recipe')
def api_random_recipe():
    """API endpoint for random recipe with enhanced data"""
    recipe = random.choice(RANDOM_RECIPES)
    
    # Get video suggestions with enhanced data
    video_suggestions = get_enhanced_cooking_videos(recipe['video_search'], recipe.get('youtube_channels', []))
    
    # Add cooking tips
    cooking_tip = random.choice(COOKING_TIPS)
    
    return jsonify({
        'success': True,
        'recipe': recipe,
        'videos': video_suggestions,
        'cooking_tip': cooking_tip,
        'emergency_protocol': random.choice(ANGRY_MOM_EMERGENCY_PROTOCOLS)
    })

@bp.route('/api/generate-bahana')
def api_generate_bahana():
    """API to generate random excuse"""
    excuse_type = request.args.get('type', 'general')
    
    if excuse_type in DESI_EXCUSES:
        excuses = DESI_EXCUSES[excuse_type]
    else:
        # Mix all excuses
        all_excuses = []
        for category in DESI_EXCUSES.values():
            all_excuses.extend(category)
        excuses = all_excuses
    
    excuse = random.choice(excuses)
    guilt_response = random.choice(GUILT_TRIP_RESPONSES)
    
    return jsonify({
        'success': True,
        'excuse': excuse,
        'guilt_response': guilt_response,
        'type': excuse_type
    })

@bp.route('/api/suggest-recipes', methods=['POST'])
def api_suggest_recipes():
    """Enhanced recipe suggestions with detailed matching"""
    try:
        data = request.get_json()
        available_ingredients = data.get('ingredients', [])
        
        if not available_ingredients:
            return jsonify({
                'success': False,
                'error': 'No ingredients selected! Fridge empty hai kya? 😅'
            })
        
        matching_recipes = []
        partial_matches = []
        
        for recipe in RECIPE_SUGGESTIONS:
            recipe_ingredients = [ing.lower().strip() for ing in recipe['ingredients']]
            available_lower = [ing.lower().strip() for ing in available_ingredients]
            
            # Calculate matches
            matches = len(set(recipe_ingredients) & set(available_lower))
            match_percentage = (matches / len(recipe_ingredients)) * 100
            missing_ingredients = [
                ing for ing in recipe_ingredients 
                if ing not in available_lower
            ]
            
            recipe_copy = recipe.copy()
            recipe_copy['match_percentage'] = round(match_percentage)
            recipe_copy['missing_ingredients'] = missing_ingredients
            recipe_copy['available_ingredients'] = [
                ing for ing in recipe_ingredients 
                if ing in available_lower
            ]
            recipe_copy['videos'] = get_enhanced_cooking_videos(recipe['video_search'])
            
            # Categorize recipes
            if match_percentage >= 70:  # High match
                matching_recipes.append(recipe_copy)
            elif match_percentage >= 40:  # Partial match
                partial_matches.append(recipe_copy)
        
        # Sort by match percentage
        matching_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)
        partial_matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        # Combine results
        all_results = matching_recipes + partial_matches[:3]  # Top 3 partial matches
        
        return jsonify({
            'success': True,
            'recipes': all_results[:8],  # Top 8 total results
            'perfect_matches': len(matching_recipes),
            'partial_matches': len(partial_matches),
            'total_found': len(all_results),
            'cooking_tip': random.choice(COOKING_TIPS),
            'ingredient_suggestions': get_ingredient_suggestions(available_ingredients)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error finding recipes: {str(e)}'
        })

# HELPER FUNCTIONS

def get_cooking_videos(search_query, max_results=3):
    """Get cooking videos from web (mock function for now)"""
    # This would integrate with YouTube API in real implementation
    # For now, returning mock data
    
    mock_videos = [
        {
            "title": f"Easy {search_query.title()} - Step by Step",
            "channel": "Kabita's Kitchen",
            "duration": "8:45",
            "views": "2.3M views",
            "thumbnail": "https://picsum.photos/320/180",
            "url": f"https://youtube.com/search?q={search_query.replace(' ', '+')}"
        },
        {
            "title": f"Quick {search_query.title()} Recipe in Hindi",
            "channel": "Cook with Nisha",
            "duration": "6:20", 
            "views": "1.8M views",
            "thumbnail": "https://picsum.photos/320/180",
            "url": f"https://youtube.com/search?q={search_query.replace(' ', '+')}"
        },
        {
            "title": f"Restaurant Style {search_query.title()}",
            "channel": "Hebbar's Kitchen",
            "duration": "10:15",
            "views": "3.1M views", 
            "thumbnail": "https://picsum.photos/320/180",
            "url": f"https://youtube.com/search?q={search_query.replace(' ', '+')}"
        }
    ]
    
    return random.sample(mock_videos, min(max_results, len(mock_videos)))

def get_enhanced_cooking_videos(search_query, preferred_channels=None):
    """Get enhanced cooking videos with channel info"""
    
    if preferred_channels:
        channels = preferred_channels[:2]  # Use preferred channels
    else:
        # Get random popular channels
        all_channels = [ch['name'] for ch in YOUTUBE_COOKING_CHANNELS['hindi']]
        channels = random.sample(all_channels, 2)
    
    enhanced_videos = []
    
    for i, channel in enumerate(channels):
        # Find channel info
        channel_info = None
        for ch in YOUTUBE_COOKING_CHANNELS['hindi']:
            if ch['name'] == channel:
                channel_info = ch
                break
        
        video = {
            "title": f"{search_query.title()} - {['Easy', 'Perfect', 'Restaurant Style'][i]}",
            "channel": channel,
            "duration": f"{random.randint(5,12)}:{random.randint(10,59)}",
            "views": f"{random.uniform(1.2, 5.8):.1f}M views",
            "thumbnail": f"https://picsum.photos/320/180?random={i}",
            "url": f"https://youtube.com/results?search_query={search_query.replace(' ', '+')}"
        }
        
        if channel_info:
            video["mom_favorite"] = channel_info.get("mom_favorite", False)
            video["search_tip"] = channel_info.get("search_tip", "")
            video["specialty"] = channel_info.get("specialty", "")
        
        enhanced_videos.append(video)
    
    return enhanced_videos

def get_ingredient_suggestions(current_ingredients):
    """Suggest additional ingredients to get more recipes"""
    suggestions = []
    
    # Common combinations that unlock more recipes
    combo_suggestions = [
        {"add": ["eggs"], "unlocks": "protein-rich recipes"},
        {"add": ["cheese"], "unlocks": "comfort food recipes"},
        {"add": ["dal"], "unlocks": "healthy dal-based recipes"},
        {"add": ["atta"], "unlocks": "paratha and roti recipes"},
        {"add": ["jeera", "haldi"], "unlocks": "traditional Indian recipes"},
        {"add": ["garam masala"], "unlocks": "restaurant-style recipes"}
    ]
    
    current_lower = [ing.lower() for ing in current_ingredients]
    
    for combo in combo_suggestions:
        add_ingredients = [ing for ing in combo["add"] if ing.lower() not in current_lower]
        if add_ingredients:
            suggestions.append({
                "ingredients": add_ingredients,
                "benefit": combo["unlocks"]
            })
    
    return suggestions[:3]  # Top 3 suggestions