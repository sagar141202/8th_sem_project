import os
import pickle
import numpy as np
import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import gradio as gr
import tensorflow as tf
import warnings
warnings.filterwarnings("ignore")

MODEL_PATH   = "results/cnn_lstm_model.keras"
SCALER_PATH  = "scaler.pkl"
ENCODER_PATH = "label_encoder.pkl"

TARGET_SR = 16000
N_MFCC    = 40
N_MELS    = 128
N_CHROMA  = 12

print("loading CNN-LSTM model...")
model = tf.keras.models.load_model(MODEL_PATH)
with open(SCALER_PATH,  "rb") as f: scaler = pickle.load(f)
with open(ENCODER_PATH, "rb") as f: enc    = pickle.load(f)

EMO_COLORS = {
    "angry":   "#ef4444",
    "happy":   "#f59e0b",
    "neutral": "#7F77DD",
    "sad":     "#3b82f6"
}
EMO_EMOJI = {"angry": "[ANGRY]", "happy": "[HAPPY]", "neutral": "[NEUTRAL]", "sad": "[SAD]"}

print(f"ready — classes: {enc.classes_}")

def get_features(y, sr):
    mfccs    = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC).T, axis=0)
    chroma   = np.mean(librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=N_CHROMA).T, axis=0)
    mel      = np.mean(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS).T, axis=0)
    zcr      = np.mean(librosa.feature.zero_crossing_rate(y).T, axis=0)
    rolloff  = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr).T, axis=0)
    rms      = np.mean(librosa.feature.rms(y=y).T, axis=0)
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr).T, axis=0)
    return np.hstack([mfccs, chroma, mel, zcr, rolloff, rms, centroid])

def plot_waveform(y, sr, emotion):
    fig, ax = plt.subplots(figsize=(10, 2.8))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")
    t = np.linspace(0, len(y)/sr, num=len(y))
    ax.plot(t, y, color="#6366f1", linewidth=0.7, alpha=0.9, label="waveform")
    hop   = 512
    rms   = librosa.feature.rms(y=y, hop_length=hop)[0]
    t_rms = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
    col   = EMO_COLORS.get(emotion, "#f59e0b")
    ax.fill_between(t_rms,  rms, alpha=0.35, color=col)
    ax.fill_between(t_rms, -rms, alpha=0.35, color=col)
    ax.plot(t_rms,  rms, color=col, linewidth=1.8, label="RMS energy")
    ax.plot(t_rms, -rms, color=col, linewidth=1.8)
    ax.set_xlim(0, len(y)/sr)
    ax.set_xlabel("time (s)", color="#94a3b8", fontsize=11)
    ax.set_ylabel("amplitude", color="#94a3b8", fontsize=11)
    ax.set_title(f"Waveform  ·  predicted: {emotion.upper()}",
                 color="white", fontsize=13, pad=10, fontweight="normal")
    ax.tick_params(colors="#64748b", labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for sp in ["left", "bottom"]: ax.spines[sp].set_edgecolor("#1e293b")
    ax.legend(facecolor="#1e293b", labelcolor="#cbd5e1",
              fontsize=9, framealpha=0.8, loc="upper right")
    fig.tight_layout(pad=0.8)
    return fig

def plot_mel(y, sr):
    fig, ax = plt.subplots(figsize=(10, 2.8))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")
    S    = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS, fmax=8000)
    S_db = librosa.power_to_db(S, ref=np.max)
    img  = librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="mel",
                                    ax=ax, cmap="magma", fmax=8000)
    cb = fig.colorbar(img, ax=ax, format="%+2.0f dB", pad=0.01)
    cb.ax.tick_params(colors="#94a3b8", labelsize=8)
    cb.outline.set_edgecolor("#1e293b")
    ax.set_title("Mel spectrogram", color="white", fontsize=13,
                 pad=10, fontweight="normal")
    ax.set_xlabel("time (s)", color="#94a3b8", fontsize=11)
    ax.set_ylabel("Hz", color="#94a3b8", fontsize=11)
    ax.tick_params(colors="#64748b", labelsize=9)
    for sp in ax.spines.values(): sp.set_edgecolor("#1e293b")
    fig.tight_layout(pad=0.8)
    return fig

def plot_confidence(probs, classes):
    fig, ax = plt.subplots(figsize=(10, 2.8))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")
    sorted_pairs = sorted(zip(probs, classes), reverse=True)
    s_probs, s_classes = zip(*sorted_pairs)
    bar_colors = [EMO_COLORS.get(c, "#6366f1") for c in s_classes]
    bars = ax.barh(s_classes, [p*100 for p in s_probs],
                   color=bar_colors, height=0.45, edgecolor="none")
    for bar, prob in zip(bars, s_probs):
        ax.text(bar.get_width() + 0.8,
                bar.get_y() + bar.get_height()/2,
                f"{prob*100:.1f}%",
                va="center", ha="left",
                color="white", fontsize=11, fontweight="normal")
    ax.set_xlim(0, 115)
    ax.set_xlabel("confidence (%)", color="#94a3b8", fontsize=11)
    ax.set_title("Emotion confidence scores", color="white",
                 fontsize=13, pad=10, fontweight="normal")
    ax.tick_params(colors="#64748b", labelsize=10)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for sp in ["left", "bottom"]: ax.spines[sp].set_edgecolor("#1e293b")
    fig.tight_layout(pad=0.8)
    return fig

