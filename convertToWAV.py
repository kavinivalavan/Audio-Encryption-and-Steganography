from pydub import AudioSegment
import os

def convert_to_wav(input_file, output_file):
    # Check if the output file already exists
    if os.path.exists(output_file):
        print(f"The output file '{output_file}' already exists. Please remove it or choose a different output file.")
        return

    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Export the audio file as a wav file
    audio.export(output_file, format="wav")

input_file = "BlueandGreyMPEG.mpeg"
output_file = "BlueandGreyWAV.wav"


convert_to_wav(input_file, output_file)
