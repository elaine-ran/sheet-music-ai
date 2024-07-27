import os
import librosa
import numpy as np
import pandas as pd
import random
import soundfile as sf


def time_stretch(data_path, metadata_path, copynum, rate=None):
    if rate is None:
        rate = random.uniform(0.1, 3.0)

    metadata = pd.read_csv(metadata_path)

    for index, row in metadata.iterrows():
        file_path = os.path.join(data_path, row['Chord'])
        if "copy" not in file_path:
            y, sr = librosa.load(file_path + ".wav")
            y_stretch = librosa.effects.time_stretch(y, rate=rate)
            output_path = f"{file_path} copy {copynum}.wav"
            sf.write(output_path, y_stretch, sr)

def add_noise(data_path, metadata_path, copynum):

    metadata = pd.read_csv(metadata_path)


    for index, row in metadata.iterrows():
        file_path = os.path.join(data_path, f"{row['Chord']}")
        if "copy" not in file_path:
            y, sr = librosa.load(file_path+".wav")
            noise_amp = 0.005 * np.amax(y)
            noise = noise_amp * np.random.normal(size=y.shape)
            y_noisy = y + noise
            output_path = f"{file_path} copy {copynum}.wav"
            sf.write(output_path, y_noisy, sr)

def time_stretch_and_add_noise(data_path, metadata_path, copynum, rate=random.uniform(0.1, 3.0)):
        
        metadata = pd.read_csv(metadata_path)
    
    
        for index, row in metadata.iterrows():
            file_path = os.path.join(data_path, f"{row['Chord']}")
            if "copy" not in file_path:
                y, sr = librosa.load(file_path+".wav")
                noise_amp = 0.005 * np.amax(y)
                noise = noise_amp * np.random.normal(size=y.shape)
                y_noisy = y + noise
                y_stretch = librosa.effects.time_stretch(y_noisy, rate=rate)
                output_path = f"{file_path} copy {copynum}.wav"
                sf.write(output_path, y_stretch, sr)



