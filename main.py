from flask import Flask, request, redirect, render_template, send_file
from PIL import Image, ImageDraw, ImageFont, ImageOps
import datetime
import os
from flask.helpers import url_for

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/discord')
def discord():
    return render_template('discord.html')

@app.route('/tweet', methods=['GET', 'POST'])
def tweet():
    if request.method == 'POST':
        return redirect(url_for('generate_image'))
    return render_template('tweet.html', image_path=None)

@app.route('/generate', methods=['POST'])
def generate_image():
    image_file = request.files.get('image')
    if image_file:
        pfp = Image.open(image_file)
        pfp = pfp.resize((48, 48))
    else:
        pfp_path = 'pfp.png'
        pfp = Image.open(pfp_path)
        pfp = pfp.resize((48, 48))
    username = request.form['username']
    text = request.form['text']

    image = Image.new('RGB', (600, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    mask = Image.new("L", pfp.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, pfp.size[0], pfp.size[1]), fill=255)

    pfp = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
    pfp.putalpha(mask)

    image.paste(pfp, (10, 10), mask=pfp)

    font_username = ImageFont.truetype('arial.ttf', 18)
    font_timestamp = ImageFont.truetype('arial.ttf', 14)
    font_text = ImageFont.truetype('arial.ttf', 16)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    draw.text((68, 15), f'{username}', fill=(0, 0, 0), font=font_username)
    draw.text((68, 40), f'@{username}', fill=(101, 119, 134), font=font_username)

    draw.text((68, 70), text, fill=(0, 0, 0), font=font_text)

    timestamp = datetime.datetime.now().strftime('%I %p %d %B')
    draw.text((68, 124), f'{timestamp}', fill=(101, 119, 134), font=font_username)

    tweet_reaction = Image.open("static/tweet_reactions.png")
    tweet_reaction = tweet_reaction.resize((500, 50))
    reaction_position = (50, 125 + font_text.getsize(text)[1] + 5)
    image.paste(tweet_reaction, reaction_position)

    blue_tick_path = 'static/verified.png'
    blue_tick = Image.open(blue_tick_path)
    blue_tick_size = (24, 18)
    blue_tick = blue_tick.resize(blue_tick_size)
    username_width = font_username.getsize(username)[0]
    blue_tick_position = (68 + username_width + 5, 16)
    image.paste(blue_tick, blue_tick_position, mask=blue_tick)

    image_path = 'static/generated_tweet.png'
    image.save(image_path)
    
    return render_template('tweet.html', image_path=image_path)

@app.route('/download/<path:filename>', methods=['GET'])
def download_image(filename):
    return send_file(filename, as_attachment=True)



#hm



@app.route('/generate_discord', methods=['POST'])
def generate_discord():
    image_file = request.files.get('image')
    if image_file:
        pfp = Image.open(image_file)
        pfp = pfp.resize((48, 48))
    else:
        pfp_path = 'pfp.png'
        pfp = Image.open(pfp_path)
        pfp = pfp.resize((48, 48))
    username = request.form['username']
    text = request.form['text']

    image = Image.new('RGB', (600, 100), color=(54, 57, 63))
    draw = ImageDraw.Draw(image)

    mask = Image.new("L", pfp.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, pfp.size[0], pfp.size[1]), fill=255)

    pfp = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
    pfp.putalpha(mask)

    image.paste(pfp, (20, 20), mask=pfp)
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    today = f"today " + str(current_time) 
    font_username = ImageFont.truetype('arial.ttf', 18)
    font_text = ImageFont.truetype('arial.ttf', 16)
    font_date = ImageFont.truetype('arial.ttf', 13)

    draw.text((80, 20), f'{username}', fill=(255, 255, 255), font=font_username)
    draw.text((156, 25), today, fill=(255, 255, 255), font=font_date)
    draw.text((80, 45), text, fill=(255, 255, 255), font=font_text)

    image_path = 'static/generated_discord.png'
    image.save(image_path)

    return render_template('discord.html', image_path=image_path, username=username, text=text)

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(host='0.0.0.0', port=8080)

