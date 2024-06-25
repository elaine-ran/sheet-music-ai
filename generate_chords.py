import numpy as np
import pandas as pd
import soundfile as sf
import librosa
import os
import random

def load_isolated_notes(directory, csvpath):
    notes = {}
    df = pd.read_csv(csvpath)
    notes_names = df["Note"]
    for filename in os.listdir(directory):
        if filename.endswith(".wav") and "copy" not in filename:
            filepath = os.path.join(directory, filename)
            note, sr = librosa.load(filepath, sr=44100)
            note_name = df.loc[df['File Names'] == filename[:-4], 'Note'].values[0]
            notes[note_name] = note
    return notes

def align_and_sum_notes(isolated_notes, chosen_notes):
    # Find the peaks of the notes
    peaks = [np.argmax(np.abs(isolated_notes[note])) for note in chosen_notes]
    
    # Determine the minimum peak index and align all notes based on this
    min_peak = min(peaks)
    aligned_notes = []
    for peak, note in zip(peaks, chosen_notes):
        start_idx = peak - min_peak
        if start_idx < 0:
            aligned_note = np.pad(isolated_notes[note], (abs(start_idx), 0), 'constant')
        else:
            aligned_note = isolated_notes[note][start_idx:]
        aligned_notes.append(aligned_note)
    
    # Determine the minimum length of the aligned notes
    min_length = min(len(note) for note in aligned_notes)
    
    # Sum the aligned notes
    chord = np.sum([note[:min_length] for note in aligned_notes], axis=0)
    
    return chord
    
def generate_random_chords(isolated_notes, num_chords=5, min_notes=3, max_notes=3):

    df = pd.DataFrame()

    chords = []
    chords_notes = []
    file_names = []
    notes_1 = []
    notes_2 = []
    notes_3 = []
    note_names = list(isolated_notes.keys())

    for _ in range(num_chords):
        num_notes_in_chord = random.randint(min_notes, max_notes)
        chosen_notes = random.sample(note_names, num_notes_in_chord)

        chord = align_and_sum_notes(isolated_notes, chosen_notes)
        chords.append(chord)
        chords_notes.append(chosen_notes)
    
    for i in range(num_chords):
        file_names.append(f"chords_{i+1}")
        notes_1.append(chords_notes[i][0])
        notes_2.append(chords_notes[i][1])
        notes_3.append(chords_notes[i][2])


    
    df['File Names'] = file_names
    df['Note 1'] = notes_1
    df['Note 2'] = notes_2
    df['Note 3'] = notes_3
    df.to_csv('piano_chords.csv', index=False)

    return chords, chords_notes

def save_chords(chords, directory='generated_chords'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i, chord in enumerate(chords):
        sf.write(os.path.join(directory, f'chord_{i+1}.wav'), chord, 44100)

data_path = '/Users/elaineran/Desktop/summer-project/piano_notes/'
metadata_path = '/Users/elaineran/Desktop/summer-project/piano_notes.csv'

isolated_notes = load_isolated_notes(data_path,metadata_path)

num_chords = 10
chords, chords_notes = generate_random_chords(isolated_notes, num_chords)

    # Save the generated chords
save_chords(chords)
