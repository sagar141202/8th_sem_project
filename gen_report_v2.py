from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, Image, KeepTogether
)
import os

W, H = A4
DARK_MAROON = colors.HexColor('#6B0000')
BLACK = colors.black
GRAY = colors.HexColor('#555555')
TH_NAVY  = colors.HexColor('#1a3a5c')
TH_GREEN = colors.HexColor('#0d5c3a')
TH_ALT_GREEN = colors.HexColor('#e6f4ee')
TH_ALT_BLUE  = colors.HexColor('#e8f0f7')
WHITE = colors.white

# ── STYLES ─────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

COVER_TITLE = S('ct', fontName='Times-Roman', fontSize=14, alignment=TA_CENTER, leading=20)
COVER_BOLD  = S('cb', fontName='Times-Bold',  fontSize=16, alignment=TA_CENTER, leading=24)
COVER_NORM  = S('cn', fontName='Times-Roman', fontSize=13, alignment=TA_CENTER, leading=18)
COVER_DEPT  = S('cd', fontName='Times-Bold',  fontSize=13, alignment=TA_CENTER, leading=18)
COVER_SMALL = S('cs', fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=16)

CERT   = S('cert',  fontName='Times-Roman', fontSize=12, alignment=TA_JUSTIFY, leading=20)
CERT_B = S('certb', fontName='Times-Bold',  fontSize=12, alignment=TA_LEFT,    leading=20)

CH   = S('ch',  fontName='Times-Bold',   fontSize=16, alignment=TA_CENTER, leading=24, spaceAfter=12, spaceBefore=6)
SEC  = S('sec', fontName='Times-Bold',   fontSize=13, alignment=TA_LEFT,   leading=20, spaceAfter=6,  spaceBefore=10)
BODY = S('body',fontName='Times-Roman',  fontSize=12, alignment=TA_JUSTIFY,leading=20, spaceAfter=6)
BODY_I=S('bi',  fontName='Times-Roman',  fontSize=12, alignment=TA_JUSTIFY,leading=20, spaceAfter=4, leftIndent=22)
BULL = S('bull', fontName='Times-Roman', fontSize=12, alignment=TA_JUSTIFY,leading=19, spaceAfter=3, leftIndent=26, bulletIndent=12)
TOC  = S('toc',  fontName='Times-Roman', fontSize=12, alignment=TA_LEFT,   leading=20)
TOCB = S('tocb', fontName='Times-Bold',  fontSize=12, alignment=TA_LEFT,   leading=20)
FIG  = S('fig',  fontName='Times-Italic',fontSize=11, alignment=TA_CENTER, leading=16, spaceAfter=8, spaceBefore=4)
REF  = S('ref',  fontName='Times-Roman', fontSize=11, alignment=TA_JUSTIFY,leading=18, spaceAfter=5, leftIndent=30, firstLineIndent=-30)
CODE = S('code', fontName='Courier',     fontSize=8,  leading=13, backColor=colors.HexColor('#f5f5f5'),
         leftIndent=8, rightIndent=8, spaceBefore=6, spaceAfter=6, borderPadding=6)
# Small cell style for tight tables
CELL = S('cell', fontName='Times-Roman', fontSize=9,  alignment=TA_LEFT, leading=13)
CELLB= S('cellb',fontName='Times-Bold',  fontSize=9,  alignment=TA_LEFT, leading=13)

# Usable page width (A4 minus margins)
PW = W - 4.5*cm  # 2.5cm left + 2cm right

def header_footer(canvas, doc):
    canvas.saveState()
    pn = doc.page
    if pn > 1:
        canvas.setFont('Times-Roman', 9)
        canvas.setFillColor(GRAY)
        canvas.drawString(2.5*cm, 1.2*cm, 'Speech Emotion Recognition Using Deep Learning — NIT Kurukshetra')
        canvas.setStrokeColor(GRAY)
        canvas.setLineWidth(0.3)
        canvas.line(2.5*cm, 1.6*cm, W-2*cm, 1.6*cm)
        canvas.setFont('Times-Roman', 10)
        canvas.setFillColor(BLACK)
        canvas.drawCentredString(W/2, 0.7*cm, str(pn - 1))
    canvas.restoreState()

# ── TABLE BUILDER ──────────────────────────────────────────────────
def tbl(headers, rows, widths, hc=TH_NAVY, ac=TH_ALT_BLUE, font_size=10):
    """Build a table that fits within page width. widths must sum <= PW."""
    # Convert header/cell text to Paragraph for wrapping
    cell_style = ParagraphStyle('cs2', fontName='Times-Roman', fontSize=font_size,
                                 leading=font_size+4, alignment=TA_LEFT)
    head_style = ParagraphStyle('hs2', fontName='Times-Bold', fontSize=font_size,
                                 leading=font_size+4, alignment=TA_LEFT, textColor=WHITE)
    def wrap(val, style):
        if isinstance(val, str):
            return Paragraph(val, style)
        return val

    data = [[wrap(h, head_style) for h in headers]]
    for row in rows:
        data.append([wrap(c, cell_style) for c in row])

    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), hc),
        ('TEXTCOLOR',(0,0),(-1,0), WHITE),
        ('FONTNAME',(0,0),(-1,0),'Times-Bold'),
        ('FONTNAME',(0,1),(-1,-1),'Times-Roman'),
        ('FONTSIZE',(0,0),(-1,-1), font_size),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, ac]),
        ('GRID',(0,0),(-1,-1), 0.5, colors.HexColor('#aaaaaa')),
        ('TOPPADDING',(0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',(0,0),(-1,-1), 6),
        ('RIGHTPADDING',(0,0),(-1,-1), 6),
        ('WORDWRAP',(0,0),(-1,-1), 'LTR'),
    ]))
    return t

def img_block(path, w=None, caption=None):
    if w is None:
        w = PW
    items = []
    if os.path.exists(path):
        try:
            img = Image(path, width=w, height=w*0.53)
            img.hAlign = 'CENTER'
            items.append(img)
        except Exception as e:
            items.append(Paragraph(f'[Figure: {caption}]', BODY))
    if caption:
        items.append(Paragraph(caption, FIG))
    return items

story = []

# ── CERTIFICATE ─────────────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('CERTIFICATE', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    'We hereby certify that the work presented in this B.Tech Project Report titled '
    '<b>"Speech Emotion Recognition Using Deep Learning"</b>, submitted in partial fulfillment '
    'of the requirements for the award of the degree of Bachelor of Technology in Electronics '
    'and Communication Engineering, is an authentic record of our own work carried out during '
    'the period January 2026 to May 2026, under the supervision of <b>Dr. Vrinda Gupta</b>, '
    'Associate Professor, Department of Electronics and Communication Engineering, National '
    'Institute of Technology Kurukshetra.', CERT))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'The matter embodied in this project report has not been submitted, in part or in full, '
    'for the award of any other degree or diploma at this or any other university.', CERT))
story.append(Spacer(1, 1.0*cm))
sig1 = Table([
    [Paragraph('Signature of the Candidates:', CERT_B), ''],
    [Paragraph('Kasagani Charan Kumar (12215095)', CERT), Paragraph('Sagar S. Maddi (12215121)', CERT)],
    [Paragraph('ECE B5, NIT Kurukshetra', CERT), Paragraph('ECE B6, NIT Kurukshetra', CERT)],
], colWidths=[8.5*cm, 8.3*cm])
sig1.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
                           ('RIGHTPADDING',(0,0),(-1,-1),0),('GRID',(0,0),(-1,-1),0,WHITE)]))
story.append(sig1)
story.append(Spacer(1, 1.0*cm))
story.append(HRFlowable(width='100%', thickness=0.4, color=GRAY))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(
    'This is to certify that the above statement made by the candidates is correct to the best of my knowledge.', CERT))
