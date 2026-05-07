const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Speech Emotion Recognition Using Deep Learning";
pres.author = "Sagar S. Maddi & Kasagani Charan Kumar";

// ── Palette ──────────────────────────────────────────────────────────────────
const C = {
  navy:    "1B2A4A",   // primary dark
  white:   "FFFFFF",
  offWhite:"F7F8FC",
  accent:  "8B1A1A",   // NIT deep red
  light:   "D6DCE4",
  text:    "1B2A4A",
  muted:   "5A6A7E",
  black:   "111111",
};

// ── Helpers ───────────────────────────────────────────────────────────────────
const IMG_DIR = path.resolve(__dirname, "../Emotion results images");
const IMG = (file) => {
  const localName = file
    .replace("WhatsApp_Image_", "WhatsApp Image ")
    .replace("_at_", " at ")
    .replace(/(\d{2})_(\d{2})_(\d{2})\.jpeg$/, "$1.$2.$3.jpeg");
  return path.join(IMG_DIR, localName);
};

function slideHeader(slide, title, pgNum) {
  // Dark top bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.72,
    fill: { color: C.navy }, line: { color: C.navy }
  });
  // NIT red accent stripe (left)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.18, h: 0.72,
    fill: { color: C.accent }, line: { color: C.accent }
  });
  // Slide title
  slide.addText(title, {
    x: 0.3, y: 0, w: 9.1, h: 0.72,
    fontSize: 20, bold: true, color: C.white,
    fontFace: "Calibri", valign: "middle", align: "left",
    margin: [0, 0, 0, 12]
  });
  // Page number
  slide.addText(`${pgNum} / 10`, {
    x: 8.5, y: 0, w: 1.3, h: 0.72,
    fontSize: 10, color: "AABBCC", fontFace: "Calibri",
    valign: "middle", align: "right", margin: 0
  });
  // Footer
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.35, w: 10, h: 0.275,
    fill: { color: C.light }, line: { color: C.light }
  });
  slide.addText("NIT Kurukshetra  |  ECE Dept.  |  B.Tech 8th Sem FYP 2025–26  |  Dr. Vrinda Gupta", {
    x: 0.3, y: 5.35, w: 9.4, h: 0.275,
    fontSize: 8.5, color: C.muted, fontFace: "Calibri",
    valign: "middle", align: "left"
  });
  slide.background = { color: C.offWhite };
}

