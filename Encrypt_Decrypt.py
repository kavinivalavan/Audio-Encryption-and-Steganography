
import wave

def audio_to_binary(input_file, output_file):
    # Open the audio file
    print("Reading audio file...")
    with wave.open(input_file, 'rb') as audio_file:
        # Read audio data
        audio_data = audio_file.readframes(audio_file.getnframes())
        pcm_encoding = audio_file.getcomptype()
        sample_width = audio_file.getsampwidth()
        channels = audio_file.getnchannels()
        frame_rate = audio_file.getframerate()
    print("Finished reading audio file.")
    
    # Convert audio data to binary
    binary_data = bytearray(audio_data)
    
    print("Writing audio file...")
    # Write binary data to a file
    with open(output_file, 'wb') as binary_file:
        binary_file.write(binary_data)
    print("Wrote...")
    
if __name__ == "__main__":
    input_audio_file = 'encryptedaudio.wav'  # Replace with your audio file path
    output_binary_file = 'ToDecrypt.bin'  # Replace with your desired output file path

    audio_to_binary(input_audio_file, output_binary_file)


import wave

def binary_to_audio(input_binary_file, output_audio_file):
    # Read binary data from the file
    with open(input_binary_file, 'rb') as binary_file:
        binary_data = binary_file.read()

    # Assume 16-bit PCM encoding, 2 channels, and a sample rate of 44100 (adjust as needed)
    sample_width = 2
    channels = 2
    frame_rate = 44100

    # Create a new wave file for writing
    with wave.open(output_audio_file, 'wb') as audio_file:
        audio_file.setnchannels(channels)
        audio_file.setsampwidth(sample_width)
        audio_file.setframerate(frame_rate)
        audio_file.writeframes(binary_data)

if __name__ == "__main__":
    input_binary_file = 'decrypted.bin'  # Replace with your binary file path
    output_audio_file = 'decryptedaudio.wav'  # Replace with your desired output audio file path

    binary_to_audio(input_binary_file, output_audio_file)



from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key from a file
def load_key():
    return open("key.key", "rb").read()

# Encrypt a binary file
def encrypt_file(input_file, output_file, key):
    cipher_suite = Fernet(key)

    with open(input_file, "rb") as file:
        file_data = file.read()
        encrypted_data = cipher_suite.encrypt(file_data)

    with open(output_file, "wb") as file:
        file.write(encrypted_data)

# Decrypt a binary file
def decrypt_file(input_file, output_file, key):
    cipher_suite = Fernet(key)

    with open(input_file, "rb") as file:
        encrypted_data = file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)

    with open(output_file, "wb") as file:
        file.write(decrypted_data)

# Example usage
key = load_key()

# Encrypt a binary file
encrypt_file("ToEncrypt.bin", "encrypted.bin", key)

# Decrypt a binary file
decrypt_file("ToDecrypt.bin", "decrypted.bin", key)


