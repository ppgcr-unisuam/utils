'''
ppgcr_utils.emg
Modulo com funcoes para o processamento de sinais de eletromiografia de superficie
Desenvolvido e mantido pelos colaboradores do programa de ciencias da reabilitacao - Unisuam
'''

import numpy as np
from scipy import signal

# Filtro do Mello, Oliveira e Nadal (10.1016/j.cmpb.2007.04.004)
def filt_emg(emg_signal, sf=1000):
    """
    Filtra um sinal de EMG com passa-banda e filtros notch nas harmônicas de 60 Hz, de acordo com o procedimento proposto
    pelos colegas em "Digital Butterworth filter for subtracting noise from low magnitude surface electromyogram" (10.1016/j.cmpb.2007.04.004)

    O processamento aplica:
    - filtro passa-banda de 20 a 450 Hz;
    - filtros notch em 60 Hz e em suas harmônicas viáveis até abaixo da
      frequência de Nyquist;
    - filtragem bidirecional (`sosfiltfilt`) para evitar defasagem temporal.

    Parâmetros
    ----------
    emg_signal : array-like
        Sinal de EMG em uma dimensão.
    sf : float, opcional (default=1000)
        Frequência de amostragem do sinal em Hz.

    Retorna
    -------
    filtered : ndarray
        Sinal filtrado com o mesmo comprimento do sinal de entrada.

    Notas
    -----
    - O filtro passa-banda é de 4ª ordem, com faixa de 20 a 450 Hz.
    - Os filtros notch são aplicados em 60 Hz e em suas harmônicas
      admissíveis abaixo de Nyquist.
    - A filtragem é realizada em formato SOS (second-order sections),
      com aplicação bidirecional para minimizar distorções de fase.
    - O sinal de entrada é convertido para `numpy.ndarray` com tipo `float`.

    Exemplos
    --------
    >>> emg_filtrado = filt_emg(emg_bruto, sf=2000)
    """

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
