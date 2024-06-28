from flask import Flask, request, render_template, send_file
from pytube import YouTube
import instaloader
import os

app = Flask(__name__)

DEFAULT_SAVE_PATH = "C:\\Users\\Krishna\\Desktop\\Python Project"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form['quality']
    save_path = request.form['directory'].strip()
    platform = request.form['platform']

    if not save_path:
        save_path = DEFAULT_SAVE_PATH

    if not os.path.exists(save_path):
        return "The specified directory does not exist."

    if platform == "youtube":
        yt = YouTube(url)

        if quality == "highest":
            stream = yt.streams.get_highest_resolution()
        elif quality == "lowest":
            stream = yt.streams.get_lowest_resolution()
        else:
            stream = yt.streams.filter(res=quality).first()

        if stream:
            file_path = stream.download(output_path=save_path)
            return send_file(file_path, as_attachment=True, download_name=yt.title + ".mp4")
        else:
            return "The requested quality is not available."
    elif platform == "instagram":
        loader = instaloader.Instaloader()
        try:
            post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
            loader.download_post(post, target=save_path)
            return "Instagram Reel downloaded successfully."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return "Unsupported platform."

if __name__ == '__main__':
    app.run(debug=True)
