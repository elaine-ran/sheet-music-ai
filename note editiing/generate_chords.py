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

def find_note_start(note, threshold=0.01):
    """
    Find the start index of a note where the signal first exceeds a given threshold.
    """
    for i, value in enumerate(note):
        if np.abs(value) > threshold:
            return i
    return len(note)  # Return the end if no value exceeds the threshold

def align_and_sum_notes(isolated_notes, chosen_notes):
    # Find the start index of each note
    starts = [find_note_start(isolated_notes[note]) for note in chosen_notes]
    
    # Determine the earliest start index
    earliest_start = min(starts)
    
    # Align each note to the earliest start index
    aligned_notes = []
    for start, note in zip(starts, chosen_notes):
        start_idx = start - earliest_start
        if start_idx < 0:
            aligned_note = np.pad(isolated_notes[note], (abs(start_idx), 0), 'constant')
        else:
            aligned_note = isolated_notes[note][start_idx:]
        aligned_notes.append(aligned_note)
    
    # Determine the minimum length of the aligned notes
    min_length = min(len(note) for note in aligned_notes)
    
    # Trim all aligned notes to the minimum length
    aligned_notes = [note[:min_length] for note in aligned_notes]
    
    # Sum the aligned notes
    chord = np.sum(aligned_notes, axis=0)
    
    return chord
    
def generate_random_chords(isolated_notes, num_chords, min_notes=2, max_notes=8):
    df = pd.DataFrame()

    chords = []
    chords_notes = []
    file_names = []
    num_notes = []
    note_names = list(isolated_notes.keys())

    for _ in range(num_chords):
        num_notes_in_chord = random.randint(min_notes, max_notes)
        chosen_notes = random.sample(note_names, num_notes_in_chord)

        chord = align_and_sum_notes(isolated_notes, chosen_notes)
        chords.append(chord)
        chords_notes.append(chosen_notes)
        file_names.append(f"chord_{_+1}")
        num_notes.append(num_notes_in_chord)
    
    # Prepare the DataFrame columns
    df['File Names'] = file_names
    df['Number of Notes'] = num_notes
    
    # Create columns for notes
    for i in range(1, 9):
        df[f'Note {i}'] = [chords_notes[j][i-1] if i <= len(chords_notes[j]) else '' for j in range(num_chords)]
    
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

num_chords = 1000
chords, chords_notes = generate_random_chords(isolated_notes, num_chords)

    # Save the generated chords
save_chords(chords)
