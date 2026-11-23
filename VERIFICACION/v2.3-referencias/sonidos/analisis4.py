#!/usr/bin/env python3
"""Detección genérica de sonidos del juego en un audio de gameplay.

1. Detecta eventos tonales (como analisis3.py).
2. Busca el arpegio de cambio de turno: 3 tonos ~784, ~880, ~1174 Hz
   en menos de 0,5 s (firma medida en Vegetta).
3. Para cada arpegio, busca el tic de los últimos 10 s: tonos repetidos
   ~1 s antes del arpegio.
4. Busca candidatos de cuenta atrás 3-2-1 en todo el audio.
5. Lista los huecos de silencio >= 2 s (donde podría esconderse una
   cuenta atrás limpia).

Uso: python3 analisis4.py audio.wav eventos4.csv
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
    merged = []
    for ev in events:
        if merged and ev["t"] - (merged[-1]["t"] + merged[-1]["dur"]) < 0.08 \
                and abs(ev["f"] - merged[-1]["f"]) < 60:
            last = merged[-1]
            last["dur"] = ev["t"] + ev["dur"] - last["t"]
        else:
            merged.append(dict(ev))
    return merged, x


def main():
    path, out = sys.argv[1], sys.argv[2]
    evs, x = detect_events(path)
    with open(out, "w") as fh:
        fh.write("t,dur,f,mag\n")
        for ev in evs:
            fh.write(f"{ev['t']:.3f},{ev['dur']:.3f},{ev['f']:.0f},{ev['mag']:.2f}\n")
    print(f"{len(evs)} eventos en {out} (duración {len(x)/SR/60:.1f} min)")

    # --- 2. arpegios de cambio de turno ---
    arp = []
    for i in range(len(evs) - 2):
        a, b, c = evs[i], evs[i + 1], evs[i + 2]
        if c["t"] - a["t"] <= 0.6 and abs(a["f"] - 784) < 70 \
                and abs(b["f"] - 880) < 70 and abs(c["f"] - 1174) < 80:
            arp.append(a["t"])
    # quitar duplicados cercanos
    arp2 = []
    for t in arp:
        if not arp2 or t - arp2[-1] > 2:
            arp2.append(t)
    print(f"\n== ARPEGIOS de cambio de turno: {len(arp2)} ==")
    print("  " + ", ".join(f"{t:.1f}" for t in arp2))

    # --- 3. tic antes de cada arpegio ---
    print("\n== TIC 12 s antes de cada arpegio ==")
    found = 0
    for T in arp2:
        win = [e for e in evs if T - 12.5 <= e["t"] <= T - 0.3]
        seqs = []
        cur = [win[0]] if win else []
        for e in win[1:]:
            if cur and 0.7 <= e["t"] - cur[-1]["t"] <= 1.3 \
                    and abs(e["f"] - cur[-1]["f"]) < 120:
                cur.append(e)
            else:
                if len(cur) >= 4:
                    seqs.append(cur)
                cur = [e]
        if len(cur) >= 4:
            seqs.append(cur)
        for s in seqs:
            found += 1
            print(f"  arpegio {T:.1f}: {len(s)} tics "
                  f"{s[0]['t']:.1f}-{s[-1]['t']:.1f} "
                  f"f={np.median([e['f'] for e in s]):.0f} Hz "
                  f"dur~{np.median([e['dur'] for e in s]):.2f}s "
                  f"mag~{np.median([e['mag'] for e in s]):.3f}")
    if not found:
        print("  ninguno con >=4 tics iguales a ~1 s")

    # --- 4. cuenta atrás: 3 tonos ascendentes ~1 s ---
    print("\n== CANDIDATOS CUENTA ATRÁS (3 tonos ascendentes ~1 s) ==")
    n = 0
    for i in range(len(evs) - 2):
        a, b, c = evs[i], evs[i + 1], evs[i + 2]
        if 0.7 <= b["t"] - a["t"] <= 1.3 and 0.7 <= c["t"] - b["t"] <= 1.3 \
                and b["f"] > a["f"] + 40 and c["f"] > b["f"] + 40 \
                and a["dur"] < 0.6 and b["dur"] < 0.6 and c["dur"] < 0.6:
            n += 1
            print(f"  {a['t']:.1f}s: {a['f']:.0f} -> {b['f']:.0f} -> "
                  f"{c['f']:.0f} Hz (dur {a['dur']:.2f}/{b['dur']:.2f}/{c['dur']:.2f}s)")
    if not n:
        print("  ninguno")

    # --- 5. huecos de silencio >= 2 s (RMS por 100 ms < 0.005) ---
    print("\n== HUECOS DE SILENCIO >= 2 s ==")
    hop = int(SR * 0.1)
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2))
                    for i in range(0, len(x) - hop, hop)])
    quiet = rms < 0.004
    i = 0
    gaps = []
    while i < len(quiet):
        if not quiet[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(quiet) and quiet[j + 1]:
            j += 1
        dur = (j - i + 1) * 0.1
        if dur >= 2.0:
            gaps.append((i * 0.1, dur))
        i = j + 1
    print(f"  {len(gaps)} huecos: " +
          ", ".join(f"{t:.0f}s ({d:.1f}s)" for t, d in gaps[:25]))


if __name__ == "__main__":
    main()
