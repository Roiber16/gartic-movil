#!/usr/bin/env python3
"""Detección de pitidos (beeps) tonales en el audio de un gameplay.

Idea: los sonidos del juego son tonos casi puros (una sola frecuencia
dominante, amplitud alta). La voz tiene armónicos y vibrato; la música
de fondo suena más baja. Un fotograma de STFT se marca como "pitido"
cuando el pico espectral en 300-4000 Hz concentra gran parte de la
energía de la banda. Los fotogramas seguidos se agrupan en eventos con
inicio, fin, duración, frecuencia dominante y pendiente de frecuencia.

Uso: python3 analisis.py audio-2h.wav eventos-2h.csv
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft

SR = 22050
NPERSEG = 1024
HOP = 256
FMIN, FMAX = 300, 4000


def detect(path, out_csv):
    sr, data = wavfile.read(path)
    assert sr == SR, f"se esperaba {SR} Hz, llegó {sr}"
    if data.ndim > 1:
        data = data[:, 0]
    x = data.astype(np.float32) / 32768.0
    chunk = SR * 300  # 5 minutos por trozo
    events = []
    t0 = 0.0
    for start in range(0, len(x), chunk):
        seg = x[start:start + chunk]
        f, t, Z = stft(seg, fs=SR, window="hann", nperseg=NPERSEG,
                       noverlap=NPERSEG - HOP, nfft=NPERSEG)
        mag = np.abs(Z)  # (frecuencias, fotogramas)
        band = (f >= FMIN) & (f <= FMAX)
        magb = mag[band]
        fb = f[band]
        total = magb.sum(axis=0) + 1e-12
        peak_i = magb.argmax(axis=0)
        peak_mag = magb[peak_i, np.arange(magb.shape[1])]
        ratio = peak_mag / total
        rms = np.sqrt((seg ** 2).mean())
        # energía por fotograma (aprox. con la magnitud total)
        frame_e = mag.sum(axis=0)
        thresh_e = np.percentile(frame_e, 90)
        is_beep = (ratio > 0.55) & (frame_e > thresh_e)
        # agrupar fotogramas seguidos
        i = 0
        n = len(is_beep)
        while i < n:
            if not is_beep[i]:
                i += 1
                continue
            j = i
            while j + 1 < n and is_beep[j + 1]:
                j += 1
            dur = (j - i + 1) * HOP / SR
            if dur >= 0.03:  # al menos 30 ms
                freqs = fb[peak_i[i:j + 1]]
                events.append({
                    "t": t0 + t[i],
                    "dur": dur,
                    "f_med": float(np.median(freqs)),
                    "f_ini": float(freqs[0]),
                    "f_fin": float(freqs[-1]),
                    "ratio": float(np.median(ratio[i:j + 1])),
                    "amp": float(np.median(peak_mag[i:j + 1])),
                })
            i = j + 1
        t0 += len(seg) / SR
        print(f"  {t0/60:.1f} min procesados, {len(events)} eventos",
              flush=True)
    # fusionar eventos pegados (<80 ms) con frecuencia parecida
    merged = []
    for ev in events:
        if merged and ev["t"] - (merged[-1]["t"] + merged[-1]["dur"]) < 0.08 \
                and abs(ev["f_med"] - merged[-1]["f_med"]) < 60:
            last = merged[-1]
            last["dur"] = ev["t"] + ev["dur"] - last["t"]
            last["f_fin"] = ev["f_fin"]
        else:
            merged.append(dict(ev))
    with open(out_csv, "w") as fh:
        fh.write("t,dur,f_med,f_ini,f_fin,ratio,amp\n")
        for ev in merged:
            fh.write(f"{ev['t']:.3f},{ev['dur']:.3f},{ev['f_med']:.0f},"
                     f"{ev['f_ini']:.0f},{ev['f_fin']:.0f},"
                     f"{ev['ratio']:.2f},{ev['amp']:.1f}\n")
    print(f"{len(merged)} eventos en {out_csv}")


if __name__ == "__main__":
    detect(sys.argv[1], sys.argv[2])
