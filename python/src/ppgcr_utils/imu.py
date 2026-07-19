'''
ppgcr_utils.imu
Modulo com funcoes para o processamento de sinais de sensores e centrais inerciais
Desenvolvido e mantido pelos colaboradores do programa de ciencias da reabilitacao - Unisuam
'''

import numpy as np

def calcular_freeacc(x, y, z, matriz_rotacao, g=9.80665):
    """
    Converte a aceleração nos eixos do sensor para aceleração livre
    no sistema global ENU: East, North e Up.

    Parâmetros
    ----------
    x, y, z : float
        Acelerações medidas pelo sensor, em m/s².

    matriz_rotacao : array 3x3
        Matriz que transforma vetores do sistema do sensor
        para o sistema global ENU.

    g : float
        Aceleração da gravidade, em m/s².

    Retorna
    -------
    freeacc_e, freeacc_n, freeacc_u : float
        Aceleração livre nos eixos East, North e Up.
    """

    # Aceleração medida nos eixos do sensor
    acc_sensor = np.array([x, y, z])

    # Rotaciona a aceleração para o sistema global ENU
    acc_enu = matriz_rotacao @ acc_sensor

    # Remove a gravidade, que atua no eixo Up
    gravidade = np.array([0, 0, g])

    freeacc = acc_enu - gravidade

    return freeacc[0], freeacc[1], freeacc[2]