story.append(Spacer(1, 1.0*cm))
story.append(Paragraph('Signature of the Supervisor', CERT_B))
story.append(Spacer(1, 0.6*cm))
story.append(Paragraph('<b>Dr. Vrinda Gupta</b>', CERT))
story.append(Paragraph('Associate Professor', CERT))
story.append(Paragraph('Department of Electronics and Communication Engineering', CERT))
story.append(Paragraph('National Institute of Technology Kurukshetra', CERT))
story.append(PageBreak())

# ── DECLARATION ─────────────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('DECLARATION', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.5*cm))
for para in [
    'We, Kasagani Charan Kumar (12215095) and Sagar S. Maddi (12215121), students of B.Tech '
    '8th Semester, Department of Electronics and Communication Engineering, National Institute '
    'of Technology Kurukshetra, hereby declare that the project report titled '
    '<b>"Speech Emotion Recognition Using Deep Learning"</b> is an original piece of work '
    'carried out by us under the guidance of Dr. Vrinda Gupta, Associate Professor, '
    'Department of Electronics and Communication Engineering, NIT Kurukshetra.',
    'We further declare that this work has not been submitted, either in full or in part, '
    'for the award of any other degree or diploma to this university or any other institution '
    'of learning. All sources of information used in this project have been duly acknowledged.',
    'The implementation, results, analysis, and all findings presented in this report are our '
    'own contributions, conducted ethically and in accordance with the norms of academic research.',
]:
    story.append(Paragraph(para, CERT))
    story.append(Spacer(1, 0.3*cm))
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph('Place: Kurukshetra', CERT))
story.append(Paragraph('Date: May 2026', CERT))
story.append(Spacer(1, 1.0*cm))
sig2 = Table([
    [Paragraph('<b>Kasagani Charan Kumar</b>', CERT), Paragraph('<b>Sagar S. Maddi</b>', CERT)],
    [Paragraph('Roll No: 12215095 | ECE B5', CERT), Paragraph('Roll No: 12215121 | ECE B6', CERT)],
], colWidths=[8.5*cm, 8.3*cm])
sig2.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
                           ('RIGHTPADDING',(0,0),(-1,-1),0),('GRID',(0,0),(-1,-1),0,WHITE)]))
story.append(sig2)
story.append(PageBreak())

# ── ACKNOWLEDGEMENT ─────────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('ACKNOWLEDGEMENT', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.5*cm))
for para in [
    'We would like to express our sincere and heartfelt gratitude to our project supervisor, '
    '<b>Dr. Vrinda Gupta</b>, Associate Professor, Department of Electronics and Communication '
    'Engineering, National Institute of Technology Kurukshetra, for her invaluable guidance, '
    'constant encouragement, and constructive feedback throughout the course of this project.',
    'We extend our sincere thanks to the faculty and staff of the Department of Electronics '
    'and Communication Engineering, NIT Kurukshetra, for providing us with the necessary '
    'resources and a conducive academic environment throughout the entire project duration.',
    'We are grateful to the creators of the publicly available speech emotion datasets — '
    'RAVDESS, TESS, and EMO-DB — which formed the experimental foundation of this project. '
    'We also acknowledge the open-source community behind Python, TensorFlow, Keras, '
    'librosa, Gradio, and scikit-learn, without which this work would not have been possible.',
    'Finally, we thank our families and friends for their unwavering support and encouragement '
    'throughout our academic journey.',
]:
    story.append(Paragraph(para, CERT))
    story.append(Spacer(1, 0.3*cm))
story.append(Spacer(1, 1.0*cm))
story.append(Paragraph('Kasagani Charan Kumar (12215095)', CERT))
story.append(Paragraph('Sagar S. Maddi (12215121)', CERT))
story.append(Paragraph('Department of ECE, NIT Kurukshetra | May 2026', CERT))
story.append(PageBreak())

# ── ABSTRACT ────────────────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('ABSTRACT', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.5*cm))
for para in [
    'Speech Emotion Recognition (SER) is the task of automatically identifying a speaker\'s '
    'emotional state from the acoustic characteristics of their voice. This project presents '
    'a complete, end-to-end SER pipeline trained on three publicly available benchmark datasets '
    '— RAVDESS, TESS, and EMO-DB — covering four emotion classes: Angry, Happy, Neutral, and Sad.',
    'A 184-dimensional feature vector is extracted from each audio clip by combining seven '
    'complementary acoustic feature types: MFCC (40 dimensions), Chroma STFT (12 dimensions), '
    'Mel Spectrogram (128 dimensions), Zero Crossing Rate, Spectral Rolloff, RMS Energy, and '
    'Spectral Centroid. A 4x data augmentation pipeline expands the training corpus from '
    'approximately 5,131 to 20,524 samples.',
    'Three deep learning architectures are designed, trained, and systematically compared: '
    'an LSTM baseline (70.3% test accuracy), a CNN-LSTM hybrid model (89.7% test accuracy), '
    'and a Transformer Encoder. The CNN-LSTM hybrid achieves the best balance of accuracy '
    'and computational efficiency with per-class F1-scores ranging from 0.87 to 0.91.',
    'An interactive real-time web application is developed using Gradio, featuring waveform '
    'visualization with RMS energy overlay, Mel spectrogram display, and confidence score '
    'bar charts for all emotion classes.',
]:
    story.append(Paragraph(para, CERT))
    story.append(Spacer(1, 0.3*cm))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    '<b>Keywords:</b> Speech Emotion Recognition, CNN-LSTM, MFCC, Deep Learning, '
    'RAVDESS, TESS, EMO-DB, Gradio, Mel Spectrogram, Data Augmentation, Affective Computing.', CERT))
story.append(PageBreak())

# ── TABLE OF CONTENTS ───────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('TABLE OF CONTENTS', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
toc_entries = [
    ('Certificate', 'i', False), ('Declaration', 'ii', False),
    ('Acknowledgement', 'iii', False), ('Abstract', 'iv', False),
    ('List of Figures', 'v', False), ('List of Tables', 'vi', False),
    ('Chapter 1 — Introduction', '1', True),
    ('Chapter 2 — Problem Statement and Objectives', '4', True),
    ('Chapter 3 — Literature Survey', '6', True),
    ('Chapter 4 — Datasets Used', '9', True),
    ('Chapter 5 — Feature Extraction', '12', True),
    ('Chapter 6 — Data Augmentation', '15', True),
    ('Chapter 7 — Model Architectures', '17', True),
    ('Chapter 8 — Implementation Details', '22', True),
    ('Chapter 9 — Results and Analysis', '25', True),
    ('Chapter 10 — Gradio Web Application', '30', True),
    ('Chapter 11 — Comparison with Prior Work', '38', True),
    ('Chapter 12 — Advantages and Limitations', '40', True),
    ('Chapter 13 — Future Scope', '42', True),
    ('Chapter 14 — Conclusion', '44', True),
    ('References', '46', True),
    ('Appendix', '48', True),
]
for title, page, bold in toc_entries:
    st = TOCB if bold else TOC
    dots = '.' * max(2, 62 - len(title))
    story.append(Paragraph(f'{title} {dots} {page}', st))
story.append(PageBreak())

