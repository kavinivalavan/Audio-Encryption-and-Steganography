import wave
import numpy as np
from pydub import AudioSegment
import os

def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

def convert_to_wav(input_file, output_file):
    if os.path.exists(output_file):
        print(f"The output file '{output_file}' already exists. Please remove it or choose a different output file.")
        return

    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")

def encode_audio(input_audio_file, output_audio_file, secret_message):
    binary_message = text_to_binary(secret_message)
    audio = wave.open(input_audio_file, 'rb')
    params = audio.getparams()
    frames = audio.readframes(-1)
    audio.close()

    frames_array = np.frombuffer(frames, dtype=np.int16)
    max_amplitude = np.max(np.abs(frames_array))

    encoded_frames = []
    bit_index = 0

    for frame in frames_array:
        if bit_index < len(binary_message):
            binary_bit = int(binary_message[bit_index])
            new_frame = frame + binary_bit * max_amplitude  # Modulate frequency based on the bit
            bit_index += 1
        else:
            new_frame = frame
        encoded_frames.append(new_frame)

    encoded_audio = wave.open(output_audio_file, 'wb')
    encoded_audio.setparams(params)
    encoded_audio.writeframes(np.array(encoded_frames, dtype=np.int16))
    encoded_audio.close()

def decode_audio(encoded_audio_file):
    encoded_audio = wave.open(encoded_audio_file, 'rb')
    frames = np.frombuffer(encoded_audio.readframes(-1), dtype=np.int16)
    encoded_audio.close()

    binary_message = ''
    max_amplitude = np.max(np.abs(frames))

    for frame in frames:
        bit = int((frame / max_amplitude + 1) / 2)  # Demodulate frequency to extract bit
        binary_message += str(bit)

    decoded_text = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        decoded_text += chr(int(byte, 2))

    return decoded_text

def aud_stg_fm():
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY USING FM")
        print("1. Encode the audio")
        print("2. Decode the audio")
        print("3. Exit")
        choice1 = int(input("Enter the Choice: "))
        if choice1 == 1:
            input_audio_file = input("Enter the input audio file path: ")
            output_audio_file = input("Enter the output audio file path: ")

            if not input_audio_file.endswith('.wav'):
                print("Converting the input audio file to WAV format...")
                temp_wav_file = input("Enter the audio file path for the converted file: ")
                convert_to_wav(input_audio_file, temp_wav_file)
                input_audio_file = temp_wav_file

            secret_message = input("Enter the message to encode: ")

            encode_audio(input_audio_file, output_audio_file, secret_message)
            print(f'Secret message encoded in audio file: {output_audio_file}')
        elif choice1 == 2:
            input_file = input("Enter name of the file to be decoded: ")
            decoded_message = decode_audio(input_file)
            print(f'Decoded secret message: {decoded_message}')
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
            print("\n")
