import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing   import LabelEncoder, StandardScaler
from sklearn.metrics         import classification_report
import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import pickle
import warnings
warnings.filterwarnings("ignore")

FEAT_DIR    = "extracted_features"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

BATCH  = 32
EPOCHS = 100
SEED   = 42

tf.random.set_seed(SEED)
np.random.seed(SEED)

def load_data():
    X = np.load(os.path.join(FEAT_DIR, "X_all.npy"))
    y = np.load(os.path.join(FEAT_DIR, "y_all.npy"))

    enc   = LabelEncoder()
    y_enc = enc.fit_transform(y)
    y_cat = tf.keras.utils.to_categorical(y_enc)

    print(f"loaded X: {X.shape}  classes: {enc.classes_}")

    scaler = StandardScaler()
    X      = scaler.fit_transform(X)

    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    with open("label_encoder.pkl", "wb") as f:
        pickle.dump(enc, f)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_cat, test_size=0.2, random_state=SEED, stratify=y_enc
    )

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test  = X_test.reshape(X_test.shape[0],  X_test.shape[1],  1)

    return X_train, X_test, y_train, y_test, enc

def build_lstm(input_shape, n_classes):
    inp = layers.Input(shape=input_shape)
    x   = layers.LSTM(128, return_sequences=True)(inp)
    x   = layers.Dropout(0.3)(x)
    x   = layers.LSTM(64)(x)
    x   = layers.Dropout(0.3)(x)
    x   = layers.Dense(64, activation="relu")(x)
    x   = layers.Dropout(0.3)(x)
    out = layers.Dense(n_classes, activation="softmax")(x)
    m   = Model(inp, out, name="LSTM_baseline")
    m.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
              loss="categorical_crossentropy", metrics=["accuracy"])
    return m

def build_cnn_lstm(input_shape, n_classes):
    inp = layers.Input(shape=input_shape)
    x   = layers.Conv1D(64, kernel_size=5, activation="relu", padding="same")(inp)
    x   = layers.BatchNormalization()(x)
    x   = layers.MaxPooling1D(pool_size=2)(x)
    x   = layers.Conv1D(128, kernel_size=3, activation="relu", padding="same")(x)
    x   = layers.BatchNormalization()(x)
    x   = layers.MaxPooling1D(pool_size=2)(x)
    x   = layers.LSTM(64)(x)
    x   = layers.Dropout(0.4)(x)
    x   = layers.Dense(64, activation="relu")(x)
    x   = layers.Dropout(0.3)(x)
    out = layers.Dense(n_classes, activation="softmax")(x)
    m   = Model(inp, out, name="CNN_LSTM_hybrid")
    m.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
              loss="categorical_crossentropy", metrics=["accuracy"])
    return m

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.att   = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ff1   = layers.Dense(ff_dim, activation="relu")
        self.ff2   = layers.Dense(embed_dim)
        self.norm1 = layers.LayerNormalization(epsilon=1e-6)
        self.norm2 = layers.LayerNormalization(epsilon=1e-6)
        self.drop1 = layers.Dropout(dropout_rate)
        self.drop2 = layers.Dropout(dropout_rate)

    def call(self, x, training=False):
        attn_out = self.att(x, x)
        attn_out = self.drop1(attn_out, training=training)
        x        = self.norm1(x + attn_out)
        ff_out   = self.ff2(self.ff1(x))
        ff_out   = self.drop2(ff_out, training=training)
        return self.norm2(x + ff_out)

def build_transformer(input_shape, n_classes):
    inp = layers.Input(shape=input_shape)
    x   = layers.Dense(64)(inp)
    x   = TransformerBlock(embed_dim=64, num_heads=4, ff_dim=128)(x)
    x   = TransformerBlock(embed_dim=64, num_heads=4, ff_dim=128)(x)
    x   = layers.GlobalAveragePooling1D()(x)
    x   = layers.Dense(64, activation="relu")(x)
    x   = layers.Dropout(0.3)(x)
    out = layers.Dense(n_classes, activation="softmax")(x)
    m   = Model(inp, out, name="Transformer_encoder")
    m.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
              loss="categorical_crossentropy", metrics=["accuracy"])
    return m

