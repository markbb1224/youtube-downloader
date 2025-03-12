from flask import Flask, request, send_file, jsonify
import os
import yt_dlp

app = Flask(__name__)

# 設定下載資料夾
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "YouTube Downloader API is running!"

@app.route("/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url")
    format_type = data.get("format", "mp4")  # 預設下載 MP4

    if not url:
        return jsonify({"error": "請提供 YouTube 影片網址"}), 400

    try:
        ydl_opts = {
            "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s"
        }

        if format_type == "mp3":
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        else:
            ydl_opts["format"] = "bestvideo+bestaudio/best"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if format_type == "mp3":
                filename = filename.replace(".webm", ".mp3").replace(".mp4", ".mp3")

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
