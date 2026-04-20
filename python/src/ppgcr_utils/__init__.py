"""
Pacote com utilitarios para processamento e analise de dados e sinais. Desenvolvido pelos colaboradores do programa de pos graduação em ciencias da reabilitação da UNISUAM
Uso recomendado

>>> import ppgcr_utils as cru 

"""

from .cop import computar_area_elipse_cop, computar_freqs
from .emg import filt_emg
from .plotting import stat_diff

__version__ = "0.1.0"
