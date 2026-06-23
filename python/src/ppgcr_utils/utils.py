'''
ppgcr_utils.utils
Modulo com funcoes utilitarias para tarefas diversas
Desenvolvido e mantido pelos colaboradores do programa de ciencias da reabilitacao - Unisuam
'''

import pandas as pd
from scipy import stats

def resumo(x, numeric_summary='auto', digits=1):
    
    def resumo_series(s):
        s = s.dropna()
        nome = s.name
        n = len(s)
        unicos = s.nunique()
        
        if unicos <= 2:
            cont = s.value_counts()
            mais_freq = cont.index[0]
            value = f"{cont.iloc[0]} ({100*cont.iloc[0]/n:.{digits}f}%)"
            return pd.DataFrame(
                {'value': [value]},
                index=[f"{nome}({mais_freq})"]
            )
        
        if not pd.api.types.is_numeric_dtype(s):
            cont = s.value_counts()
            valores = [''] + [
                f"{cont.loc[i]} ({100*cont.loc[i]/n:.{digits}f}%)"
                for i in cont.index
            ]
            return pd.DataFrame(
                {'value': valores},
                index=[nome] + list(cont.index)
            )
        
        if numeric_summary == 'auto':
            p = stats.shapiro(s).pvalue
            metodo = 'mean' if p > 0.05 else 'iqr'
        else:
            metodo = numeric_summary
        
        if metodo == 'mean':
            value = f"{s.mean():.{digits}f}±{s.std():.{digits}f}"
        elif metodo == 'iqr':
            value = (
                f"{s.quantile(.50):.{digits}f} "
                f"[{s.quantile(.25):.{digits}f}; {s.quantile(.75):.{digits}f}]"
            )
        
        return pd.DataFrame({'value': [value]}, index=[nome])
    
    if isinstance(x, pd.Series):
        return resumo_series(x)
    
    return pd.concat([resumo_series(x[col]) for col in x.columns])