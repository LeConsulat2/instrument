import os
from pydub import AudioSegment


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
            print(f"Saved {output_file}")


# Step 3 - Convert MP4 to MP3 if needed
def convert_to_mp3(input_file):
    if input_file.endswith(".mp4"):
        audio = AudioSegment.from_file(input_file, "mp4")
        mp3_file = input_file.replace(".mp4", ".mp3")
        audio.export(mp3_file, format="mp3")
        return mp3_file
    return input_file


# Step 4 - Main function to process the audio file
def process_audio(input_file, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get the original file name
    original_file_name = os.path.basename(input_file)

    # Convert MP4 to MP3 if needed
    input_file = convert_to_mp3(input_file)

    # Separate the audio
    separate_audio(input_file, output_folder)

    # Save each stem as a separate MP3 file
    save_stems(output_folder, original_file_name)

    print(f"All stems saved in {output_folder}")


# Entry point for running the script
if __name__ == "__main__":
    # Request user input for the audio file path
    input_file = input("Enter the full path of the audio file (MP3 or MP4): ").strip()

    # Validate the input file path
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
    else:
        # Define the output folder (same location as the input file)
        output_folder = os.path.dirname(input_file)

        # Ask the user if they want to specify a different output folder
        custom_output = (
            input(
                f"Output will be saved in the same directory as the input file ({output_folder}). Do you want to specify a different output folder? (y/n): "
            )
            .strip()
            .lower()
        )

        if custom_output == "y":
            output_folder = input("Enter the full path of the output folder: ").strip()
            if not os.path.exists(output_folder):
                print(f"Creating output folder: {output_folder}")

        # Process the audio file
        process_audio(input_file, output_folder)