# ── LIST OF FIGURES ─────────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('LIST OF FIGURES', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
figs = [
    ('1.1', 'Block diagram of the complete Speech Emotion Recognition pipeline', '3'),
    ('5.1', 'Illustration of MFCC extraction from a speech waveform', '13'),
    ('5.2', 'Mel spectrogram of an angry speech sample from RAVDESS dataset', '14'),
    ('7.1', 'Architecture of the LSTM Baseline model', '18'),
    ('7.2', 'Architecture of the CNN-LSTM Hybrid model', '19'),
    ('7.3', 'Architecture of the Transformer Encoder model', '21'),
    ('9.1', 'Training and validation accuracy curves for the CNN-LSTM model', '26'),
    ('9.2', 'Training and validation loss curves for the CNN-LSTM model', '27'),
    ('10.1', 'Gradio interface — HAPPY speech detected (99.9% confidence)', '31'),
    ('10.2', 'Waveform + Mel spectrogram for HAPPY speech prediction', '32'),
    ('10.3', 'Gradio interface — ANGRY speech detected (100.0% confidence)', '33'),
    ('10.4', 'Waveform + Mel spectrogram for ANGRY speech prediction', '34'),
    ('10.5', 'Gradio interface — SAD speech detected (89.8% confidence)', '35'),
    ('10.6', 'Confidence scores for SAD speech prediction', '36'),
    ('10.7', 'Gradio interface — NEUTRAL speech detected (76.4% confidence)', '37'),
    ('10.8', 'Confidence scores for NEUTRAL speech prediction', '38'),
]
for num, title, page in figs:
    story.append(Paragraph(f'<b>Figure {num}</b>  —  {title} {"." * max(2, 58 - len(title))} {page}', TOC))
story.append(PageBreak())

# ── LIST OF TABLES ──────────────────────────────────────────────────
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('LIST OF TABLES', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
tables_list = [
    ('3.1', 'Summary of related work in Speech Emotion Recognition', '7'),
    ('4.1', 'Datasets used in this project with key statistics', '10'),
    ('5.1', 'Feature extraction pipeline — 7 feature types, 184 total dimensions', '13'),
    ('6.1', 'Data augmentation techniques and their effects on training data', '16'),
    ('7.1', 'Summary of three neural network architectures and parameters', '21'),
    ('8.1', 'Software stack and development environment details', '23'),
    ('8.2', 'Project scripts and their respective purposes', '24'),
    ('9.1', 'Model comparison results — test accuracy and F1-scores', '26'),
    ('9.2', 'Per-class performance metrics for the CNN-LSTM model', '28'),
    ('11.1','Comparison of this work with prior published results', '39'),
]
for num, title, page in tables_list:
    story.append(Paragraph(f'<b>Table {num}</b>  —  {title} {"." * max(2, 56 - len(title))} {page}', TOC))
story.append(PageBreak())

# ── CH 1 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 1 — Introduction', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('1.1  Background and Motivation', SEC))
story.append(Paragraph(
    'Human communication is inherently multi-dimensional. While words convey information, '
    'the emotional tone of a speaker\'s voice carries meaning that extends far beyond the '
    'literal content of the message. Emotions such as anger, happiness, sadness, and '
    'neutrality are naturally expressed through changes in pitch, energy, speaking rate, '
    'and spectral characteristics of the voice. Speech Emotion Recognition (SER) is the '
    'automated task of detecting these emotional states from audio recordings — a field '
    'at the intersection of signal processing, machine learning, and affective computing.', BODY))
story.append(Paragraph(
    'The ability of machines to understand human emotion from voice has profound implications '
    'across many real-world domains. Customer service call centers can use SER to monitor '
    'caller satisfaction in real time. Mental health platforms can detect early signs of '
    'depression or anxiety from subtle voice patterns. E-learning systems can adapt content '
    'delivery based on a learner\'s emotional engagement. Smart virtual assistants can '
    'provide more empathetic and contextually appropriate responses.', BODY))
story.append(Paragraph('1.2  Project Overview', SEC))
story.append(Paragraph(
    'This project builds a complete, end-to-end Speech Emotion Recognition system. Starting '
    'from raw audio recordings sourced from RAVDESS, TESS, and EMO-DB datasets, the system '
    'extracts a rich 184-dimensional feature vector comprising seven acoustic feature types. '
    'A 4x data augmentation pipeline expands the training corpus from approximately 5,131 '
    'to over 20,524 samples. Three deep neural network architectures — LSTM baseline, '
    'CNN-LSTM hybrid, and Transformer Encoder — are designed, trained, and rigorously '
    'compared. The best performing model is integrated into an interactive Gradio web '
    'application for real-time emotion detection.', BODY))
story.append(Paragraph('1.3  Scope of the Project', SEC))
for pt in [
    'Design and implement a complete audio-to-emotion classification pipeline in software, requiring no specialized hardware.',
    'Combine three benchmark speech emotion datasets for a diverse, multi-speaker, multi-language training corpus.',
    'Engineer a comprehensive 184-dimensional feature set including four novel additions beyond the open-source baseline.',
    'Apply a 4x data augmentation pipeline to expand the training corpus and reduce overfitting.',
    'Train and systematically compare three deep learning architectures on the same dataset.',
    'Develop a Gradio web application for real-time emotion detection with waveform and spectrogram visualization.',
    'Evaluate model performance using accuracy, F1-score, precision, recall, and per-class metrics.',
]:
    story.append(Paragraph(f'\u2022  {pt}', BULL))
story.append(Paragraph('1.4  Report Organization', SEC))
story.append(Paragraph(
    'This report is organized into fourteen chapters covering problem statement, literature '
    'survey, datasets, feature extraction, augmentation, model architectures, implementation, '
    'results, web application, comparison with prior work, limitations, future scope, and '
    'conclusion. References and an appendix follow.', BODY))
story.append(PageBreak())

# ── CH 2 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 2 — Problem Statement and Objectives', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('2.1  Problem Statement', SEC))
story.append(Paragraph('Despite significant progress in SER, several critical challenges remain unaddressed in existing open-source implementations:', BODY))
for pt in [
    'Most existing SER systems are trained on a single dataset, severely limiting generalization to unseen speakers, accents, and recording conditions.',
    'The majority of implementations rely solely on MFCC features, neglecting complementary acoustic cues such as energy, spectral brightness, and harmonic content.',
    'Few open-source projects apply data augmentation, leaving models vulnerable to overfitting on small speech emotion datasets.',
    'Systematic fair comparison of LSTM, CNN-LSTM, and Transformer architectures on the same combined dataset is largely absent.',
    'Real-time, accessible web interfaces for speech emotion demonstration are rarely provided alongside academic implementations.',
]:
    story.append(Paragraph(f'\u2022  {pt}', BULL))
story.append(Paragraph('2.2  Objectives', SEC))
story.append(Paragraph('This project addresses the above gaps through the following specific objectives:', BODY))
for i, obj in enumerate([
    'Extract a 184-dimensional feature vector combining MFCC, Chroma STFT, Mel Spectrogram, Zero Crossing Rate, Spectral Rolloff, RMS Energy, and Spectral Centroid.',
    'Combine RAVDESS, TESS, and EMO-DB datasets to create a diverse multi-speaker training corpus covering four emotion classes.',
    'Apply a 4x augmentation pipeline (time stretching, pitch shifting, Gaussian noise) to expand training data from ~5,131 to ~20,524 samples.',
    'Design, implement, and train three neural network architectures: LSTM baseline, CNN-LSTM hybrid, and Transformer Encoder.',
    'Evaluate all three models on a held-out test set using accuracy, F1-score, precision, recall, and per-class metrics.',
    'Develop a Gradio-based interactive web application with waveform visualization, Mel spectrogram, and real-time confidence output.',
], 1):
    story.append(Paragraph(f'({i})  {obj}', BODY_I))
story.append(PageBreak())

# ── CH 3 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 3 — Literature Survey', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'Research in Speech Emotion Recognition spans over two decades, evolving from classical '
    'machine learning to modern deep learning. The following survey covers the most relevant '
    'prior work that contextualizes the contributions of this project.', BODY))
