import plotly.graph_objs as go
import plotly.plotly as py

def weapon(df):
    
    trace1 = go.Bar(
    x=df['weapon_type'].tolist(),
    y=df['count'].tolist(),
    name='Frequency',
    marker = dict(color = '#1883B2',),
    opacity = 0.8
    )
        
    trace2 = go.Bar(
    x=df['weapon_type'].tolist(),
    y=df['fatality'].tolist(),
    name='Fatalities and Injuries',
    marker = dict(color = '#A4E3FF',),
    opacity = 0.8
    )
    
    data = [trace2,trace1]
    layout = go.Layout(
            xaxis = dict(tickangle = 45),
            title = 'Frequency/Fatalities and Injuries by Weapon Type',
            barmode='group',)
    
    fig = go.Figure(data=data, layout=layout)
    p1 = py.plot(fig, filename='weapon_type', auto_open=False)
    return p1
