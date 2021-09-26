import streamlit as st
import plotly.graph_objects as go

def newton( f, df, x, tol = 1.0e-6, return_niter = False, return_seq = False ):
    
    stop = False
    
    k = 0
    
    if return_seq:
        seq = [ x ]
    
    while not stop:
        
        x_prev = x
        x = x - f( x ) / df( x )

        if return_seq:
            seq.append( x )
        
        stop = ( abs( x - x_prev ) <= tol )
        
        k = k + 1
        
    if return_seq:
        return seq
    elif return_niter:
        return ( x, k )
    else:
        return x

def NewtonPage():
    st.write("XD")

    fig = go.Figure(
    data=[go.Scatter(x=[0, 1], y=[0, 1])],
    layout=go.Layout(
        xaxis=dict(range=[0, 5], autorange=False),
        yaxis=dict(range=[0, 5], autorange=False),
        title="Start Title",
        updatemenus=[dict(
            type="buttons",
            bgcolor="#ce4212",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])
            ],
    ),
    frames=[go.Frame(data=[go.Scatter(x=[1, 2], y=[1, 2])]),
            go.Frame(data=[go.Scatter(x=[1, 4], y=[1, 4])]),
            go.Frame(data=[go.Scatter(x=[3, 4], y=[3, 4])],
                     layout=go.Layout(title_text="End Title"))])
    
    st.plotly_chart(fig)
    return