story.append(Paragraph('3.1  Classical Machine Learning Approaches', SEC))
story.append(Paragraph(
    'Early SER systems relied on hand-crafted acoustic features fed into classical classifiers. '
    'Stuhlsatz et al. (2011) demonstrated that Support Vector Machines combined with MFCC '
    'features could achieve 77.4% accuracy on the EMO-DB dataset. While effective for small, '
    'controlled datasets, SVM-based approaches struggle to capture temporal dynamics inherent '
    'in emotional speech. Fayek et al. (2017) evaluated Deep Neural Networks on the IEMOCAP '
    'corpus, achieving 64.7% accuracy, highlighting the limitations of DNNs on small datasets '
    'due to overfitting — underscoring the need for augmentation strategies.', BODY))
story.append(Paragraph('3.2  Recurrent and Convolutional Approaches', SEC))
story.append(Paragraph(
    'Zhao et al. (2019) introduced deep 1D and 2D CNN-LSTM networks for SER, recognizing '
    'that emotional speech carries both local spectral patterns (captured by CNNs) and '
    'temporal dependencies (captured by LSTMs). Their hybrid approach on RAVDESS achieved '
    '70.1% accuracy. Issa et al. (2020) demonstrated that combining CNN with Mel spectrograms '
    'produces 74.2% accuracy on RAVDESS+EMO-DB, pointing to the value of the Mel spectrogram '
    'as a rich visual representation of emotional speech.', BODY))
story.append(Paragraph('3.3  Open-Source Baseline', SEC))
story.append(Paragraph(
    'The open-source repository by x4nth055 (2019) provides an LSTM-based SER system '
    'trained on RAVDESS and TESS using MFCC, Chroma, and Mel features, achieving '
    'approximately 77.2% accuracy. This serves as the baseline for this project. However, '
    'it lacks data augmentation, additional feature engineering, systematic architecture '
    'comparison, and an interactive web demonstration — all of which are addressed here.', BODY))
story.append(Paragraph('3.4  Literature Comparison Table', SEC))

# FIX 1: Table 3.1 — all on one page, proper widths that sum to PW
# PW = ~16.3 cm. Use 6 cols: 3.0 + 1.5 + 3.2 + 3.2 + 1.7 + 3.7 = 17.3 — too wide
# Use smaller font and tighter widths: 2.8+1.4+3.0+3.2+1.6+3.3 = 15.3 -> ok
lit_widths = [2.8*cm, 1.4*cm, 3.0*cm, 3.2*cm, 1.6*cm, 3.3*cm]
story.append(KeepTogether([
    tbl(
        ['Author(s)', 'Year', 'Method', 'Dataset', 'Acc.', 'Limitation'],
        [
            ['Stuhlsatz et al.', '2011', 'SVM + MFCC', 'EMO-DB', '77.4%', 'Single dataset, no deep learning'],
            ['Fayek et al.', '2017', 'DNN + MFCC', 'IEMOCAP', '64.7%', 'Small dataset, no augmentation'],
            ['Zhao et al.', '2019', 'CNN-LSTM', 'RAVDESS', '70.1%', 'No feature ablation study'],
            ['Issa et al.', '2020', 'CNN + Mel', 'RAVDESS + EMO-DB', '74.2%', 'No noise robustness test'],
            ['x4nth055', '2019', 'LSTM + MFCC/Mel', 'RAVDESS + TESS', '77.2%', 'No augmentation, no demo'],
            ['This Work', '2025-26', 'CNN-LSTM + 7 features', 'RAVDESS + TESS + EMO-DB', '89.7%', 'Local deployment only'],
        ],
        lit_widths, font_size=9
    ),
    Paragraph('Table 3.1: Comparison of related work in Speech Emotion Recognition.', FIG),
]))
story.append(PageBreak())

# ── CH 4 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 4 — Datasets Used', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'Three publicly available, well-established speech emotion benchmark datasets are '
    'combined to form the training and evaluation corpus. Using multiple datasets ensures '
    'speaker diversity, acoustic variety, and improved model generalization.', BODY))
story.append(Paragraph('4.1  RAVDESS', SEC))
story.append(Paragraph(
    'The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS) comprises '
    'recordings from 24 professional actors (12 male, 12 female) vocalizing two semantically '
    'neutral sentences in North American English across eight emotion levels and two '
    'intensity levels. Four emotion classes — Angry, Happy, Neutral, and Sad — are selected, '
    'yielding approximately 4,390 training-relevant audio clips.', BODY))
story.append(Paragraph('4.2  TESS', SEC))
story.append(Paragraph(
    'The Toronto Emotional Speech Set (TESS) features two female actresses (aged 26 and 64) '
    'speaking 200 target words across seven emotion categories. TESS provides high emotional '
    'clarity and clean studio recordings, complementing RAVDESS. Approximately 741 clips '
    'relevant to the four target emotion classes are utilized.', BODY))
story.append(Paragraph('4.3  EMO-DB', SEC))
story.append(Paragraph(
    'The Berlin Database of Emotional Speech (EMO-DB) is a German-language dataset recorded '
    'in the anechoic chamber of the Technical University of Berlin. Ten professional actors '
    '(5 male, 5 female) performed ten German sentences across seven emotion categories. The '
    'German-language data introduces acoustic variation that contributes positively to model '
    'robustness. Approximately 454 EMO-DB clips are included after filtering for the four '
    'target emotion classes.', BODY))

# FIX 2: Table 4.1 — proper widths summing to PW
# 3.5 + 3.2 + 2.3 + 2.8 + 4.5 = 16.3 cm = PW ✓
story.append(KeepTogether([
    tbl(
        ['Dataset', 'Speakers', 'Language', 'Emotions Used', 'Clips (Approx.)'],
        [
            ['RAVDESS', '24 (12M, 12F)', 'English', '4 of 8', '~4,390'],
            ['TESS', '2 (Female)', 'English', '4 of 7', '~741'],
            ['EMO-DB', '10 (5M, 5F)', 'German', '4 of 7', '~454'],
            ['TOTAL', '36 speakers', 'Multi', '4 classes', '~5,131 (before augmentation)'],
        ],
        [3.4*cm, 3.0*cm, 2.4*cm, 2.9*cm, 4.6*cm],
        hc=TH_GREEN, ac=TH_ALT_GREEN, font_size=10
    ),
    Paragraph('Table 4.1: Datasets used in this project with key statistics.', FIG),
]))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'After applying the 4x augmentation pipeline, the effective training set grows to '
    '20,524 samples: Neutral (9,040), Angry (3,828), Happy (3,816), and Sad (3,840). '
    'The higher neutral count reflects the natural prevalence of neutral speech in '
    'RAVDESS and TESS.', BODY))
story.append(PageBreak())

# ── CH 5 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 5 — Feature Extraction', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'Raw audio waveforms cannot be directly processed by neural networks. Feature '
    'extraction converts each variable-length audio clip into a fixed-length numerical '
    'vector that captures the acoustic characteristics relevant for emotion classification. '
    'All feature extraction is performed using the librosa library at a standardized '
    'sample rate of 16,000 Hz.', BODY))
story.append(Paragraph('5.1  Feature Pipeline', SEC))

