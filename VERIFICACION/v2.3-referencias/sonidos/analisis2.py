#!/usr/bin/env python3
"""Detección de pitidos del juego por "novedad" espectral.

El directo lleva música de fondo (un loop en sol mayor) y la voz de
Vegetta encima, así que un pico tonal sin más no basta: se compara cada
fotograma de STFT con la mediana local (±2 s) en cada frecuencia. Un
pitido del juego es un salto brusco y concentrado en 1-2 bins (un tono
casi puro), mientras que la voz reparte la energía por muchos armónicos
y las notas de piano duran más y tienen armónicos.

Uso: python3 analisis2.py audio-16min.wav eventos2-16min.csv
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft

SR = 22050
NPERSEG = 2048
HOP = 256
FMIN, FMAX = 250, 5000


def detect(path, out_csv):
    sr, data = wavfile.read(path)
    assert sr == SR
    if data.ndim > 1:
        data = data[:, 0]
    x = data.astype(np.float32) / 32768.0
    chunk = SR * 300
    events = []
    base_t = 0.0
    for start in range(0, len(x), chunk):
        seg = x[start:start + chunk]
        f, t, Z = stft(seg, fs=SR, window="hann", nperseg=NPERSEG,
                       noverlap=NPERSEG - HOP, nfft=NPERSEG)
        mag = np.abs(Z)
        band = (f >= FMIN) & (f <= FMAX)
        magb = mag[band]
        fb = f[band]
        # fondo local: mediana en ±2 s (ventana de ~172 fotogramas)
        W = 172
        bg = np.empty_like(magb)
        n = magb.shape[1]
        for i in range(n):
            lo = max(0, i - W // 2)
            hi = min(n, i + W // 2)
            bg[:, i] = np.median(magb[:, lo:hi], axis=1)
        nov = magb / (bg + 1e-6)
        # candidato: pico de novedad alto y concentrado
        top = nov.argmax(axis=0)
        topv = nov[top, np.arange(n)]
        # segundo pico fuera de ±3 bins del primero
        nov2 = nov.copy()
        for i in range(n):
            lo = max(0, top[i] - 3)
            hi = min(nov.shape[0], top[i] + 4)
            nov2[lo:hi, i] = 0
        second = nov2.max(axis=0)
        conc = topv / (second + 1e-9)
        is_beep = (topv > 6) & (conc > 2.5) & (magb[top, np.arange(n)] > 0.15)
        i = 0
        while i < n:
            if not is_beep[i]:
                i += 1
                continue
            j = i
            while j + 1 < n and is_beep[j + 1]:
                j += 1
            dur = (j - i + 1) * HOP / SR
            if dur >= 0.03:
                freqs = fb[top[i:j + 1]]
                novs = topv[i:j + 1]
                events.append({
                    "t": base_t + t[i],
                    "dur": dur,
                    "f_med": float(np.average(freqs, weights=novs)),
                    "f_ini": float(freqs[0]),
                    "f_fin": float(freqs[-1]),
                    "nov": float(np.median(novs)),
                })
            i = j + 1
        base_t += len(seg) / SR
        print(f"  {base_t/60:.1f} min, {len(events)} eventos", flush=True)
    merged = []
    for ev in events:
        if merged and ev["t"] - (merged[-1]["t"] + merged[-1]["dur"]) < 0.08 \
                and abs(ev["f_med"] - merged[-1]["f_med"]) < 80:
            last = merged[-1]
            last["dur"] = ev["t"] + ev["dur"] - last["t"]
            last["f_fin"] = ev["f_fin"]
        else:
            merged.append(dict(ev))
    with open(out_csv, "w") as fh:
        fh.write("t,dur,f_med,f_ini,f_fin,nov\n")
        for ev in merged:
            fh.write(f"{ev['t']:.3f},{ev['dur']:.3f},{ev['f_med']:.0f},"
                     f"{ev['f_ini']:.0f},{ev['f_fin']:.0f},{ev['nov']:.1f}\n")
    print(f"{len(merged)} eventos en {out_csv}")


if __name__ == "__main__":
    detect(sys.argv[1], sys.argv[2])
