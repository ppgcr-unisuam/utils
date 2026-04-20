'''
ppgcr_utils.cop
Modulo com funcoes para o processamento de sinais de posicao de centro de pressao
Desenvolvido e mantido pelos colaboradores do programa de ciencias da reabilitacao - Unisuam
'''

import numpy as np
from scipy import stats, signal

## frequência média, em Hertz
def computar_freqs(sinal1d,freq_aq=1000,method='fft',show=True):
    """
    Calcula o espectro de potência e a frequência média de um sinal 1D.

    A frequência média é definida como a média ponderada das frequências
    pelo espectro de potência (PSD).

    Parâmetros
    ----------
    sinal1d : array-like
        Sinal unidimensional (ex.: série temporal de EMG ou COP).
    freq_aq : float, opcional (default=1000)
        Frequência de amostragem do sinal em Hz.
    method : {'fft', 'welch', 'legado'}, opcional (default='fft')
        Método utilizado para estimar o espectro de potência:
        - 'fft'    : FFT direta com PSD one-sided
        - 'welch'  : método de Welch (mais robusto a ruído)
        - 'legado' : implementação anterior (mantida para compatibilidade)
    show : bool, opcional
        Parâmetro reservado (não utilizado atualmente).

    Retorna
    -------
    f : ndarray
        Vetor de frequências (Hz).
    psd : ndarray
        Densidade espectral de potência associada a cada frequência.
    frequencia_media : float
        Frequência média do sinal (Hz), ponderada pela PSD.

    Notas
    -----
    - O sinal é centralizado (remoção da média) antes da análise.
    - A PSD é calculada apenas para frequências positivas (one-sided).
    - A frequência média pode ser sensível a ruído de alta frequência,
      especialmente quando calculada via FFT direta.

    Exemplos
    --------
    >>> f, psd, f_mean = computar_freqs(sinal, freq_aq=1000, method='welch')
    """
    
    y = sinal1d - np.mean(sinal1d)
    N = len(y)

    if method == 'legado':
        yf = np.fft.fft(y) # splicar a transformada de Fourier
        xf = np.fft.fftfreq(N, 1 / freq_aq)[:N // 2]  # frequências positivas
        spectra = np.abs(yf[:N // 2])**2  # espectro de potência
        frequencia_media = np.sum(xf * spectra) / np.sum(spectra) # ponderada pelo espectro de potência
        f = xf
        psd = spectra
    if method == 'fft':
        yf = np.fft.fft(y)                               # FFT (two-sided)
        f = np.fft.fftfreq(N, d=1/freq_aq)[:N // 2]      # frequências positivas (0 ... < fs/2)
        # PSD one-sided em cm^2/Hz
        psd = (1 / (freq_aq * N)) * (np.abs(yf[:N // 2])**2)
        # correção one-sided: dobra tudo
        psd *= 2
        frequencia_media = np.sum(f * psd) / np.sum(psd)
    elif method == 'welch':
        f, psd = signal.welch(y, fs=freq_aq,nperseg=1024)
        frequencia_media = (f * psd).sum() / psd.sum()
    return f,psd,frequencia_media


# computa area da elipese
def computar_area_elipse_cop(ml, ap, p=0.95):
    """
    Calcula a elipse de confiança do centro de pressão (COP) e sua área.

    A elipse é baseada na distribuição bivariada dos dados nos eixos
    médio-lateral (ML) e ântero-posterior (AP), assumindo normalidade.

    Parâmetros
    ----------
    ml : array-like
        Sinal do COP no eixo médio-lateral (cm).
    ap : array-like
        Sinal do COP no eixo ântero-posterior (cm).
    p : float, opcional (default=0.95)
        Nível de confiança da elipse (ex.: 0.95 para 95%).

    Retorna
    -------
    a : float
        Semi-eixo maior da elipse (cm).
    b : float
        Semi-eixo menor da elipse (cm).
    cov : ndarray, shape (2, 2)
        Matriz de covariância dos dados (cm²).
    area : float
        Área da elipse de confiança (cm²).

    Notas
    -----
    - Os sinais são centralizados antes do cálculo (remoção da média).
    - A elipse é baseada na distribuição qui-quadrado com 2 graus de liberdade.
    - A área é dada por: π * a * b.
    - A interpretação depende da suposição de distribuição aproximadamente normal.

    Exemplos
    --------
    >>> a, b, cov, area = computar_area_elipse_cop(ml, ap, p=0.95)
    """

    # remove DC (média)
    ml = ml - ml.mean()
    ap = ap - ap.mean()
    X = np.column_stack([ml, ap])
    cov = np.cov(X, rowvar=False, ddof=1)  # cm²
    # autovalores (ordenados do maior para o menor)
    evals = np.linalg.eigvalsh(cov)[::-1]
    evals = np.maximum(evals, 0)  # segurança numérica
    k = stats.chi2.ppf(p, df=2)
    a = np.sqrt(k * evals[0])  # cm
    b = np.sqrt(k * evals[1])  # cm
    area = np.pi * a * b       # cm²
    return a,b,cov,area