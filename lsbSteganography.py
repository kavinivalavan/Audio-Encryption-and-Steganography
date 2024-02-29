from pydub import AudioSegment
import os
import wave

def convert_to_wav(input_file, output_file):
    # Check if the output file already exists
    if os.path.exists(output_file):
        print(f"The output file '{output_file}' already exists. Please remove it or choose a different output file.")
        return

    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Export the audio file as a wav file
    audio.export(output_file, format="wav")

def encode_aud_data(frame_bytes, data):
    # Encoding logic from code1
    data = data + '*^*^*'
    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(0, len(result), 1):
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res) - 4] == str(result[i]):
            frame_bytes[j] = (frame_bytes[j] & 253)  # 253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1

    return frame_bytes

def decode_aud_data(frame_bytes):
    extracted = ""
    p = 0
    for i in range(len(frame_bytes)):
        if p == 1:
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res) - 2] == '0':
            extracted += res[len(res) - 4]
        else:
            extracted += res[len(res) - 1]

        all_bytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                extracted = decoded_data[:-5]
                p = 1
                break

    return extracted


def aud_steg():
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY USING LSB")
        print("1. Encode the audio")
        print("2. Decode the audio")
        print("3. Exit")
        choice1 = int(input("Enter the Choice: "))
        if choice1 == 1:
            input_file = input("Enter name of the input file (with extension): ")
            output_file = input("Enter name of the stego file (with extension): ")

            # Check if the input file is not in WAV format, then convert it
            if not input_file.endswith('.wav'):
                converted_file = input("Enter the audio file path for the converted file: ")
                convert_to_wav(input_file, converted_file)
                input_file = converted_file

            song = wave.open(input_file, mode='rb')
            nframes = song.getnframes()
            frames = song.readframes(nframes)
            frame_list = list(frames)
            frame_bytes = bytearray(frame_list)

            data = input("\nEnter the secret message: ")
            frame_bytes = encode_aud_data(frame_bytes, data)

            with wave.open(output_file, 'wb') as fd:
                fd.setparams(song.getparams())
                fd.writeframes(frame_bytes)
            print("\nEncoded the data successfully in the audio file.")
            song.close()

        elif choice1 == 2:
            input_file = input("Enter name of the file to be decoded: ")
            # Check if the input file is not in WAV format, then convert it
            if not input_file.endswith('.wav'):
                converted_file = "converted_audio.wav"
                convert_to_wav(input_file, converted_file)
                input_file = converted_file

            song = wave.open(input_file, mode='rb')
            nframes = song.getnframes()
            frames = song.readframes(nframes)
            frame_list = list(frames)
            frame_bytes = bytearray(frame_list)

            extracted_data = decode_aud_data(frame_bytes)
            print("The Encoded data was: ", extracted_data)
            song.close()

        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
            print("\n")


