from flask import Flask, request, render_template, send_from_directory
import os
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def upload_form():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        process_audio(file_path)
        return send_from_directory(UPLOAD_FOLDER, file.filename)
    return "No file uploaded", 400


def process_audio(input_file):
    output_folder = os.path.dirname(input_file)
    original_file_name = os.path.basename(input_file)
    input_file = convert_to_mp3(input_file)
    separate_audio(input_file, output_folder)
    save_stems(output_folder, original_file_name)


def convert_to_mp3(input_file):
    if input_file.endswith(".mp4"):
        audio = AudioSegment.from_file(input_file, "mp4")
        mp3_file = input_file.replace(".mp4", ".mp3")
        audio.export(mp3_file, format="mp3")
        return mp3_file
    return input_file


def separate_audio(input_file, output_folder):
    os.system(
        f'spleeter separate -i "{input_file}" -p spleeter:5stems -o "{output_folder}"'
    )


def save_stems(output_folder, original_file_name):
    stem_names = ["vocals", "drums", "bass", "piano", "other"]
    base_name = os.path.splitext(original_file_name)[0]
    stems_folder = os.path.join(output_folder, base_name)
    for stem in stem_names:
        stem_file_path = os.path.join(stems_folder, f"{stem}.wav")
        if os.path.exists(stem_file_path):
            stem_audio = AudioSegment.from_file(stem_file_path)
            output_file = os.path.join(output_folder, f"{base_name}-{stem}.mp3")
            stem_audio.export(output_file, format="mp3")


if __name__ == "__main__":
    app.run(debug=True)
