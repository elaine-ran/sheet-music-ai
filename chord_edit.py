import os
import librosa
import numpy as np
import pandas as pd
import random
import soundfile as sf

def time_stretch(data_path, metadata_path, copynum, rate=random.uniform(0.1, 3.0)):
    
    metadata = pd.read_csv(metadata_path)


    for index, row in metadata.iterrows():
        file_path = os.path.join(data_path, f"{row['Chord']}")
        y, sr = librosa.load(file_path+".wav")
        y_stretch = librosa.effects.time_stretch(y, rate=rate)
        if copynum == 1:
            sf.write(file_path+" copy.wav", y_stretch, sr)
        else:
            sf.write(file_path+" copy "+copynum+".wav", y_stretch, sr)

def add_noise(data_path, metadata_path, copynum):

    metadata = pd.read_csv(metadata_path)


    for index, row in metadata.iterrows():
        file_path = os.path.join(data_path, f"{row['Chord']}")
        y, sr = librosa.load(file_path+".wav")
        noise_amp = 0.005 * np.amax(y)
        noise = noise_amp * np.random.normal(size=y.shape)
        y_noisy = y + noise
        sf.write(os.path.join(file_path, f"copy {copynum}.wav"), y_noisy, sr)

def time_stretch_and_add_noise(data_path, metadata_path, copynum, rate=random.uniform(0.1, 3.0)):
        
        metadata = pd.read_csv(metadata_path)
    
    
        for index, row in metadata.iterrows():
            file_path = os.path.join(data_path, f"{row['Chord']}")
            y, sr = librosa.load(file_path+".wav")
            noise_amp = 0.005 * np.amax(y)
            noise = noise_amp * np.random.normal(size=y.shape)
            y_noisy = y + noise
            y_stretch = librosa.effects.time_stretch(y_noisy, rate=rate)
            sf.write(os.path.join(file_path, f"copy {copynum}.wav"), y_stretch, sr)