function bullet(text, sub) {
  const items = [{ text, options: { bold: false, breakLine: !sub } }];
  if (sub) items.push({ text: sub, options: { italic: true, breakLine: true, color: C.muted } });
  return items.flat();
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 1 — Title
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  // left accent
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.22, h: 5.625, fill: { color: C.accent }, line: { color: C.accent } });

  s.addText("B.Tech 8th Semester Final Year Project", {
    x: 0.45, y: 0.65, w: 9.3, h: 0.45,
    fontSize: 13, color: "AABBCC", fontFace: "Calibri", bold: false
  });

  s.addText("Speech Emotion Recognition\nUsing Deep Learning", {
    x: 0.45, y: 1.2, w: 9.1, h: 1.7,
    fontSize: 34, bold: true, color: C.white, fontFace: "Calibri",
    align: "left"
  });

  // Divider
  s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 3.05, w: 5.5, h: 0.04, fill: { color: C.accent }, line: { color: C.accent } });

  s.addText([
    { text: "Sagar S. Maddi", options: { bold: true } },
    { text: "  (12215121 – ECE B6)" }
  ], { x: 0.45, y: 3.2, w: 9, h: 0.35, fontSize: 13, color: C.white, fontFace: "Calibri" });

  s.addText([
    { text: "Kasagani Charan Kumar", options: { bold: true } },
    { text: "  (12215095 – ECE B5)" }
  ], { x: 0.45, y: 3.58, w: 9, h: 0.35, fontSize: 13, color: C.white, fontFace: "Calibri" });

  s.addText("Mentor: Dr. Vrinda Gupta  |  Dept. of Electronics & Communication Engineering", {
    x: 0.45, y: 4.05, w: 9, h: 0.35, fontSize: 11.5, color: "AABBCC", fontFace: "Calibri"
  });

  s.addText("National Institute of Technology, Kurukshetra  —  May 2026", {
    x: 0.45, y: 4.45, w: 9, h: 0.35, fontSize: 11, color: "AABBCC", fontFace: "Calibri"
  });

  s.addText("CNN-LSTM  ·  RAVDESS + TESS + EMO-DB  ·  Gradio Web App  ·  89.7% Accuracy", {
    x: 0.45, y: 5.0, w: 9, h: 0.35, fontSize: 10, color: "6A8AAA", fontFace: "Calibri"
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 2 — Project Overview & Motivation
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  slideHeader(s, "Project Overview & Motivation", 1);

  // Two columns
  // Left: motivation
  s.addText("Motivation", {
    x: 0.35, y: 0.85, w: 4.5, h: 0.35,
    fontSize: 14, bold: true, color: C.accent, fontFace: "Calibri"
  });
  const motItems = [
    { text: "Speech carries emotion beyond literal words — pitch, energy, and spectral cues encode affect.", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri", breakLine: true } },
    { text: "Applications: mental health monitoring, call-center analytics, adaptive e-learning, empathetic virtual assistants.", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri", breakLine: true } },
    { text: "Existing open-source SER systems lack augmentation, multi-dataset training, and accessible demos.", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri", breakLine: true } },
    { text: "This project closes those gaps with a complete, reproducible, deployable pipeline.", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri" } },
  ];
  s.addText(motItems, { x: 0.35, y: 1.25, w: 4.4, h: 3.4 });

  // Divider
  s.addShape(pres.shapes.RECTANGLE, { x: 4.95, y: 0.85, w: 0.04, h: 3.8, fill: { color: C.light }, line: { color: C.light } });

  // Right: what was built
  s.addText("What We Built", {
    x: 5.15, y: 0.85, w: 4.5, h: 0.35,
    fontSize: 14, bold: true, color: C.accent, fontFace: "Calibri"
  });
  const whatItems = [
    { text: "184-dim feature vector: MFCC, Chroma, Mel Spectrogram, ZCR, RMS, Spectral Centroid, Rolloff", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri", breakLine: true } },
    { text: "4× data augmentation: ~5,131 → 20,524 samples (time-stretch, pitch-shift, noise)", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri", breakLine: true } },
    { text: "3 architectures trained & compared: LSTM, CNN-LSTM, Transformer Encoder", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri", breakLine: true } },
    { text: "Best model: CNN-LSTM — 89.7% test accuracy (vs 70.3% baseline)", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri", breakLine: true } },
    { text: "Gradio web app — real-time demo with waveform, Mel spectrogram, confidence charts", options: { bullet: true, fontSize: 12, color: C.text, fontFace: "Calibri" } },
  ];
  s.addText(whatItems, { x: 5.15, y: 1.25, w: 4.55, h: 3.4 });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 3 — Datasets & Feature Extraction
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  slideHeader(s, "Datasets & Feature Extraction", 2);

  // Datasets table
  s.addText("Datasets Used — Combined Multi-Speaker Corpus", {
    x: 0.35, y: 0.85, w: 9.3, h: 0.32,
    fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri"
  });

  const tblData = [
    [
      { text: "Dataset",  options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
      { text: "Speakers", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
      { text: "Language", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
      { text: "Clips (used)", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
    ],
    ["RAVDESS", "24 (12M+12F)", "English", "~4,390"],
    ["TESS",    "2 (Female)",   "English", "~741"],
    ["EMO-DB",  "10 (5M+5F)",   "German",  "~454"],
    [{ text: "TOTAL", options: { bold: true } }, "36 speakers", "Multi", { text: "~5,131  →  20,524 (4×aug)", options: { bold: true, color: C.accent } }],
  ];

  s.addTable(tblData, {
    x: 0.35, y: 1.22, w: 9.3, h: 1.35,
    fontFace: "Calibri", fontSize: 11,
    border: { pt: 0.5, color: C.light },
    fill: { color: C.white },
    colW: [2.2, 2.1, 1.8, 3.2],
  });

  // Feature extraction
  s.addText("Feature Extraction Pipeline — 184-Dimensional Vector", {
    x: 0.35, y: 2.72, w: 9.3, h: 0.32,
    fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri"
  });

  const features = [
    ["MFCC (40-dim)",             "Vocal tract shape — primary emotion cue",         "Baseline"],
    ["Chroma STFT (12-dim)",      "Harmonic / pitch class energy",                    "Baseline"],
    ["Mel Spectrogram (128-dim)", "Freq–time energy map — richest single feature",    "Baseline"],
    ["ZCR, RMS, Centroid, Rolloff (4-dim)", "Loudness, brightness, voicing (NEW)",   "NEW ✓"],
  ];

  const fData = [
    [
      { text: "Feature", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
      { text: "What it captures", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
      { text: "Status", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
    ],
    ...features.map(r => [r[0], r[1], { text: r[2], options: r[2].includes("NEW") ? { bold: true, color: C.accent } : {} }])
  ];

  s.addTable(fData, {
    x: 0.35, y: 3.08, w: 9.3, h: 1.65,
    fontFace: "Calibri", fontSize: 11,
    border: { pt: 0.5, color: C.light },
    fill: { color: C.white },
    colW: [2.8, 5.2, 1.3],
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 4 — Data Augmentation & Model Architectures
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  slideHeader(s, "Data Augmentation & Model Architectures", 3);

  // Aug section
  s.addText("Data Augmentation (4× Pipeline)", {
    x: 0.35, y: 0.85, w: 4.5, h: 0.32,
    fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri"
  });

  const augItems = [
    { text: "Time Stretching ×1.1  — simulates fast speech delivery", options: { bullet: true, fontSize: 11.5, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "Pitch Shifting +2 semitones  — cross-gender voice variation", options: { bullet: true, fontSize: 11.5, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "Gaussian Noise  (σ=0.005, ~20 dB SNR) — real-world mic conditions", options: { bullet: true, fontSize: 11.5, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "Result: 5,131 → 20,524 samples — same label, 4× variety", options: { bullet: true, fontSize: 11.5, fontFace: "Calibri", color: C.text, bold: true } },
  ];
  s.addText(augItems, { x: 0.35, y: 1.22, w: 4.45, h: 2.05 });

  // Model table
  s.addText("Model Comparison", {
    x: 0.35, y: 3.42, w: 4.5, h: 0.32,
    fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri"
  });

  const mData = [
    [
      { text: "Model", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
      { text: "Params", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
      { text: "Accuracy", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 11 } },
    ],
    ["LSTM Baseline",           "~120K", "70.3%"],
    [{ text: "CNN-LSTM Hybrid ★", options: { bold: true } }, { text: "~80K", options: { bold: true } }, { text: "89.7%", options: { bold: true, color: C.accent } }],
    ["Transformer Encoder",     "~171K", "Early stopped"],
  ];
  s.addTable(mData, {
    x: 0.35, y: 3.78, w: 4.45, h: 1.25,
    fontFace: "Calibri", fontSize: 11,
    border: { pt: 0.5, color: C.light },
    fill: { color: C.white },
    colW: [2.0, 1.0, 1.45],
  });

  // Right: CNN-LSTM arch diagram (text-based)
  s.addShape(pres.shapes.RECTANGLE, { x: 4.95, y: 0.85, w: 0.04, h: 4.15, fill: { color: C.light }, line: { color: C.light } });

  s.addText("CNN-LSTM Architecture", {
    x: 5.15, y: 0.85, w: 4.55, h: 0.32,
    fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri"
  });

  const layers = [
    "Input (184 × 1)",
    "Conv1D (64 filters, k=5) + BatchNorm + MaxPool",
    "Conv1D (128 filters, k=3) + BatchNorm + MaxPool",
    "LSTM (64 units) + Dropout 0.4",
    "Dense (64, ReLU) + Dropout 0.3",
    "Dense (4, Softmax) → Emotion class",
  ];

  let ly = 1.28;
  layers.forEach((txt, i) => {
    const isTop = i === 0;
    const isBot = i === layers.length - 1;
    const bg = isBot ? C.accent : (isTop ? C.navy : "E8EEF5");
    const fg = (isTop || isBot) ? C.white : C.text;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.3, y: ly, w: 4.2, h: 0.48, fill: { color: bg }, line: { color: C.light } });
    s.addText(txt, { x: 5.3, y: ly, w: 4.2, h: 0.48, fontSize: 11, color: fg, fontFace: "Calibri", align: "center", valign: "middle" });
    if (i < layers.length - 1) {
      s.addText("▼", { x: 5.3, y: ly + 0.48, w: 4.2, h: 0.22, fontSize: 11, color: C.muted, fontFace: "Calibri", align: "center", valign: "middle" });
    }
    ly += i < layers.length - 1 ? 0.7 : 0;
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 5 — Results & Per-Class Performance
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  slideHeader(s, "Results & Per-Class Performance", 4);

  // Big accuracy callout
  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 0.88, w: 3.0, h: 1.6, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("89.7%", { x: 0.35, y: 0.88, w: 3.0, h: 1.0, fontSize: 40, bold: true, color: C.white, fontFace: "Calibri", align: "center", valign: "bottom" });
  s.addText("CNN-LSTM Test Accuracy", { x: 0.35, y: 1.75, w: 3.0, h: 0.55, fontSize: 11, color: "AABBCC", fontFace: "Calibri", align: "center", valign: "top" });

  s.addShape(pres.shapes.RECTANGLE, { x: 3.55, y: 0.88, w: 2.95, h: 1.6, fill: { color: C.accent }, line: { color: C.accent } });
  s.addText("+19.4 pp", { x: 3.55, y: 0.88, w: 2.95, h: 1.0, fontSize: 38, bold: true, color: C.white, fontFace: "Calibri", align: "center", valign: "bottom" });
  s.addText("Gain over LSTM baseline (70.3%)", { x: 3.55, y: 1.75, w: 2.95, h: 0.55, fontSize: 11, color: C.white, fontFace: "Calibri", align: "center" });

  s.addShape(pres.shapes.RECTANGLE, { x: 6.7, y: 0.88, w: 2.95, h: 1.6, fill: { color: "2C4A7A" }, line: { color: "2C4A7A" } });
  s.addText("0.87–0.91", { x: 6.7, y: 0.88, w: 2.95, h: 1.0, fontSize: 36, bold: true, color: C.white, fontFace: "Calibri", align: "center", valign: "bottom" });
  s.addText("Per-class F1 Range", { x: 6.7, y: 1.75, w: 2.95, h: 0.55, fontSize: 11, color: "AABBCC", fontFace: "Calibri", align: "center" });

  // Per-class table
  s.addText("Per-Class Performance — CNN-LSTM Model", {
    x: 0.35, y: 2.65, w: 9.3, h: 0.32,
    fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri"
  });

  const perf = [
    [
      { text: "Emotion", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 12 } },
      { text: "Precision", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 12 } },
      { text: "Recall",    options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 12 } },
      { text: "F1-Score",  options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 12 } },
      { text: "Samples",   options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 12 } },
    ],
    ["Angry",   "0.93", "0.89", { text: "0.91", options: { bold: true } }, "766"],
    ["Happy",   "0.93", "0.83", { text: "0.88", options: {} }, "763"],
    ["Neutral", "0.89", "0.93", { text: "0.91", options: { bold: true } }, "1,808"],
    ["Sad",     "0.85", "0.89", { text: "0.87", options: {} }, "768"],
    [
      { text: "Weighted Avg", options: { bold: true } },
      { text: "0.90", options: { bold: true, color: C.accent } },
      { text: "0.90", options: { bold: true, color: C.accent } },
      { text: "0.90", options: { bold: true, color: C.accent } },
      "4,105"
    ],
  ];

  s.addTable(perf, {
    x: 0.35, y: 3.0, w: 9.3, h: 2.05,
    fontFace: "Calibri", fontSize: 12,
    border: { pt: 0.5, color: C.light },
    fill: { color: C.white },
    colW: [2.0, 1.8, 1.7, 1.8, 2.0],
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 6 — System Architecture & Workflow
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  slideHeader(s, "System Architecture & Workflow", 5);

  const steps = [
    { label: "Raw Audio Input", sub: "WAV / Mic" },
    { label: "Preprocessing", sub: "Resample → 16 kHz" },
    { label: "Data Augmentation", sub: "4× expansion" },
    { label: "Feature Extraction", sub: "184-dim vector" },
    { label: "CNN-LSTM Model", sub: "89.7% accuracy" },
    { label: "Emotion Output", sub: "Happy / Angry\nNeutral / Sad" },
  ];

  const boxW = 1.35, boxH = 0.95, gap = 0.1;
  const totalW = steps.length * boxW + (steps.length - 1) * gap;
  const startX = (10 - totalW) / 2;
  const rowY = 1.1;

  steps.forEach((st, i) => {
    const x = startX + i * (boxW + gap);
    const isLast = i === steps.length - 1;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: rowY, w: boxW, h: boxH,
      fill: { color: isLast ? C.accent : C.navy },
      line: { color: isLast ? C.accent : C.navy }
    });
    s.addText(st.label, {
      x, y: rowY, w: boxW, h: boxH * 0.58,
      fontSize: 10.5, bold: true, color: C.white, fontFace: "Calibri", align: "center", valign: "bottom"
    });
    s.addText(st.sub, {
      x, y: rowY + boxH * 0.55, w: boxW, h: boxH * 0.42,
      fontSize: 9, color: "AABBCC", fontFace: "Calibri", align: "center", valign: "top"
    });
    if (!isLast) {
      s.addText("→", {
        x: x + boxW, y: rowY, w: gap, h: boxH,
        fontSize: 16, color: C.muted, fontFace: "Calibri", align: "center", valign: "middle"
      });
    }
  });

  // Gradio sub-flow below
  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 2.3, w: 9.3, h: 0.03, fill: { color: C.light }, line: { color: C.light } });

  s.addText("Gradio Web Application — Real-Time Inference Flow", {
    x: 0.35, y: 2.45, w: 9.3, h: 0.32,
    fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri"
  });

  const appSteps = [
    { label: "1. Upload / Record", sub: "WAV audio file or live mic" },
    { label: "2. Feature Extract", sub: "184-dim vector in real time" },
    { label: "3. CNN-LSTM Inference", sub: "Softmax probability output" },
    { label: "4. Waveform + Mel Plot", sub: "RMS energy overlay" },
    { label: "5. Confidence Chart", sub: "All 4 emotion scores" },
  ];

  const bW = 1.72, bH = 0.88;
  const aStartX = 0.35;
  appSteps.forEach((st, i) => {
    const x = aStartX + i * (bW + 0.04);
    s.addShape(pres.shapes.RECTANGLE, { x, y: 2.88, w: bW, h: bH, fill: { color: "E8EEF5" }, line: { color: C.light } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 2.88, w: bW, h: 0.06, fill: { color: C.navy }, line: { color: C.navy } });
    s.addText(st.label, { x, y: 2.94, w: bW, h: 0.42, fontSize: 11, bold: true, color: C.navy, fontFace: "Calibri", align: "center", valign: "middle" });
    s.addText(st.sub, { x, y: 3.36, w: bW, h: 0.38, fontSize: 10, color: C.muted, fontFace: "Calibri", align: "center", valign: "top" });
  });

  // Software stack
  s.addText("Tech Stack: Python 3.11  ·  TensorFlow 2.16 / Keras  ·  librosa 0.11  ·  NumPy  ·  scikit-learn  ·  Gradio 6.14  ·  Matplotlib", {
    x: 0.35, y: 3.95, w: 9.3, h: 0.3,
    fontSize: 10.5, color: C.muted, fontFace: "Calibri", align: "center"
  });

  // Training config
  const cfgItems = [
    { text: "Training config: 100 epochs max  |  Early stopping (patience=10)  |  Batch=32  |  Adam lr=1e-3  |  ReduceLROnPlateau  |  80/20 stratified split", options: { fontSize: 11, color: C.text, fontFace: "Calibri" } },
  ];
  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 4.35, w: 9.3, h: 0.7, fill: { color: "E8EEF5" }, line: { color: C.light } });
  s.addText(cfgItems, { x: 0.45, y: 4.35, w: 9.1, h: 0.7, valign: "middle" });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 7 — Live Application Screenshots (4 images in 2×2 grid)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  slideHeader(s, "Gradio Web App — Prediction Interface Screenshots", 6);

  s.addText("Each screenshot shows: Detected Emotion  ·  Confidence Score  ·  Audio Metadata  ·  All Emotion Scores", {
    x: 0.35, y: 0.82, w: 9.3, h: 0.28,
    fontSize: 10.5, color: C.muted, fontFace: "Calibri", align: "center"
  });

  // 2×2 grid of interface screenshots (images 0,2,4,6)
  const imgs = [
    { path: IMG("WhatsApp_Image_2026-05-07_at_10_54_41.jpeg"), cap: "Fig 10.1 — HAPPY  (99.9%)" },
    { path: IMG("WhatsApp_Image_2026-05-07_at_10_56_18.jpeg"), cap: "Fig 10.3 — ANGRY  (100.0%)" },
    { path: IMG("WhatsApp_Image_2026-05-07_at_10_59_52.jpeg"), cap: "Fig 10.5 — SAD  (89.8%)" },
    { path: IMG("WhatsApp_Image_2026-05-07_at_11_01_57.jpeg"), cap: "Fig 10.7 — NEUTRAL  (76.4%)" },
  ];

  const iW = 4.55, iH = 2.08;
  const positions = [
    { x: 0.2,  y: 1.18 },
    { x: 5.05, y: 1.18 },
    { x: 0.2,  y: 3.35 },
    { x: 5.05, y: 3.35 },
  ];

  imgs.forEach((img, i) => {
    const { x, y } = positions[i];
    s.addShape(pres.shapes.RECTANGLE, { x: x-0.04, y: y-0.04, w: iW+0.08, h: iH+0.3, fill: { color: C.white }, line: { color: C.light } });
    s.addImage({ path: img.path, x, y, w: iW, h: iH, sizing: { type: "contain", w: iW, h: iH } });
    s.addText(img.cap, {
      x, y: y + iH + 0.02, w: iW, h: 0.24,
      fontSize: 9, color: C.muted, fontFace: "Calibri", italic: true, align: "center"
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 8 — Waveform & Spectrogram Visualizations (4 images 2×2)
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  slideHeader(s, "Gradio Web App — Waveform + Mel Spectrogram & Confidence Charts", 7);

  s.addText("Top row: Waveform + RMS Energy overlay + Mel Spectrogram  ·  Bottom row: Emotion Confidence Bar Charts", {
    x: 0.35, y: 0.82, w: 9.3, h: 0.28,
    fontSize: 10.5, color: C.muted, fontFace: "Calibri", align: "center"
  });

  const imgs = [
    { path: IMG("WhatsApp_Image_2026-05-07_at_10_55_06.jpeg"), cap: "Fig 10.2 — HAPPY Waveform + Mel" },
    { path: IMG("WhatsApp_Image_2026-05-07_at_10_57_33.jpeg"), cap: "Fig 10.4 — ANGRY Waveform + Mel" },
    { path: IMG("WhatsApp_Image_2026-05-07_at_11_00_11.jpeg"), cap: "Fig 10.6 — SAD Confidence Scores" },
    { path: IMG("WhatsApp_Image_2026-05-07_at_11_02_28.jpeg"), cap: "Fig 10.8 — NEUTRAL Confidence Scores" },
  ];

  const iW = 4.55, iH = 2.08;
  const positions = [
    { x: 0.2,  y: 1.18 },
    { x: 5.05, y: 1.18 },
    { x: 0.2,  y: 3.35 },
    { x: 5.05, y: 3.35 },
  ];

  imgs.forEach((img, i) => {
    const { x, y } = positions[i];
    s.addShape(pres.shapes.RECTANGLE, { x: x-0.04, y: y-0.04, w: iW+0.08, h: iH+0.3, fill: { color: C.white }, line: { color: C.light } });
    s.addImage({ path: img.path, x, y, w: iW, h: iH, sizing: { type: "contain", w: iW, h: iH } });
    s.addText(img.cap, {
      x, y: y + iH + 0.02, w: iW, h: 0.24,
      fontSize: 9, color: C.muted, fontFace: "Calibri", italic: true, align: "center"
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 9 — Comparison, Advantages & Limitations
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  slideHeader(s, "Comparison with Prior Work  |  Advantages & Limitations", 8);

  // Comparison table
  s.addText("Comparison with Prior Work", {
    x: 0.35, y: 0.85, w: 9.3, h: 0.3, fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri"
  });

  const cmp = [
    [
      { text: "Method / Author", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 10.5 } },
      { text: "Dataset", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 10.5 } },
      { text: "Accuracy", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 10.5 } },
      { text: "Aug.", options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 10.5 } },
    ],
    ["SVM + MFCC (2011)", "EMO-DB", "77.4%", "No"],
    ["DNN + MFCC (2017)", "IEMOCAP", "64.7%", "No"],
    ["CNN-LSTM (2019)",   "RAVDESS", "70.1%", "No"],
    ["x4nth055 LSTM (2019)", "RAVDESS+TESS", "77.2%", "No"],
    [
      { text: "This Work — CNN-LSTM ★", options: { bold: true } },
      { text: "RAVDESS+TESS+EMO-DB", options: {} },
      { text: "89.7%", options: { bold: true, color: C.accent } },
      { text: "4×", options: { bold: true, color: C.accent } },
    ],
  ];

  s.addTable(cmp, {
    x: 0.35, y: 1.18, w: 9.3, h: 1.6,
    fontFace: "Calibri", fontSize: 11,
    border: { pt: 0.5, color: C.light },
    fill: { color: C.white },
    colW: [3.0, 2.5, 1.6, 2.2],
  });

  // Advantages & Limitations columns
  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 2.9, w: 0.04, h: 2.15, fill: { color: C.accent }, line: { color: C.accent } });
  s.addText("Advantages", { x: 0.5, y: 2.88, w: 4.35, h: 0.3, fontSize: 13, bold: true, color: C.accent, fontFace: "Calibri" });

  const advItems = [
    { text: "Multi-dataset: speaker diversity across RAVDESS, TESS, EMO-DB", options: { bullet: true, fontSize: 11, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "4× augmentation cuts overfitting without extra data collection", options: { bullet: true, fontSize: 11, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "CNN-LSTM +19.4 pp over LSTM baseline; all F1 ≥ 0.87", options: { bullet: true, fontSize: 11, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "Runs on standard consumer laptop — no specialized hardware", options: { bullet: true, fontSize: 11, fontFace: "Calibri", color: C.text } },
  ];
  s.addText(advItems, { x: 0.5, y: 3.2, w: 4.25, h: 1.82 });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.05, y: 2.9, w: 0.04, h: 2.15, fill: { color: "2C4A7A" }, line: { color: "2C4A7A" } });
  s.addText("Limitations & Future Scope", { x: 5.2, y: 2.88, w: 4.55, h: 0.3, fontSize: 13, bold: true, color: "2C4A7A", fontFace: "Calibri" });

  const limItems = [
    { text: "Only 4 emotion classes; expand to 7-8 (Fear, Disgust, Surprise)", options: { bullet: true, fontSize: 11, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "Transformer Encoder training was stopped early due to hardware limits", options: { bullet: true, fontSize: 11, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "File-level only; no streaming/frame-level real-time inference yet", options: { bullet: true, fontSize: 11, fontFace: "Calibri", color: C.text, breakLine: true } },
    { text: "Future: Wav2Vec2 embeddings, Hugging Face cloud deployment, edge TFLite", options: { bullet: true, fontSize: 11, fontFace: "Calibri", color: C.text } },
  ];
  s.addText(limItems, { x: 5.2, y: 3.2, w: 4.45, h: 1.82 });
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDE 10 — Conclusion & Links
// ═══════════════════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.22, h: 5.625, fill: { color: C.accent }, line: { color: C.accent } });

  s.addText("Conclusion", {
    x: 0.45, y: 0.4, w: 9.2, h: 0.55,
    fontSize: 24, bold: true, color: C.white, fontFace: "Calibri"
  });

  const concl = [
    { text: "End-to-end SER pipeline: raw audio → 184-dim features → CNN-LSTM → real-time Gradio demo", options: { bullet: true, fontSize: 13, fontFace: "Calibri", color: "CADCFC", breakLine: true } },
    { text: "CNN-LSTM achieves 89.7% accuracy — 19.4 pp above LSTM baseline; macro F1 = 0.89", options: { bullet: true, fontSize: 13, fontFace: "Calibri", color: "CADCFC", breakLine: true } },
    { text: "Multi-dataset training (36 speakers) + 4× augmentation → robust, generalizable model", options: { bullet: true, fontSize: 13, fontFace: "Calibri", color: "CADCFC", breakLine: true } },
    { text: "No specialized hardware required — runs fully on consumer MacBook with Metal GPU", options: { bullet: true, fontSize: 13, fontFace: "Calibri", color: "CADCFC", breakLine: true } },
    { text: "Interactive Gradio app provides accessible, real-time emotion detection from any browser", options: { bullet: true, fontSize: 13, fontFace: "Calibri", color: "CADCFC" } },
  ];
  s.addText(concl, { x: 0.45, y: 1.05, w: 9.2, h: 2.1 });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 3.25, w: 9.1, h: 0.04, fill: { color: C.accent }, line: { color: C.accent } });

  // Links
  s.addText([
    { text: "🔗  Live Demo: ", options: { bold: true } },
    { text: "https://095706ea257921b090.gradio.live/" }
  ], { x: 0.45, y: 3.38, w: 9.1, h: 0.38, fontSize: 12.5, color: C.white, fontFace: "Calibri" });

  s.addText([
    { text: "📁  GitHub: ", options: { bold: true } },
    { text: "https://github.com/sagar141202/8th_sem_project" }
  ], { x: 0.45, y: 3.8, w: 9.1, h: 0.38, fontSize: 12.5, color: C.white, fontFace: "Calibri" });

  s.addText("Mentor: Dr. Vrinda Gupta  |  Dept. of ECE, NIT Kurukshetra", {
    x: 0.45, y: 4.28, w: 9.1, h: 0.3, fontSize: 11, color: "6A8AAA", fontFace: "Calibri"
  });

  s.addText("Thank You", {
    x: 0.45, y: 4.68, w: 9.1, h: 0.6,
    fontSize: 28, bold: true, color: C.accent, fontFace: "Calibri"
  });
}

// Write
pres.writeFile({ fileName: path.resolve(__dirname, "SER_FYP_Presentation.pptx") })
  .then(() => console.log("✅ PPTX written"))
  .catch(e => console.error("❌", e));