# FIX 3: Table 5.1 — feature pipeline. Overlap was from col widths too narrow.
# 4 cols: 4.5 + 2.0 + 5.8 + 4.0 = 16.3 ✓
story.append(KeepTogether([
    tbl(
        ['Feature Type', 'Dims', 'What It Captures', 'Status'],
        [
            ['MFCC (Mel-Frequency Cepstral Coefficients)', '40', 'Vocal tract shape — tone fingerprint of the voice', 'Baseline'],
            ['Chroma STFT', '12', 'Pitch class content — harmonic structure of speech', 'Baseline'],
            ['Mel Spectrogram', '128', 'Frequency-time energy map of the voice', 'Baseline'],
            ['Zero Crossing Rate (ZCR)', '1', 'Voiced vs. unvoiced regions — high in angry speech', 'NEW (ours)'],
            ['Spectral Rolloff', '1', 'Frequency brightness — higher in happy speech', 'NEW (ours)'],
            ['RMS Energy', '1', 'Overall loudness — high in angry speech', 'NEW (ours)'],
            ['Spectral Centroid', '1', 'Center of spectral mass — voice brightness', 'NEW (ours)'],
            ['TOTAL', '184', 'Combined per-clip feature vector', '—'],
        ],
        [4.5*cm, 1.5*cm, 6.5*cm, 3.8*cm], font_size=9
    ),
    Paragraph('Table 5.1: Feature extraction pipeline — 7 feature types, 184 total dimensions.', FIG),
]))
story.append(Paragraph('5.2  Feature Descriptions', SEC))
story.append(Paragraph(
    '<b>MFCC (40 coefficients):</b> Mel-Frequency Cepstral Coefficients represent the '
    'short-term power spectrum of audio mapped to the mel frequency scale, approximating '
    'the human auditory system\'s response. The first coefficients capture the overall '
    'spectral envelope — the most discriminative cue for emotion recognition.', BODY))
story.append(Paragraph(
    '<b>Chroma STFT (12 coefficients):</b> Chroma features represent the energy distribution '
    'across the 12 pitch classes of the musical octave, capturing harmonic and melodic '
    'content that reflects tonal variation in emotional speech.', BODY))
story.append(Paragraph(
    '<b>Mel Spectrogram (128 coefficients):</b> A frequency-time energy map computed using '
    'a mel-scale filterbank. It provides the richest single feature representation, '
    'capturing both spectral and temporal dynamics simultaneously.', BODY))
story.append(Paragraph(
    '<b>ZCR, Spectral Rolloff, RMS Energy, Spectral Centroid (4 NEW features):</b> '
    'These scalar features are novel additions beyond the baseline. ZCR measures signal '
    'sign changes — high in energetic angry speech. Spectral Rolloff captures frequency '
    'brightness. RMS Energy measures overall loudness. Spectral Centroid represents the '
    'center of mass of the spectrum, distinguishing bright happy voices from darker sad ones.', BODY))
story.append(PageBreak())

# ── CH 6 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 6 — Data Augmentation', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'Deep learning models require substantial training data to learn robust representations '
    'and avoid overfitting. The combined dataset at approximately 5,131 clips is relatively '
    'small by deep learning standards. A systematic 4x data augmentation pipeline is applied, '
    'creating three synthetic variants of every original audio clip.', BODY))

# FIX 4: Table 6.1 — 3 cols with proper widths. 3.0 + 6.0 + 7.3 = 16.3 ✓
story.append(KeepTogether([
    tbl(
        ['Technique', 'Implementation', 'Effect on Training Data'],
        [
            ['Time Stretching',
             'librosa.effects.time_stretch(rate=1.1)\nSpeeds audio up by 10%',
             'Simulates fast speakers; same emotional content at a different delivery rate'],
            ['Pitch Shifting',
             'librosa.effects.pitch_shift(n_steps=2)\nRaises pitch by 2 semitones',
             'Simulates cross-gender voice variation; same words at a higher voice frequency'],
            ['Gaussian Noise Injection',
             'Add Gaussian noise with sigma=0.005\n(approx. 20 dB SNR)',
             'Simulates real-world microphone noise and background interference conditions'],
            ['Overall Result',
             '4x total dataset size:\n~5,131 → ~20,524 samples',
             'Model sees substantially more variation — less overfitting, better generalization to unseen voices'],
        ],
        [3.0*cm, 5.8*cm, 7.5*cm], font_size=9
    ),
    Paragraph('Table 6.1: Data augmentation techniques applied in this project.', FIG),
]))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'Each augmentation preserves the emotional label of the original clip. The result is '
    'a model that has seen substantially more acoustic variation during training, leading '
    'to better generalization to unseen voices, microphone conditions, and speaking styles.', BODY))
story.append(PageBreak())

# ── CH 7 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 7 — Model Architectures', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'Three neural network architectures are designed and compared. All models receive '
    'the same 184-dimensional feature vector reshaped as a (184, 1) sequence and produce '
    'a 4-class softmax output corresponding to Angry, Happy, Neutral, and Sad.', BODY))
story.append(Paragraph('7.1  Model A: LSTM Baseline', SEC))
story.append(Paragraph(
    'The LSTM Baseline follows the architecture of the original open-source repository '
    'and serves as the performance reference point. Long Short-Term Memory networks are '
    'a class of Recurrent Neural Networks designed to capture temporal dependencies in '
    'sequential data by maintaining a cell state that determines which information to '
    'retain and which to discard.', BODY))
story.append(Paragraph(
    '<b>Architecture:</b> Input(184,1) → LSTM(128, return_sequences=True) → Dropout(0.3) '
    '→ LSTM(64) → Dropout(0.3) → Dense(64, ReLU) → Dropout(0.3) → Dense(4, Softmax)', BODY_I))
story.append(Paragraph('<b>Parameters:</b> ~120,388   |   <b>Test Accuracy:</b> 70.3%', BODY_I))
story.append(Paragraph('7.2  Model B: CNN-LSTM Hybrid (Primary Contribution)', SEC))
story.append(Paragraph(
    'The CNN-LSTM Hybrid is the primary architectural contribution of this project. '
    'Conv1D layers first scan the feature sequence to detect local patterns — sudden '
    'amplitude spikes in angry speech, high-frequency bursts in happy speech — and '
    'produce a compact feature map. The LSTM then models temporal relationships between '
    'the extracted patterns. Batch Normalization layers are added after each convolution '
    'to stabilize and accelerate training.', BODY))
story.append(Paragraph(
    '<b>Architecture:</b> Input(184,1) → Conv1D(64,k=5) → BatchNorm → MaxPool(2) '
    '→ Conv1D(128,k=3) → BatchNorm → MaxPool(2) → LSTM(64) → Dropout(0.4) '
    '→ Dense(64, ReLU) → Dropout(0.3) → Dense(4, Softmax)', BODY_I))
story.append(Paragraph('<b>Parameters:</b> ~79,684   |   <b>Test Accuracy:</b> 89.7%', BODY_I))
story.append(Paragraph('7.3  Model C: Transformer Encoder', SEC))
story.append(Paragraph(
    'The Transformer Encoder applies Multi-Head Self-Attention to the feature sequence, '
    'allowing every position to attend to every other position simultaneously — capturing '
    'long-range dependencies that LSTMs may miss. Two stacked Transformer blocks are used, '
    'each comprising Multi-Head Attention (4 heads) followed by Layer Normalization and a '
    'Feed-Forward sublayer, the same technology used in GPT and BERT.', BODY))
story.append(Paragraph(
    '<b>Architecture:</b> Input(184,1) → Dense(64) → TransformerBlock×2 [MultiHeadAttention(4 heads) '
    '+ Add&Norm + FeedForward(128) + Add&Norm] → GlobalAveragePooling → Dense(64, ReLU) '
    '→ Dropout(0.3) → Dense(4, Softmax)', BODY_I))
story.append(Paragraph(
    '<b>Parameters:</b> ~170,948   |   <b>Note:</b> Training was stopped early due to computational '
    'constraints on local hardware; the Transformer was still converging when stopped.', BODY_I))

# FIX 5: Table 7.1 — 5 cols. 3.0+3.2+2.2+2.8+5.1=16.3 ✓
story.append(KeepTogether([
    tbl(
        ['Model', 'Architecture Type', 'Parameters', 'Test Accuracy', 'Notes'],
        [
            ['LSTM Baseline', 'Recurrent (2-layer LSTM)', '~120K', '70.3%', 'Same as original open-source repo'],
            ['CNN-LSTM Hybrid', 'Hybrid: CNN + LSTM', '~80K', '89.7%', 'Best model — primary contribution'],
            ['Transformer Encoder', 'Attention-based (2 blocks)', '~171K', 'Converging (stopped early)', 'State-of-the-art approach'],
        ],
        [3.0*cm, 3.5*cm, 2.2*cm, 3.0*cm, 4.6*cm], font_size=9
    ),
    Paragraph('Table 7.1: Summary of three neural network architectures.', FIG),
]))
story.append(PageBreak())