def predict_emotion(audio_path):
    if audio_path is None:
        return None, None, None, "No audio uploaded.", ""

    try:
        y, sr = librosa.load(audio_path, sr=TARGET_SR, mono=True)
    except Exception as e:
        return None, None, None, f"Could not load audio: {e}", ""

    if len(y) < TARGET_SR * 0.5:
        return None, None, None, "Audio too short — speak for at least 1 second.", ""

    feat     = get_features(y, sr)
    feat     = scaler.transform(feat.reshape(1, -1))
    feat     = feat.reshape(1, feat.shape[1], 1)
    probs    = model.predict(feat, verbose=0)[0]
    pred_idx = np.argmax(probs)
    emotion  = enc.classes_[pred_idx]
    conf     = probs[pred_idx]
    emoji    = EMO_EMOJI.get(emotion, "")

    wave_fig = plot_waveform(y, sr, emotion)
    mel_fig  = plot_mel(y, sr)
    conf_fig = plot_confidence(probs, enc.classes_)

    summary = (
        f"Emotion  :  {emotion.upper()}\n\n"
        f"Confidence   :  {conf*100:.1f}%\n"
        f"Duration     :  {len(y)/sr:.2f} s\n"
        f"Sample rate  :  {sr} Hz\n"
        f"Model        :  CNN-LSTM (89.7% acc)"
    )
    breakdown = "\n".join([
        f"  {c:<10}  {'█' * int(p*20):<20}  {p*100:.1f}%"
        for c, p in sorted(zip(enc.classes_, probs), key=lambda x: -x[1])
    ])
    return wave_fig, mel_fig, conf_fig, summary, breakdown

CSS = """
#title    { text-align:center; padding:18px 0 2px; }
#subtitle { text-align:center; color:#94a3b8; font-size:0.88rem; margin-bottom:6px; }
#team     { text-align:center; font-size:0.85rem; color:#a5b4fc; margin-bottom:4px; }
#inst     { text-align:center; font-size:0.8rem;  color:#64748b; margin-bottom:16px; }
.footer-block { text-align:center; color:#475569; font-size:0.76rem;
                line-height:2; margin-top:12px; padding:8px 0; }
footer { visibility:hidden; }
"""

with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="indigo",
        secondary_hue="amber",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter")
    ),
    css=CSS,
    title="Emotion Recognition Using Speech — NIT Kurukshetra"
) as demo:

    gr.Markdown("# ��️ Emotion Recognition Using Speech", elem_id="title")
    gr.Markdown(
        "Real-time detection of human emotions from speech using CNN-LSTM deep learning",
        elem_id="subtitle"
    )
    gr.Markdown(
        "**Sagar S. Maddi** (12215121 · ECE B6) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "**Charan Kasagani** (12215095 · ECE B5)",
        elem_id="team"
    )
    gr.Markdown(
        "Mentor: **Dr. Vrinda Gupta** &nbsp;·&nbsp; "
        "Dept. of Electronics & Communication Engineering &nbsp;·&nbsp; "
        "**NIT Kurukshetra** &nbsp;·&nbsp; 8th Semester FYP 2025–2026",
        elem_id="inst"
    )

    with gr.Row():
        with gr.Column(scale=1):
            audio_in = gr.Audio(
                sources=["upload", "microphone"],
                type="filepath",
                label="Upload or record audio (.wav recommended)"
            )
            detect_btn = gr.Button(
                "Detect Emotion",
                variant="primary",
                size="lg"
            )
            with gr.Accordion("Model & dataset info", open=False):
                gr.Markdown("""
**Architecture** — CNN-LSTM hybrid: 2× Conv1D → BatchNorm → MaxPool → LSTM → Dense

**Features (184-dim)** — MFCC (40) · Chroma (12) · Mel spectrogram (128) · ZCR · Spectral rolloff · RMS energy · Spectral centroid

**Training data** — RAVDESS · TESS · EMO-DB · 4× augmentation (stretch · pitch shift · noise)

**Performance** — 89.7% test accuracy · 4-class: angry · happy · neutral · sad
                """)

        with gr.Column(scale=1):
            summary_out   = gr.Textbox(
                label="Prediction result",
                lines=7
            )
            breakdown_out = gr.Textbox(
                label="All emotion scores",
                lines=5
            )

    with gr.Row():
        wave_out = gr.Plot(label="Waveform + RMS energy")
        mel_out  = gr.Plot(label="Mel spectrogram")

    conf_out = gr.Plot(label="Confidence scores")

    detect_btn.click(
        fn=predict_emotion,
        inputs=[audio_in],
        outputs=[wave_out, mel_out, conf_out, summary_out, breakdown_out]
    )
    audio_in.change(
        fn=predict_emotion,
        inputs=[audio_in],
        outputs=[wave_out, mel_out, conf_out, summary_out, breakdown_out]
    )

    gr.Markdown("""
<div class="footer-block">
Emotion Recognition Using Speech &nbsp;·&nbsp; NIT Kurukshetra &nbsp;·&nbsp; 2025–2026<br>
Sagar S. Maddi (12215121) &nbsp;&amp;&nbsp; Charan Kasagani (12215095)<br>
CNN-LSTM · RAVDESS + TESS + EMO-DB · librosa · TensorFlow · Gradio
</div>
""")

if __name__ == "__main__":
    demo.launch(share=False)
