import lsbFinal
import fmFinal
import wave
import numpy as np
from pydub import AudioSegment
import os
while True:
    print("\n\t\tAUDIO STEGANOGRAPHY")
    print("1. Using LSB Technique")
    print("2. Using Frequency Modulation")
    print("3. Exit")
    ch= int(input("Enter your choice:"))
    if ch==1:
        lsbFinal.aud_steg()
    elif ch==2:
        fmFinal.aud_stg_fm()
    elif ch==3:
        break
    else:
        print("Invalid choice")