# ── CH 8 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 8 — Implementation Details', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('8.1  Development Environment', SEC))
story.append(tbl(
    ['Component', 'Version / Details'],
    [
        ['Operating System', 'macOS (Apple M3, 16 GB RAM)'],
        ['Python', '3.11.15'],
        ['TensorFlow / Keras', '2.16.2 / 3.14.0 (Metal GPU acceleration)'],
        ['librosa', '0.11.0'],
        ['scikit-learn', '1.8.0'],
        ['NumPy', '1.26.4'],
        ['Pandas', '3.0.2'],
        ['Matplotlib', '3.10.9'],
        ['Gradio', '6.14.0'],
    ],
    [5.5*cm, 10.8*cm], font_size=10
))
story.append(Paragraph('Table 8.1: Software stack and development environment.', FIG))
story.append(Paragraph('8.2  Training Configuration', SEC))
for item in [
    'Maximum epochs: 100 with early stopping (patience=10 for LSTM/CNN-LSTM, patience=15 for Transformer)',
    'Batch size: 32',
    'Optimizer: Adam with initial learning rate 1e-3 (1e-4 for Transformer)',
    'Loss function: Categorical Cross-Entropy',
    'Learning rate scheduler: ReduceLROnPlateau (factor=0.5, patience=5, min_lr=1e-6)',
    'Train/test split: 80% / 20% with stratification by emotion class',
]:
    story.append(Paragraph(f'\u2022  {item}', BULL))
story.append(Paragraph('8.3  Project Scripts', SEC))

# FIX 6: Table 8.2 — 2 cols. 4.5 + 11.8 = 16.3 ✓
story.append(KeepTogether([
    tbl(
        ['Script', 'Purpose'],
        [
            ['augment_and_extract.py',
             'Loads all audio files from RAVDESS, TESS, and EMO-DB. Applies 4x augmentation '
             '(time stretch, pitch shift, noise). Extracts 7 acoustic features per clip. '
             'Saves feature matrix X_all.npy and label vector y_all.npy to disk.'],
            ['train_all_models.py',
             'Loads extracted features, trains LSTM baseline, CNN-LSTM hybrid, and Transformer '
             'Encoder sequentially. Saves all trained models (.keras format), scaler.pkl, '
             'label_encoder.pkl, and model comparison results.'],
            ['app.py',
             'Gradio web application. Loads the pre-trained CNN-LSTM model, scaler, and label '
             'encoder at startup. Accepts audio file upload or microphone recording. Outputs '
             'predicted emotion, confidence scores, waveform plot, and Mel spectrogram.'],
        ],
        [4.5*cm, 11.8*cm], font_size=9
    ),
    Paragraph('Table 8.2: Project scripts and their respective purposes.', FIG),
]))
story.append(Paragraph('8.4  GitHub Repository', SEC))
story.append(Paragraph(
    'The complete project source code, trained model artifacts, and the Gradio web '
    'application are available at: https://github.com/sagar141202/8th_sem_project.git', BODY))
story.append(PageBreak())

# ── CH 9 ────────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 9 — Results and Analysis', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('9.1  Model Comparison', SEC))
story.append(tbl(
    ['Model', 'Test Accuracy', 'Macro F1', 'Precision (avg)', 'Recall (avg)'],
    [
        ['LSTM Baseline', '70.3%', '0.67', '0.73', '0.64'],
        ['CNN-LSTM Hybrid', '89.7%', '0.89', '0.90', '0.89'],
        ['Transformer Encoder', 'Early stopped', '—', '—', '—'],
    ],
    [4.5*cm, 3.0*cm, 2.5*cm, 3.1*cm, 3.2*cm], font_size=10
))
story.append(Paragraph('Table 9.1: Model comparison results on the held-out test set.', FIG))
story.append(Paragraph('9.2  CNN-LSTM Per-Class Performance', SEC))
story.append(tbl(
    ['Emotion', 'Precision', 'Recall', 'F1-Score', 'Test Samples'],
    [
        ['Angry', '0.93', '0.89', '0.91', '766'],
        ['Happy', '0.93', '0.83', '0.88', '763'],
        ['Neutral', '0.89', '0.93', '0.91', '1,808'],
        ['Sad', '0.85', '0.89', '0.87', '768'],
        ['Weighted Average', '0.90', '0.90', '0.90', '4,105'],
    ],
    [4.0*cm, 3.0*cm, 3.0*cm, 3.0*cm, 3.3*cm],
    hc=TH_GREEN, ac=TH_ALT_GREEN, font_size=10
))
story.append(Paragraph('Table 9.2: Per-class performance metrics for the CNN-LSTM model.', FIG))
story.append(Paragraph('9.3  Analysis of Results', SEC))
story.append(Paragraph(
    'The CNN-LSTM hybrid achieves 89.7% test accuracy, a 19.4 percentage point improvement '
    'over the LSTM baseline at 70.3%. This substantial gain is attributable to the model\'s '
    'ability to simultaneously capture local spectral patterns through Conv1D layers and '
    'long-range temporal dependencies through the LSTM layer. The Batch Normalization '
    'layers contribute to training stability and faster convergence.', BODY))
story.append(Paragraph(
    'At the per-class level, Angry speech achieves the highest F1-score of 0.91, consistent '
    'with the acoustic literature — anger produces distinctive high-energy, high-zero-crossing-rate '
    'patterns. Neutral speech also achieves F1 of 0.91, benefiting from its large test support '
    'of 1,808 samples. Happy (F1=0.88) and Sad (F1=0.87) represent more challenging classes '
    'due to acoustic similarity at moderate intensity levels. No class falls below 0.85, '
    'indicating robust and balanced classification across all four emotions.', BODY))
story.append(PageBreak())

# ── CH 10 — ONE IMAGE PAIR PER PAGE ────────────────────────────────
story.append(Paragraph('Chapter 10 — Gradio Web Application', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'An interactive real-time web application is developed using Gradio (version 6.14.0). '
    'The application loads the pre-trained CNN-LSTM model, feature scaler, and label encoder '
    'at startup, making the system ready for immediate inference from any web browser.', BODY))
story.append(Paragraph('10.1  Application Features', SEC))
for f in [
    'Audio input via file upload (WAV format recommended) or live microphone recording',
    'Automatic prediction triggered on audio upload or change — no button click required',
    'Waveform plot with RMS energy envelope overlay, color-coded by predicted emotion',
    'Mel Spectrogram visualization using the Magma colormap for clear frequency-time display',
    'Horizontal confidence bar chart showing probability scores for all four emotion classes',
    'Prediction result panel: detected emotion, confidence %, duration, sample rate, model name',
    'Model and dataset information accordion panel for academic reference',
]:
    story.append(Paragraph(f'\u2022  {f}', BULL))

story.append(Paragraph('10.2  Application Screenshots — HAPPY Speech', SEC))
story.append(Paragraph(
    'The following screenshot demonstrates the Gradio application detecting HAPPY speech '
    'from a RAVDESS audio sample. The model classifies the audio with 99.9% confidence.', BODY))

# FIX 7: One emotion per page — HAPPY
for item in img_block('/home/claude/ss1.png', w=PW,
    caption='Figure 10.1: Gradio interface — HAPPY speech detected with 99.9% confidence. '
            'Audio: 4.94 s at 16,000 Hz. Model: CNN-LSTM (89.7% acc).'):
    story.append(item)
