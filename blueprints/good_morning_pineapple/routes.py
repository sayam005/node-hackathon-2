from flask import Blueprint, render_template, request, jsonify, send_file
import requests
import random
import os
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from .data import (DESI_FAMILY_QUOTES, EXTRA_CRINGE_QUOTES, FESTIVAL_QUOTES, 
                  MOTIVATIONAL_QUOTES, ENGLISH_QUOTES, IMAGE_CATEGORIES, 
                  FALLBACK_IMAGES)

# Create blueprint for good morning feature
bp = Blueprint('good_morning_pineapple', __name__, url_prefix='/good-morning-pineapple')

@bp.route('/')
def index():
    return render_template('good_morning_pineapple.html')

@bp.route('/api/generate-wish')
def generate_wish():
    # Get category from request
    category = request.args.get('category', 'desi')
    
    # For English quotes, use API; for others, use manual
    if category == 'english':
        quote_data = get_api_quote()
    else:
        quote_data = get_manual_quote(category)
    
    # Get base image for the category
    base_image_url = get_image_for_category(category)
    
    # Create image with text overlay
    final_image_data = create_image_with_text(base_image_url, quote_data, category)
    
    return jsonify({
        'quote': quote_data['text'] if isinstance(quote_data, dict) else quote_data,
        'author': quote_data.get('author', '') if isinstance(quote_data, dict) else '',
        'image_data': final_image_data,
        'category': category,
        'status': 'success'
    })

def get_manual_quote(category):
    """Get manually curated quotes based on category"""
    if category == 'festival':
        return {'text': random.choice(FESTIVAL_QUOTES)}
    elif category == 'motivational':
        return {'text': random.choice(MOTIVATIONAL_QUOTES)}
    elif category == 'cringe':
        return {'text': random.choice(EXTRA_CRINGE_QUOTES)}
    else:  # desi or default
        return {'text': random.choice(DESI_FAMILY_QUOTES)}

def get_api_quote():
    """Get random quotes from external APIs for English category"""
    try:
        # Try quotable.io first
        response = requests.get('https://api.quotable.io/random?minLength=50&maxLength=150', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'text': data['content'],
                'author': data['author']
            }
    except Exception as e:
        print(f"Quotable API error: {e}")
    
    try:
        # Try zenquotes as backup
        response = requests.get('https://zenquotes.io/api/random', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'text': data[0]['q'],
                'author': data[0]['a']
            }
    except Exception as e:
        print(f"ZenQuotes API error: {e}")
    
    # If all APIs fail, use manual English quotes as fallback
    quote_obj = random.choice(ENGLISH_QUOTES)
    return {
        'text': quote_obj['quote'],
        'author': quote_obj['author']
    }

def get_image_for_category(category):
    """Get images using more reliable sources"""
    try:
        random_num = random.randint(1, 10000)
        
        # Try multiple reliable image sources
        image_urls = [
            # Lorem Picsum - very reliable
            f"https://picsum.photos/800/600?random={random_num}",
            f"https://picsum.photos/800/600?random={random_num + 1}",
            f"https://picsum.photos/800/600?random={random_num + 2}",
            # Unsplash source (simplified)
            f"https://source.unsplash.com/800x600/?nature&sig={random_num}",
            f"https://source.unsplash.com/800x600/?landscape&sig={random_num}",
            f"https://source.unsplash.com/800x600/?flowers&sig={random_num}",
            # Try featured images
            f"https://source.unsplash.com/featured/800x600/?nature&sig={random_num}",
        ]
        
        # Shuffle to get variety
        random.shuffle(image_urls)
        
        for url in image_urls[:3]:  # Try first 3 URLs
            try:
                print(f"Trying to fetch image from: {url}")
                response = requests.get(url, timeout=8, allow_redirects=True)
                if response.status_code == 200 and len(response.content) > 5000:
                    print(f"Successfully fetched image from: {url}")
                    return response.content
            except Exception as e:
                print(f"Error fetching from {url}: {e}")
                continue
                
    except Exception as e:
        print(f"Image fetch error: {e}")
    
    print("All image sources failed, creating fallback gradient")
    return create_fallback_image(category)

