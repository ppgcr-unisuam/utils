import numpy as np
from scipy import signal

# Filtro do Mello, Oliveira e Nadal (10.1016/j.cmpb.2007.04.004)
def filt_emg(emg_signal, sf=1000):
    # garante o formato
    x = np.asarray(emg_signal, dtype=float)
    # define nyquesima
    nyq = 0.5 * sf
    # lista com os parametros sos dos filtros a serem agrupados
    sos_stages = []
    # passa banda (20–450 Hz)
    bp_low, bp_high = 20.0, 450.0
    sos_bp = signal.butter(N=4, Wn=[bp_low/nyq, bp_high/nyq], btype='bandpass', output='sos')
    sos_stages.append(sos_bp)
    # notchs de 60
    f0 = 60.0
    Q = 35.0
    max_harm = int(np.floor(nyq // f0))  # limita às harmônicas viáveis
    for k in range(1, max_harm + 1):
        fk = f0 * k
        # Evita notch muito próximo do DC ou de Nyquist
        if 5.0 < fk < nyq * 0.98:
            # iirnotch retorna (b,a); pedimos diretamente SOS via butter? Não: convertemos via zpk
            b, a = signal.iirnotch(w0=fk, Q=Q, fs=sf)
            # Converte (b,a) em SOS - revisar quando der
            sos_notch = np.array([[b[0], b[1], b[2], 1.0, a[1], a[2]]], dtype=float)
            sos_stages.append(sos_notch)

    # aplica cascata (bandpass + notches) bidirecionalmente
    sos = np.vstack(sos_stages)
    filtered = signal.sosfiltfilt(sos, x)

    return filtered