story.append(Spacer(1, 0.3*cm))
for item in img_block('/home/claude/ss2.png', w=PW,
    caption='Figure 10.2: Waveform + RMS energy overlay (orange) and Mel spectrogram for '
            'HAPPY speech. The orange RMS envelope indicates sustained high energy.'):
    story.append(item)
story.append(PageBreak())

# ANGRY
story.append(Paragraph('10.3  Application Screenshots — ANGRY Speech', SEC))
story.append(Paragraph(
    'The model detects ANGRY speech with 100.0% confidence — the maximum possible certainty. '
    'Angry speech produces the most acoustically distinctive signature, characterised by '
    'high amplitude, high zero-crossing rate, and a dense, high-frequency Mel spectrogram.', BODY))
for item in img_block('/home/claude/ss3.png', w=PW,
    caption='Figure 10.3: Gradio interface — ANGRY speech detected with 100.0% confidence. '
            'All other emotion classes score 0.0%, indicating unambiguous classification.'):
    story.append(item)
story.append(Spacer(1, 0.3*cm))
for item in img_block('/home/claude/ss4.png', w=PW,
    caption='Figure 10.4: Waveform + RMS energy (red) and Mel spectrogram for ANGRY speech. '
            'The red RMS envelope and dense high-frequency Mel bands characterise angry speech.'):
    story.append(item)
story.append(PageBreak())

# SAD
story.append(Paragraph('10.4  Application Screenshots — SAD Speech', SEC))
story.append(Paragraph(
    'The model detects SAD speech with 89.8% confidence. Sad speech shows lower amplitude '
    'modulation and a darker spectral profile compared to angry or happy speech. The '
    'confidence chart shows 8.4% for neutral as the next closest class.', BODY))
for item in img_block('/home/claude/ss5.png', w=PW,
    caption='Figure 10.5: Gradio interface — SAD speech detected with 89.8% confidence. '
            'All emotion scores: sad 89.8%, neutral 8.4%, happy 1.2%, angry 0.5%.'):
    story.append(item)
story.append(Spacer(1, 0.3*cm))
for item in img_block('/home/claude/ss6.png', w=PW,
    caption='Figure 10.6: Confidence score bar chart for SAD prediction. The blue bar '
            'clearly dominates at 89.8%, confirming correct classification.'):
    story.append(item)
story.append(PageBreak())

# NEUTRAL
story.append(Paragraph('10.5  Application Screenshots — NEUTRAL Speech', SEC))
story.append(Paragraph(
    'The model detects NEUTRAL speech with 76.4% confidence. Neutral speech is the most '
    'acoustically ambiguous class — it overlaps with sad (18.1%) and happy (4.4%) at the '
    'boundary. Despite this, the model correctly identifies it as the dominant emotion.', BODY))
for item in img_block('/home/claude/ss7.png', w=PW,
    caption='Figure 10.7: Gradio interface — NEUTRAL speech detected with 76.4% confidence. '
            'All emotion scores: neutral 76.4%, sad 18.1%, happy 4.4%, angry 1.2%.'):
    story.append(item)
story.append(Spacer(1, 0.3*cm))
for item in img_block('/home/claude/ss8.png', w=PW,
    caption='Figure 10.8: Confidence score bar chart for NEUTRAL prediction. The purple '
            'bar leads at 76.4%, with blue (sad) at 18.1% as the next closest class.'):
    story.append(item)
story.append(PageBreak())

# ── CH 11 ───────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 11 — Comparison with Prior Work', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))

# FIX 8: Table 11.1 — 6 cols fitting PW. 3.5+1.5+3.5+2.2+2.2+3.4=16.3 ✓
story.append(KeepTogether([
    tbl(
        ['Method', 'Year', 'Dataset', 'Accuracy', 'Augment.', 'Multi-arch'],
        [
            ['SVM + MFCC', '2011', 'EMO-DB', '77.4%', 'No', 'No'],
            ['DNN + MFCC', '2017', 'IEMOCAP', '64.7%', 'No', 'No'],
            ['LSTM', '2019', 'RAVDESS', '70.1%', 'No', 'No'],
            ['CNN + Mel Spectrogram', '2020', 'RAVDESS + EMO-DB', '74.2%', 'No', 'No'],
            ['x4nth055 LSTM baseline', '2019', 'RAVDESS + TESS', '77.2%', 'No', 'No'],
            ['This Work (CNN-LSTM)', '2025-26', 'RAVDESS + TESS + EMO-DB', '89.7%', '4x', 'Yes (3)'],
        ],
        [3.5*cm, 1.5*cm, 3.5*cm, 2.2*cm, 2.2*cm, 3.4*cm], font_size=9
    ),
    Paragraph('Table 11.1: Comparison of this work with prior published results.', FIG),
]))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'This project achieves 89.7% test accuracy on the combined RAVDESS+TESS+EMO-DB corpus, '
    'representing a 12.5 percentage point improvement over the strongest prior result on '
    'a comparable dataset. This gain is attributable to multi-dataset training for improved '
    'generalization, the 4x augmentation pipeline reducing overfitting, and the hybrid '
    'CNN-LSTM architecture capturing both local and temporal acoustic patterns.', BODY))
story.append(PageBreak())

# ── CH 12 ───────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 12 — Advantages and Limitations', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('12.1  Advantages', SEC))
for a in [
    'Multi-dataset training across RAVDESS, TESS, and EMO-DB provides substantially greater speaker diversity and acoustic variety than single-dataset systems.',
    'The 4x augmentation pipeline effectively expands the training corpus and reduces overfitting without additional data collection.',
    'The CNN-LSTM hybrid architecture delivers 89.7% test accuracy — a 19.4 percentage point improvement over the LSTM baseline.',
    'Seven complementary acoustic features provide a rich 184-dimensional representation capturing multiple independent dimensions of emotional speech.',
    'The Gradio web interface provides an accessible, real-time demonstration platform with waveform, Mel spectrogram, and confidence visualization.',
    'The complete system requires no specialized hardware and runs on a standard consumer laptop with Apple Silicon acceleration.',
]:
    story.append(Paragraph(f'\u2022  {a}', BULL))
story.append(Paragraph('12.2  Limitations', SEC))
for l in [
    'The system is currently limited to four emotion classes. Extending to the full set of eight emotions available in the datasets remains as future work.',
    'The Transformer Encoder training was terminated early due to computational constraints, preventing a complete multi-architecture comparison.',
    'The system operates on file-level predictions. Frame-level, streaming real-time inference has not been implemented.',
    'Performance on completely out-of-domain audio (non-dataset speakers, spontaneous conversational speech) has not been formally evaluated.',
    'The application is deployed only locally at http://127.0.0.1:7860. Public cloud deployment on Hugging Face Spaces is planned.',
]:
    story.append(Paragraph(f'\u2022  {l}', BULL))
story.append(PageBreak())

# ── CH 13 ───────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 13 — Future Scope', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    'The current system establishes a strong baseline. The following directions are '
    'identified for future development:', BODY))
for title, desc in [
    ('Extended Emotion Classes', 'Expand from 4 to 7 or 8 emotion classes by incorporating Fear, Disgust, and Surprised categories from RAVDESS and TESS.'),
    ('Wav2Vec2 Embeddings', 'Replace hand-crafted features with pre-trained Facebook Wav2Vec2 deep embeddings, which have demonstrated state-of-the-art SER performance with minimal fine-tuning.'),
    ('Multimodal Fusion', 'Combine speech emotion with facial expression recognition from webcam video to improve accuracy on emotionally ambiguous utterances.'),
    ('Public Cloud Deployment', 'Deploy the Gradio application on Hugging Face Spaces or Render to provide a publicly accessible demonstration link.'),
    ('Frame-Level Streaming', 'Implement real-time sliding-window inference for continuous emotion monitoring during live conversations.'),
    ('Cross-Corpus Evaluation', 'Train on RAVDESS+TESS and evaluate on CREMA-D to formally measure generalization to completely unseen speakers.'),
    ('Edge Deployment', 'Export the CNN-LSTM model to TensorFlow Lite and deploy on a Raspberry Pi for resource-constrained embedded applications.'),
]:
    story.append(Paragraph(f'<b>{title}:</b>  {desc}', BULL))
