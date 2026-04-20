'''
ppgcr_utils.ploting
Modulo com funcoes para auxiliar a elaboração de graficos
Desenvolvido e mantido pelos colaboradores do programa de ciencias da reabilitacao - Unisuam
'''

import matplotlib.pyplot as plt

def stat_diff( p0, p1, lh, t='*',fontsize=8,tcolor='grey',lcolor='gray',alpha=1,ax=None,fig=None):
    """
    Adiciona uma anotação gráfica de diferença estatística entre dois pontos.

    A função desenha uma marcação em forma de colchete/ligação entre dois
    pontos de um gráfico e posiciona um texto indicativo (por exemplo: '*',
    '**', 'p < 0.05') em uma altura definida pelo usuário.

    Parâmetros
    ----------
    p0 : tuple
        Coordenadas do primeiro ponto no formato (x, y).
    p1 : tuple
        Coordenadas do segundo ponto no formato (x, y).
    lh : float
        Altura em que o texto e a linha de anotação serão posicionados.
    t : str, opcional (default='*')
        Texto a ser exibido na anotação.
    fontsize : float, opcional (default=8)
        Tamanho da fonte do texto.
    tcolor : str, opcional (default='grey')
        Cor do texto da anotação.
    lcolor : str, opcional (default='gray')
        Cor da linha de anotação.
    alpha : float, opcional (default=1)
        Transparência da anotação.
    ax : matplotlib.axes.Axes, opcional
        Eixo no qual a anotação será desenhada. Se não for informado,
        a função tenta usar o primeiro eixo de `fig` ou o estado atual
        do Matplotlib.
    fig : matplotlib.figure.Figure, opcional
        Figura da qual será obtido o primeiro eixo, caso `ax` não seja informado.

    Retorna
    -------
    None
        A função adiciona a anotação diretamente ao gráfico.

    Notas
    -----
    - Se `ax` e `fig` forem omitidos, a função utiliza a interface implícita
      do `matplotlib.pyplot`.
    - Se `fig` for informado e `ax` for `None`, será usado `fig.axes[0]`.
    - A função desenha duas anotações para formar a ligação entre os pontos.
    - O usuário deve garantir que `lh` seja compatível com a escala do eixo y.

    Exemplos
    --------
    >>> stat_diff((1, 10), (2, 12), lh=14, t='*')
    >>> stat_diff((0, 5), (1, 5.5), lh=6, t='p < 0.05', ax=ax)
    """

    # extract coords
    (x0,y0) = p0
    (x1,y1) = p1
    # def line properties
    arrow_dic={'arrowstyle':"-",'connectionstyle':"angle,angleA=0,angleB=90,rad=10",'color':lcolor}
    #check if none of ax nor fig are given
    if ax==None and fig==None:
        # proceed to non-OOP approach
        # plot the left line and text
        plt.annotate(xy=(x0,y0),text=t,ha='center',xytext=((x0+x1)/2,lh),fontsize=fontsize, arrowprops=arrow_dic,color=tcolor,alpha=alpha)
        # plot the right line and a alpha-zero text
        plt.annotate(xy=(x1,y1),text=t,ha='center',xytext=((x0+x1)/2,lh),fontsize=fontsize, arrowprops=arrow_dic,color=tcolor,alpha=alpha)
    # if fig or ax is given
    else:
        # defines actual axis
        if ax == None: ax = fig.axes[0]
        # plot the lines and texts 
        # plot the left line and text
        ax.annotate(xy=(x0,y0),text=t,ha='center',xytext=((x0+x1)/2,lh),fontsize=fontsize, arrowprops=arrow_dic,color=tcolor,alpha=alpha)
        # plot the right line and a alpha-zero text
        ax.annotate(xy=(x1,y1),text=t,ha='center',xytext=((x0+x1)/2,lh),fontsize=fontsize, arrowprops=arrow_dic,color=tcolor,alpha=alpha)