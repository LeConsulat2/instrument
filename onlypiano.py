import os
from pydub import AudioSegment
import streamlit as st


# Step 1 - Separate the audio into different stems using Spleeter
def separate_audio(input_file, output_folder):
    os.system(
        f'spleeter separate -i "{input_file}" -p spleeter:5stems -o "{output_folder}"'
    )


# Step 2 - Save each stem as a separate MP3
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
            st.write(f"Saved {output_file}")


def convert_to_mp3(input_file):
    if input_file.endswith(".mp4"):
        audio = AudioSegment.from_file(input_file, "mp4")
        mp3_file = input_file.replace(".mp4", ".mp3")
        audio.export(mp3_file, format="mp3")
        return mp3_file
    return input_file


# Step 4 - Main function to process the audio file
def process_audio(input_file):
    # Define output_folder (same location as the input file)
    output_folder = os.path.dirname(input_file)
    original_file_name = os.path.basename(input_file)

    # Convert MP4 to MP3 if needed
    input_file = convert_to_mp3(input_file)

    # Separate the audio
    separate_audio(input_file, output_folder)

    # Save each stem as a separate MP3 file
    save_stems(output_folder, original_file_name)

    st.success(f"All stems saved in {output_folder}")


# Streamlit Interface
st.title("Audio Stem Separator")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "mp4"])

if uploaded_file is not None:
    save_path = os.path.join("uploads", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} uploaded successfully!")
    if st.button("Process Audio"):
        with st.spinner("Processing..."):
            process_audio(save_path)