story.append(PageBreak())

# ── CH 14 ───────────────────────────────────────────────────────────
story.append(Paragraph('Chapter 14 — Conclusion', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
for para in [
    'This project successfully delivers a complete, end-to-end Speech Emotion Recognition '
    'system that substantially improves upon the open-source baseline in accuracy, '
    'architectural sophistication, and feature engineering.',
    'Starting from raw audio recordings across three benchmark datasets — RAVDESS, TESS, '
    'and EMO-DB — the system extracts a comprehensive 184-dimensional feature vector '
    'combining seven acoustic feature types. A 4x augmentation pipeline expands the '
    'training corpus from approximately 5,131 to 20,524 samples. Three deep learning '
    'architectures are designed, trained, and compared on the same dataset.',
    'The CNN-LSTM hybrid model achieves 89.7% test accuracy with per-class F1-scores '
    'ranging from 0.87 to 0.91, representing a 19.4 percentage point improvement over '
    'the LSTM baseline and outperforming all comparable prior work. The complete system '
    'is deployed as an interactive Gradio web application providing real-time waveform, '
    'Mel spectrogram, and confidence score visualization.',
    'The project demonstrates that a well-engineered combination of multi-dataset training, '
    'data augmentation, extended feature sets, and hybrid deep learning architecture can '
    'achieve robust, high-accuracy speech emotion recognition without requiring large '
    'computational resources, making the system practical for real-world deployment on '
    'standard consumer hardware.',
]:
    story.append(Paragraph(para, BODY))
    story.append(Spacer(1, 0.2*cm))
story.append(PageBreak())

# ── REFERENCES ──────────────────────────────────────────────────────
story.append(Paragraph('References', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
refs = [
    'Stuhlsatz, A., Meyer, C., Eyben, F., Zielke, T., Meier, G., & Schuller, B. (2011). Deep neural networks for acoustic emotion recognition: raising the benchmarks. In <i>Proceedings of IEEE ICASSP</i>, pp. 5688–5691.',
    'Fayek, H. M., Lech, M., & Cavedon, L. (2017). Evaluating deep learning architectures for speech emotion recognition. <i>Neural Networks</i>, 92, 60–68.',
    'Zhao, J., Mao, X., & Chen, L. (2019). Speech emotion recognition using deep 1D and 2D CNN LSTM networks. <i>Biomedical Signal Processing and Control</i>, 47, 312–323.',
    'Issa, D., Demirci, M. F., & Yazici, A. (2020). Speech emotion recognition with deep convolutional neural networks. <i>Biomedical Signal Processing and Control</i>, 59, 101894.',
    'Livingstone, S. R., & Russo, F. A. (2018). The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS). <i>PLOS ONE</i>, 13(5), e0196391.',
    'Pichora-Fuller, M. K., & Dupuis, K. (2020). Toronto Emotional Speech Set (TESS). <i>Scholars Portal Dataverse</i>. https://doi.org/10.5683/SP2/E8H2MF',
    'Burkhardt, F., Paeschke, A., Rolfes, M., Sendlmeier, W., & Weiss, B. (2005). A database of German emotional speech. In <i>Proceedings of Interspeech</i>, pp. 1517–1520.',
    'Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. <i>Advances in Neural Information Processing Systems</i>, 30.',
    'McFee, B., Raffel, C., Liang, D., Ellis, D. P., McVicar, M., Battenberg, E., & Nieto, O. (2015). librosa: Audio and music signal analysis in Python. In <i>Proceedings of the 14th Python in Science Conference</i>, pp. 18–25.',
    'Abadi, M., Barham, P., Chen, J., Chen, Z., Davis, A., Dean, J., ... & Zheng, X. (2016). TensorFlow: A system for large-scale machine learning. In <i>12th USENIX Symposium on Operating Systems Design and Implementation</i>, pp. 265–283.',
    'Abid, A., Abdalla, A., Abid, A., Khan, D., Alfozan, A., & Zou, J. (2019). Gradio: Hassle-free sharing and testing of ML models in the wild. <i>arXiv preprint</i>, arXiv:1906.02569.',
    'Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. <i>Advances in Neural Information Processing Systems</i>, 30.',
    'Fadheli, A. (2019). Speech Emotion Recognition. <i>GitHub repository</i>. https://github.com/x4nth055/emotion-recognition-using-speech',
]
for i, r in enumerate(refs, 1):
    story.append(Paragraph(f'[{i}]  {r}', REF))
story.append(PageBreak())

# ── APPENDIX ────────────────────────────────────────────────────────
story.append(Paragraph('Appendix', CH))
story.append(HRFlowable(width='100%', thickness=0.8, color=BLACK))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('A.1  Feature Extraction Code (Key Snippet)', SEC))
code_txt = (
    'def get_features(y, sr):\n'
    '    mfccs    = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)\n'
    '    chroma   = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)\n'
    '    mel      = np.mean(librosa.feature.melspectrogram(y=y, sr=sr).T, axis=0)\n'
    '    zcr      = np.mean(librosa.feature.zero_crossing_rate(y).T, axis=0)\n'
    '    rolloff  = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr).T, axis=0)\n'
    '    rms      = np.mean(librosa.feature.rms(y=y).T, axis=0)\n'
    '    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr).T, axis=0)\n'
    '    return np.hstack([mfccs, chroma, mel, zcr, rolloff, rms, centroid])'
)
story.append(Paragraph(code_txt.replace('\n', '<br/>'), CODE))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('A.2  CNN-LSTM Architecture Layer Summary', SEC))
story.append(tbl(
    ['Layer', 'Output Shape', 'Parameters'],
    [
        ['Input', '(None, 184, 1)', '0'],
        ['Conv1D(64, kernel_size=5)', '(None, 184, 64)', '384'],
        ['BatchNormalization', '(None, 184, 64)', '256'],
        ['MaxPooling1D(pool_size=2)', '(None, 92, 64)', '0'],
        ['Conv1D(128, kernel_size=3)', '(None, 92, 128)', '24,704'],
        ['BatchNormalization', '(None, 92, 128)', '512'],
        ['MaxPooling1D(pool_size=2)', '(None, 46, 128)', '0'],
        ['LSTM(64)', '(None, 64)', '49,408'],
        ['Dropout(0.4)', '(None, 64)', '0'],
        ['Dense(64, activation=ReLU)', '(None, 64)', '4,160'],
        ['Dropout(0.3)', '(None, 64)', '0'],
        ['Dense(4, activation=Softmax)', '(None, 4)', '260'],
        ['TOTAL', '—', '79,684'],
    ],
    [6.0*cm, 5.3*cm, 5.0*cm], font_size=10
))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('A.3  GitHub Repository', SEC))
story.append(Paragraph(
    'All source code, trained model artifacts (CNN-LSTM .keras file), feature scaler, '
    'label encoder, and the Gradio web application are available at:', BODY))
story.append(Paragraph('https://github.com/sagar141202/8th_sem_project', BODY_I))

# ── BUILD BODY PDF ──────────────────────────────────────────────────
body_out = os.path.join(os.path.dirname(__file__), 'report_body.pdf')
doc = SimpleDocTemplate(
    body_out, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.0*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    title='Speech Emotion Recognition Using Deep Learning — NIT Kurukshetra',
    author='Kasagani Charan Kumar & Sagar S. Maddi',
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print('Body PDF built:', body_out)
