import numpy as np
from scipy import stats





# computa area da elipese
def computar_area_elipse_cop(ml, ap, p=0.95):
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