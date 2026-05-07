import os
import numpy as np
import librosa
import pandas as pd
from tqdm import tqdm
import glob
import warnings
warnings.filterwarnings("ignore")

FEAT_DIR  = "extracted_features"
os.makedirs(FEAT_DIR, exist_ok=True)

TARGET_SR = 16000
N_MFCC    = 40
N_MELS    = 128
N_CHROMA  = 12

EMOTIONS_WE_USE = ["angry", "happy", "neutral", "sad"]

RAVDESS_MAP = {
    "01": "neutral", "02": "calm", "03": "happy", "04": "sad",
    "05": "angry",   "06": "fear", "07": "disgust", "08": "ps"
}

def get_emotion_from_filename(fpath):
    basename = os.path.basename(fpath)
    name, _  = os.path.splitext(basename)
    parts    = name.split("_")
    last     = parts[-1].lower()
    if last in EMOTIONS_WE_USE:
        return last
    if "-" in name and "_" in name:
        label_part = name.split("_")[-1].lower()
        if label_part in EMOTIONS_WE_USE:
            return label_part
    tokens = name.replace("_", "-").split("-")
    if len(tokens) >= 3 and tokens[2] in RAVDESS_MAP:
        emo = RAVDESS_MAP[tokens[2]]
        if emo in EMOTIONS_WE_USE:
            return emo
    return None

def load_audio(fpath):
    try:
        y, sr = librosa.load(fpath, sr=TARGET_SR, mono=True)
        return y, sr
    except Exception as e:
        print(f"  skip {fpath}: {e}")
        return None, None

def stretch_audio(y):
    return librosa.effects.time_stretch(y, rate=1.1)

def shift_pitch(y, sr):
    return librosa.effects.pitch_shift(y, sr=sr, n_steps=2)

def add_noise(y):
    noise = np.random.normal(0, 0.005, len(y))
    return (y + noise).astype(np.float32)

def extract_features(y, sr):
    mfccs    = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC).T, axis=0)
    chroma   = np.mean(librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=N_CHROMA).T, axis=0)
    mel      = np.mean(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS).T, axis=0)
    zcr      = np.mean(librosa.feature.zero_crossing_rate(y).T, axis=0)
    rolloff  = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr).T, axis=0)
    rms      = np.mean(librosa.feature.rms(y=y).T, axis=0)
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr).T, axis=0)
    return np.hstack([mfccs, chroma, mel, zcr, rolloff, rms, centroid])

def collect_files(root_folder):
    pairs     = []
    wav_files = glob.glob(os.path.join(root_folder, "**", "*.wav"), recursive=True)
    for fpath in wav_files:
        label = get_emotion_from_filename(fpath)
        if label is not None:
            pairs.append((fpath, label))
    return pairs

def run_pipeline():
    print("\n=== collecting files ===")
    all_files = []
    for d in ["data/training", "data/validation", "data/emodb/wav"]:
        if os.path.isdir(d):
            found = collect_files(d)
            print(f"  {d}: {len(found)} files")
            all_files.extend(found)
        else:
            print(f"  {d}: not found, skipping")

    all_files = [(p, l) for p, l in all_files if l in EMOTIONS_WE_USE]
    print(f"\ntotal usable files: {len(all_files)}")

    features_list = []
    labels_list   = []

    print("\n=== extracting features + augmenting ===")
    for fpath, label in tqdm(all_files, desc="processing"):
        y, sr = load_audio(fpath)
        if y is None:
            continue
        features_list.append(extract_features(y, sr))
        labels_list.append(label)
        try:
            features_list.append(extract_features(stretch_audio(y), sr))
            labels_list.append(label)
        except Exception:
            pass
        try:
            features_list.append(extract_features(shift_pitch(y, sr), sr))
            labels_list.append(label)
        except Exception:
            pass
        try:
            features_list.append(extract_features(add_noise(y), sr))
            labels_list.append(label)
        except Exception:
            pass

    X        = np.array(features_list, dtype=np.float32)
    y_labels = np.array(labels_list)

    print(f"\nfeature matrix shape: {X.shape}")
    print(f"label distribution:\n{pd.Series(y_labels).value_counts()}")

    np.save(os.path.join(FEAT_DIR, "X_all.npy"), X)
    np.save(os.path.join(FEAT_DIR, "y_all.npy"), y_labels)
    print(f"\nsaved to {FEAT_DIR}/")

if __name__ == "__main__":
    run_pipeline()