def create_fallback_image(category):
    """Create a simple gradient background if no image is available"""
    img = Image.new('RGB', (800, 600))
    draw = ImageDraw.Draw(img)
    
    # Different colors for different categories
    colors = {
        'desi': [(255, 193, 7), (255, 87, 34)],  # Orange gradient
        'festival': [(156, 39, 176), (233, 30, 99)],  # Purple-pink
        'motivational': [(33, 150, 243), (76, 175, 80)],  # Blue-green
        'cringe': [(255, 193, 7), (255, 235, 59)],  # Yellow gradient
        'english': [(63, 81, 181), (103, 58, 183)]  # Blue-purple
    }
    
    start_color = colors.get(category, colors['desi'])[0]
    end_color = colors.get(category, colors['desi'])[1]
    
    # Create gradient
    for y in range(600):
        ratio = y / 600
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line([(0, y), (800, y)], fill=(r, g, b))
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=90)
    return img_byte_arr.getvalue()

def get_font_with_emoji_support():
    """Try to get a font that supports emojis, with fallbacks"""
    font_options = [
        # Windows fonts with emoji support
        ("C:/Windows/Fonts/seguiemj.ttf", 24, 18),  # Segoe UI Emoji
        ("C:/Windows/Fonts/arial.ttf", 26, 18),     # Arial
        ("C:/Windows/Fonts/calibri.ttf", 26, 18),   # Calibri
        # macOS fonts
        ("/System/Library/Fonts/Apple Color Emoji.ttc", 24, 18),
        ("/System/Library/Fonts/Arial.ttf", 26, 18),
        # Linux fonts
        ("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 24, 18),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26, 18),
        # Basic fonts
        ("arial.ttf", 26, 18),
        ("calibri.ttf", 26, 18),
    ]
    
    for font_path, title_size, author_size in font_options:
        try:
            title_font = ImageFont.truetype(font_path, title_size)
            author_font = ImageFont.truetype(font_path, author_size)
            return title_font, author_font
        except (OSError, IOError):
            continue
    
    # Fallback to default
    return ImageFont.load_default(), ImageFont.load_default()

def create_image_with_text(image_data, quote_data, category):
    """Create image with text overlay and return as base64"""
    try:
        # Handle both URL and byte data
        if isinstance(image_data, str):
            response = requests.get(image_data, timeout=10)
            img_bytes = response.content
        else:
            img_bytes = image_data
            
        img = Image.open(io.BytesIO(img_bytes))
        
        # Resize image to standard size
        img = img.resize((800, 600), Image.Resampling.LANCZOS)
        
        # Create a darker semi-transparent overlay for better text visibility
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 150))
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        
        # Create drawing context
        draw = ImageDraw.Draw(img)
        
        # Get quote text and author
        if isinstance(quote_data, dict):
            quote_text = quote_data['text']
            author = quote_data.get('author', '')
        else:
            quote_text = quote_data
            author = ''
        
        # Get fonts with emoji support
        title_font, author_font = get_font_with_emoji_support()
        
        # Text wrapping function
        def wrap_text(text, font, max_width):
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                try:
                    # Use textbbox for more accurate measurements
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    text_width = bbox[2] - bbox[0]
                except:
                    try:
                        if hasattr(draw, 'textlength'):
                            text_width = draw.textlength(test_line, font=font)
                        else:
                            text_width = draw.textsize(test_line, font=font)[0]
                    except:
                        text_width = len(test_line) * 12
                
                if text_width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            return lines
        
        # Wrap the quote text (keep emojis!)
        max_width = img.width - 120
        wrapped_lines = wrap_text(quote_text, title_font, max_width)
        
        # Calculate total text height
        line_height = 40
        total_text_height = len(wrapped_lines) * line_height
        if author:
            total_text_height += 60
        
        # Starting Y position (center the text block)
        start_y = (img.height - total_text_height) // 2
        
        # Draw each line of the quote
        current_y = start_y
        for line in wrapped_lines:
            # Get text dimensions for centering
            try:
                bbox = draw.textbbox((0, 0), line, font=title_font)
                text_width = bbox[2] - bbox[0]
            except:
                try:
                    if hasattr(draw, 'textlength'):
                        text_width = draw.textlength(line, font=title_font)
                    else:
                        text_width = draw.textsize(line, font=title_font)[0]
                except:
                    text_width = len(line) * 15
                
            text_x = (img.width - text_width) // 2
            
            # Draw text with thick stroke for better visibility
            stroke_width = 3
            for adj_x in range(-stroke_width, stroke_width + 1):
                for adj_y in range(-stroke_width, stroke_width + 1):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((text_x + adj_x, current_y + adj_y), line, 
                                font=title_font, fill='black')
            
            # Draw main text in white (this should show emojis better)
            draw.text((text_x, current_y), line, font=title_font, fill='white')
            current_y += line_height
        
        # Draw author if available
        if author:
            author_text = f"— {author}"
            try:
                bbox = draw.textbbox((0, 0), author_text, font=author_font)
                author_width = bbox[2] - bbox[0]
            except:
                try:
                    if hasattr(draw, 'textlength'):
                        author_width = draw.textlength(author_text, font=author_font)
                    else:
                        author_width = draw.textsize(author_text, font=author_font)[0]
                except:
                    author_width = len(author_text) * 10
                
            author_x = (img.width - author_width) // 2
            author_y = current_y + 20
            
            # Draw author with stroke
            stroke_width = 2
            for adj_x in range(-stroke_width, stroke_width + 1):
                for adj_y in range(-stroke_width, stroke_width + 1):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((author_x + adj_x, author_y + adj_y), author_text, 
                                font=author_font, fill='black')
            
            # Draw main author text in gold
            draw.text((author_x, author_y), author_text, font=author_font, fill='#FFD700')
        
        # Convert to RGB and save to bytes
        img = img.convert('RGB')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        
        # Convert to base64 for embedding in HTML
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{img_base64}"
        
    except Exception as e:
        print(f"Error creating image with text: {e}")
        return create_simple_text_image(quote_data, category)

