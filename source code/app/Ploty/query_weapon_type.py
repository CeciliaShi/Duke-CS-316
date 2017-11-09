from models import *
from sqlalchemy import func
import plotly.plotly as py
import plotly.graph_objs as go 
import pandas as pd
import plotly

plotly.tools.set_credentials_file(username='xiaozhou0614', api_key='nKS0ddIHYYjKmMf5AnRw')

weapon_type = (db.session.query(func.count(Used.incident_id).label('count'), Used.weapon_type).
    group_by(Used.weapon_type).
    order_by(func.count(Used.incident_id).desc()).
    all())
weapon_type = pd.DataFrame(weapon_type)

def weapon(df):
    weapon = go.Bar(
        y=df['weapon_type'].tolist(),
        x=df['count'].tolist(),
        #text=df['weapon_type'].tolist(),
        textposition = 'auto',
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5),
            ),
        opacity=0.8,
        orientation = 'h')
    data = [weapon]
    layout = go.Layout(title='Weapon Type Frequency',
        margin=go.Margin(l=200, r=50, b=100, t=100, pad=4),
        barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    p1 = py.plot(fig, filename='weapon_type', auto_open=False)
    return p1