def train_model(model, X_train, y_train, X_test, y_test, patience=10):
    callbacks = [
        EarlyStopping(patience=patience, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=5, min_lr=1e-6, verbose=1)
    ]
    return model.fit(X_train, y_train, validation_data=(X_test, y_test),
                     epochs=EPOCHS, batch_size=BATCH, callbacks=callbacks, verbose=1)

def evaluate(model, X_test, y_test, enc, model_name):
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"\n{model_name}  --  test accuracy: {acc:.4f}")
    preds  = model.predict(X_test, verbose=0)
    y_pred = np.argmax(preds, axis=1)
    y_true = np.argmax(y_test, axis=1)
    report = classification_report(y_true, y_pred, target_names=enc.classes_, output_dict=True)
    print(classification_report(y_true, y_pred, target_names=enc.classes_))
    return acc, report

def plot_history(history, model_name):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(history.history["accuracy"],     label="train")
    axes[0].plot(history.history["val_accuracy"], label="val")
    axes[0].set_title(f"{model_name} -- accuracy")
    axes[0].legend()
    axes[1].plot(history.history["loss"],     label="train")
    axes[1].plot(history.history["val_loss"], label="val")
    axes[1].set_title(f"{model_name} -- loss")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, f"{model_name}_curve.png"), dpi=120)
    plt.close()

def plot_comparison(results_dict):
    names = list(results_dict.keys())
    accs  = [results_dict[n]["test_accuracy"] for n in names]
    plt.figure(figsize=(8, 5))
    bars = plt.bar(names, [a * 100 for a in accs], color=["#3b82f6", "#10b981", "#f59e0b"])
    plt.ylim(50, 100)
    plt.ylabel("Test Accuracy (%)")
    plt.title("Model Comparison -- Speech Emotion Recognition")
    for bar, acc in zip(bars, accs):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{acc*100:.1f}%", ha="center", va="bottom", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "model_comparison.png"), dpi=120)
    plt.close()
    print("saved comparison chart")

def main():
    print("=== loading data ===")
    X_train, X_test, y_train, y_test, enc = load_data()
    input_shape = (X_train.shape[1], 1)
    n_classes   = y_train.shape[1]
    all_results = {}

    print("\n=== Model A: LSTM ===")
    lstm = build_lstm(input_shape, n_classes)
    lstm.summary()
    h = train_model(lstm, X_train, y_train, X_test, y_test, patience=10)
    acc, rep = evaluate(lstm, X_test, y_test, enc, "LSTM")
    plot_history(h, "LSTM")
    lstm.save(os.path.join(RESULTS_DIR, "lstm_model.keras"))
    all_results["LSTM"] = {"test_accuracy": float(acc), "report": rep}

    print("\n=== Model B: CNN-LSTM ===")
    cnn_lstm = build_cnn_lstm(input_shape, n_classes)
    cnn_lstm.summary()
    h = train_model(cnn_lstm, X_train, y_train, X_test, y_test, patience=10)
    acc, rep = evaluate(cnn_lstm, X_test, y_test, enc, "CNN-LSTM")
    plot_history(h, "CNN_LSTM")
    cnn_lstm.save(os.path.join(RESULTS_DIR, "cnn_lstm_model.keras"))
    all_results["CNN-LSTM"] = {"test_accuracy": float(acc), "report": rep}

    print("\n=== Model C: Transformer ===")
    transformer = build_transformer(input_shape, n_classes)
    transformer.summary()
    h = train_model(transformer, X_train, y_train, X_test, y_test, patience=15)
    acc, rep = evaluate(transformer, X_test, y_test, enc, "Transformer")
    plot_history(h, "Transformer")
    transformer.save(os.path.join(RESULTS_DIR, "transformer_model.keras"))
    all_results["Transformer"] = {"test_accuracy": float(acc), "report": rep}

    plot_comparison(all_results)
    with open(os.path.join(RESULTS_DIR, "model_comparison_results.json"), "w") as f:
        json.dump(all_results, f, indent=2)

    best = max(all_results, key=lambda k: all_results[k]["test_accuracy"])
    print(f"\nbest model: {best}  ({all_results[best]['test_accuracy']*100:.2f}%)")

if __name__ == "__main__":
    main()