def create_simple_text_image(quote_data, category):
    """Create a simple text image as fallback"""
    colors = {
        'desi': '#FF9800',
        'festival': '#E91E63',
        'motivational': '#2196F3',
        'cringe': '#FFEB3B',
        'english': '#9C27B0'
    }
    
    background_color = colors.get(category, '#667eea')
    
    img = Image.new('RGB', (800, 600), color=background_color)
    draw = ImageDraw.Draw(img)
    
    # Get quote text
    if isinstance(quote_data, dict):
        quote_text = quote_data['text']
        author = quote_data.get('author', '')
    else:
        quote_text = quote_data
        author = ''
    
    # Get fonts with emoji support
    font, author_font = get_font_with_emoji_support()
    
    # Simple text wrapping
    words = quote_text.split()
    lines = []
    current_line = []
    max_words_per_line = 8
    
    for i, word in enumerate(words):
        current_line.append(word)
        if len(current_line) >= max_words_per_line or i == len(words) - 1:
            lines.append(' '.join(current_line))
            current_line = []
    
    # Draw text
    y = 180
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            try:
                if hasattr(draw, 'textlength'):
                    text_width = draw.textlength(line, font=font)
                else:
                    text_width = len(line) * 11
            except:
                text_width = len(line) * 11
            
        x = (800 - text_width) // 2
        
        # Draw with stroke
        stroke_width = 2
        for adj in range(-stroke_width, stroke_width + 1):
            for adj2 in range(-stroke_width, stroke_width + 1):
                if adj != 0 or adj2 != 0:
                    draw.text((x + adj, y + adj2), line, font=font, fill='black')
        
        draw.text((x, y), line, font=font, fill='white')
        y += 35
    
    # Draw author
    if author:
        author_text = f"— {author}"
        try:
            bbox = draw.textbbox((0, 0), author_text, font=author_font)
            author_width = bbox[2] - bbox[0]
        except:
            try:
                if hasattr(draw, 'textlength'):
                    author_width = draw.textlength(author_text, font=author_font)
                else:
                    author_width = len(author_text) * 8
            except:
                author_width = len(author_text) * 8
            
        author_x = (800 - author_width) // 2
        
        # Draw with stroke
        stroke_width = 2
        for adj in range(-stroke_width, stroke_width + 1):
            for adj2 in range(-stroke_width, stroke_width + 1):
                if adj != 0 or adj2 != 0:
                    draw.text((author_x + adj, y + 20 + adj2), author_text, font=author_font, fill='black')
        
        draw.text((author_x, y + 20), author_text, font=author_font, fill='#FFD700')
    
    # Convert to base64
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=90)
    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_base64}"