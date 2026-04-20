# ppgcr-utils

Repositorio com implementação de modulos utilitarios para processamento e analise de dados e sinais. Desenvolvido pelos colaboradores do programa de pos graduação em ciencias da reabilitação da UNISUAM

| Função           | Python      | R       | Matlab      |
|------------------|-------------|---------|-------------|
| computar_freqs   | ✅         |          |            |
| computar_area_elipse_cop | ✅ |          |            |
| filt_em          | ✅         |          |            |
| stat_diff        |   ✅       |          |            |


# Python

## Instalação local
O pacote não esta disponivel no pipy. Instale localmente usando o modo editavel do pip. Para usuarios do anaconda, segue instalação no ambiente base. Outros ambientes virtuais seguem a mesma logica.
```bash
C:\Users\voce\anaconda3\shell\condabin\conda-hook.ps1
conda activate base
cd ./python/src
pip install -e .
```

## Example

```python
import ppgcr_utils as cru
```
