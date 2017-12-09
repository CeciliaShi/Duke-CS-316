import plotly.plotly as py
import plotly.graph_objs as go 

def plot_victim_frequency(res):
    data = [go.Bar(
        y = [v[1] for v in res],
        x = [v[0] for v in res],
        name="Victim Type",
        marker=dict(color='rgb(49,130,189)'),
        orientation="h"
    )]

    layout = go.Layout(
        title = "Number of Terrorist Attacks by Victim Types",
        autosize=False,
        width=1000,
        height=600,
        margin=go.Margin(l=200, r=50, b=100, t=100, pad=4),
        barmode='group',)

    fig = go.Figure(data=data, layout=layout)
    p1 = py.plot(fig, filename='victim_type', auto_open=False)
    return p1

def plot_victim_fatality(res):
    nkill = go.Bar(
    y=[v[0] for v in res],
    x=[v[1] for v in res],
        name='fatality',
        marker=dict(color='rgb(49,130,189)',),
        orientation="h"
        )
    nwound = go.Bar(y=[v[0] for v in res],x=[v[2] for v in res],
        name='injury',
        marker=dict(color='rgb(204,204,204)',), 
        orientation="h"
        )

    data = [nkill, nwound]
    layout = go.Layout(title = "Fatalities and Injuries by Victim Type",
        autosize=False,
        width=1000,
        height=600,
        margin=go.Margin(l=200, r=50, b=100, t=100, pad=4),
        barmode='stack'
        )
    fig = go.Figure(data=data, layout=layout)
    p1=py.plot(fig, filename='victim_damage', auto_open=False)
    return(p1)

def plot_victim_subtype(res):
    nkill = go.Pie(
        labels = [v[0] for v in res],
        values = [v[1] for v in res],
        domain = {"x": [0, .48]},
        name = "fatality",
        hoverinfo = "label+percent+name",
        hole = .4,
        type = "pie",
        textinfo = 'none'    
        )
    nwound = go.Pie(
        labels = [v[0] for v in res],
        values = [v[2] for v in res],
        textposition ="inside",
        domain = {"x": [.52, 1]},
        name = "injury",
        hoverinfo="label+percent+name",
        hole= .4,
        type= "pie",
        textinfo='none'
        )
    data = [nkill, nwound]
    layout = go.Layout(
        legend = dict(font=dict(size=10)),
        showlegend=False,
        title="Fatalities and Injuries by Victim Subtypes",
        annotations= [
        dict(
            font= dict(
                size= 15
                ),
            showarrow= False,
            text= "Fatalities",
            x= 0.195,
            y= 0.5
            ),
        dict(
            font= dict(
                size= 15
                ),
            showarrow= False,
            text= "Injuries",
            x= 0.805,
            y= 0.5
            )
        ]
        )
    fig = go.Figure(data=data, layout=layout)
    p1 = py.plot(fig, filename='victim_subtype', auto_open=False)
    return(p1)
