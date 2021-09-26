import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import math
import plotly.graph_objects as go
from numpy.polynomial import Polynomial

""" Function that returns the position of x0 that minimizes the distance from the x axis and the function """
def min_dist( f, df, x0, tol = 1.0e-6 ):

    stop = False
    counter = 0
    while not stop:
        
        x_pre = x0
        x0 = -f( x0 ) * df( x0 )
        
        stop = ( abs( x0 - x_pre ) <= tol )
        counter = counter + 1

        if(counter > 10**4):
            counter = "Não foi possivel calcular"
            x0 = -100000
            break

    return [x0, counter]
        
def PolynomialFunction(deg):
    deg = deg + 1
    val = [None for i in range(deg)]

    polynomial_function = "f(x)="
    cont = "+"
    for i in range(deg):
        val[i] = st.slider(f'Coeficiente {i+1}', min_value=0, max_value=10, key=f"degree_{i}", value = 1)

        if i == (deg-1):
            cont = ""

        if i == 0:
            polynomial_function =  polynomial_function + f"{val[i]}"+ cont

        if i == 1 and val[i] !=0:
            if val[i] == 1:
                polynomial_function = polynomial_function + f"x"+cont
            else:
                polynomial_function = polynomial_function + f"{val[i]}x"+cont

        if val[i] != 0 and i!=0 and i!=1 :
            if val[i] == 1:
                polynomial_function =  polynomial_function + f"x^{i}"+ cont
            else:
                polynomial_function =  polynomial_function + f"{val[i]}x^{i}"+ cont
            

    st.latex(polynomial_function)
    
    return val

def ExponencialFunction(alpha):

    beta_top = "{ x }"

    if alpha == 1:
        expofunction = f"\\alpha e^{beta_top}"
    else:
        expofunction = f"{alpha}e^{beta_top}"

    st.latex(expofunction)

    return
""" Formula Page """
def FormulaPage():
    st.header("Distancia Mínima")

    my_expander = st.expander("Configurações iniciais")

    with my_expander:
        col1, col2 = st.columns(2)
        x_0 = col1.number_input("Selecione o ponto inicial", key="inicial_point", value=1.0)
        fillcolor = col2.color_picker("Selecione a cor da distância", value="#E81111")
        graphselect = st.radio('Qual tipo de gráfico?', ["Polinomio","Exponencial"], key="graph_select")
        if graphselect == 'Polinomio':
            st.write("Polinomio")
            deg = st.number_input("Selecione o grau do polinomio", value = 0)
            val = PolynomialFunction(deg)

            f = Polynomial(val)
            df = f.deriv(1)
        if graphselect == "Exponencial":
            alpha = st.number_input("Selecione o alpha", value = 1)

            def f(x):
                return alpha*np.exp(x)

            df = f

            ExponencialFunction(alpha)

    dist, counter = min_dist( f  , df , x_0 )

    """ Gera o gráfico """
    x = np.arange(-2,2,0.01)
    y = f(x)

    dataframe = pd.DataFrame(dict(x=x,y=y))
    fig = px.line(dataframe,x='x',y='y')

    if dist != -100000:
        fig.add_shape(type="line", x0=dist, y0=0, x1 = dist, y1=f(dist),
            line=dict(
            color=fillcolor,
            width=4,
        ))

    st.plotly_chart(fig)

    if dist == -100000:
        st.write("Não Foi possivel encontrar resultados")
    else:
        col1, col2 = st.columns(2)
        col1.write(f"Posição do Eixo X: {dist}")
        col2.write(f"Número de iterações: {counter}")


    return
