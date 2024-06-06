import librosa
import numpy as np

def time_stretch(data_path, metadata_path, rate=rand(0,3)):
    
    metadata = pd.read_csv(metadata_path)


    for index, row in metadata.iterrows():
        file_path = os.path.join(data_path, f"{row['Chord']}")
        y, sr = librosa.load(os.path.join(file_path), f".wav")
        y_stretch = librosa.effects.time_stretch(y, rate)
        librosa.output.write_wav(os.path.join(file_path), f"time_stretch.wav", y_stretch, sr)

def add_noise(data_path, metadata_path):

    metadata = pd.read_csv(metadata_path)


    for index, row in metadata.iterrows():
        file_path = os.path.join(data_path, f"{row['Chord']}")
        y, sr = librosa.load(os.path.join(file_path), f".wav")
        noise_amp = 0.005 * np.amax(y)
        noise = noise_amp * np.random.normal(size=y.shape)
        y_noisy = y + noise
        librosa.output.write_wav(os.path.join(file_path), f"noise.wav", y_noisy, sr)




