#!/usr/bin/env python3
"""Detección de tonos puros (pitidos del juego) en un audio largo.

Busca eventos tonales cortos y concentrados en 1-2 bins (como
analisis2.py) y luego busca dos patrones:
  a) cuenta atrás 3-2-1: 3 tonos separados ~0,9-1,1 s, frecuencia
     ascendente, seguidos poco después por el arpegio de inicio de turno.
  b) tic de los últimos 10 s: ~10 tonos iguales separados ~1 s justo
     antes de un cambio de turno (arpegio conocido).

Uso: python3 analisis3.py audio-2h.wav eventos3.csv
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft

SR = 22050
NPERSEG = 2048
HOP = 512
FMIN, FMAX = 300, 4000


def detect_events(path):
    sr, data = wavfile.read(path)
    assert sr == SR, sr
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
        med = np.median(magb, axis=0) + 1e-6
        top = magb.argmax(axis=0)
        topv = magb[top, np.arange(magb.shape[1])]
        prom = topv / med
        # concentración: energía del pico frente a la suma de la banda
        conc = topv / (magb.sum(axis=0) + 1e-9)
        is_tone = (topv > 0.006) & (prom > 8) & (conc > 0.04)
        i = 0
        n = magb.shape[1]
        while i < n:
            if not is_tone[i]:
                i += 1
                continue
            j = i
            while j + 1 < n and is_tone[j + 1]:
                j += 1
            dur = (j - i + 1) * HOP / SR
            if dur >= 0.04:
                freqs = fb[top[i:j + 1]]
                events.append({
                    "t": base_t + float(t[i]),
                    "dur": float(dur),
                    "f": float(np.median(freqs)),
                    "mag": float(np.max(topv[i:j + 1])),
                })
            i = j + 1
        base_t += len(seg) / SR
        print(f"  {base_t/60:.1f} min, {len(events)} eventos", flush=True)
    # fusionar eventos pegados (<0,08 s) con freq parecida
    merged = []
    for ev in events:
        if merged and ev["t"] - (merged[-1]["t"] + merged[-1]["dur"]) < 0.08 \
                and abs(ev["f"] - merged[-1]["f"]) < 60:
            last = merged[-1]
            last["dur"] = ev["t"] + ev["dur"] - last["t"]
        else:
            merged.append(dict(ev))
    return merged


def main():
    path, out = sys.argv[1], sys.argv[2]
    evs = detect_events(path)
    with open(out, "w") as fh:
        fh.write("t,dur,f,mag\n")
        for ev in evs:
            fh.write(f"{ev['t']:.3f},{ev['dur']:.3f},{ev['f']:.0f},{ev['mag']:.2f}\n")
    print(f"{len(evs)} eventos en {out}")

    # --- patrón b) tic antes de cada arpegio conocido ---
    arp = [660.3, 754.9, 796.9, 947.0, 982.3, 1132.8, 1172.3, 1322.8,
           1510.4, 1670.4, 1702.7, 1853.2, 1892.7, 2042.9, 2082.8, 2233.0]
    print("\n== TIC 10 s antes de cada arpegio ==")
    for T in arp:
        win = [e for e in evs if T - 12.5 <= e["t"] <= T - 0.3]
        # buscar rachas de eventos separados ~1 s con freq parecida
        seqs = []
        cur = [win[0]] if win else []
        for e in win[1:]:
            if cur and 0.7 <= e["t"] - cur[-1]["t"] <= 1.3 \
                    and abs(e["f"] - cur[-1]["f"]) < 120:
                cur.append(e)
            else:
                if len(cur) >= 3:
                    seqs.append(cur)
                cur = [e]
        if len(cur) >= 3:
            seqs.append(cur)
        for s in seqs:
            print(f"  arpegio {T}: {len(s)} tics "
                  f"{s[0]['t']:.1f}-{s[-1]['t']:.1f} "
                  f"f={np.median([e['f'] for e in s]):.0f} Hz "
                  f"dur~{np.median([e['dur'] for e in s]):.2f}s")

    # --- patrón a) cuenta atrás: 3 tonos ascendentes ~1 s ---
    print("\n== CANDIDATOS CUENTA ATRÁS (3 tonos ascendentes ~1 s) ==")
    for i in range(len(evs) - 2):
        a, b, c = evs[i], evs[i + 1], evs[i + 2]
        if 0.7 <= b["t"] - a["t"] <= 1.3 and 0.7 <= c["t"] - b["t"] <= 1.3 \
                and b["f"] > a["f"] + 40 and c["f"] > b["f"] + 40 \
                and a["dur"] < 0.6 and b["dur"] < 0.6 and c["dur"] < 0.6:
            print(f"  {a['t']:.1f}s: {a['f']:.0f} -> {b['f']:.0f} -> "
                  f"{c['f']:.0f} Hz  (dur {a['dur']:.2f}/{b['dur']:.2f}/{c['dur']:.2f}s)")


if __name__ == "__main__":
    main()
