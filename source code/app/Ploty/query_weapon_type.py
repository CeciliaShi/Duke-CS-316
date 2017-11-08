
#! python -c "import plotly; plotly.tools.set_credentials_file(username='xiaozhou0614', api_key='nKS0ddIHYYjKmMf5AnRw')"

from models import *
from sqlalchemy import func
import plotly.plotly as py
import plotly.graph_objs as go 
import pandas as pd

weapon_type = db.session.query(func.count(Used.incident_id).label('count'), Used.weapon_type).group_by(Used.weapon_type).order_by(func.count(Used.incident_id).desc()).all()

def weapon(df):
    df=pd.DataFrame(df)
    x = df['weapon_type'].tolist()
    y = df['count'].tolist()
    data = [go.Bar(
            x=y,
            y=x,
            text=y,
            textposition = 'auto',
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5),
            ),
            opacity=0.6,
            orientation = 'h')]
    
    layout = go.Layout(title='Weapon Type Frequency')
    fig = go.Figure(data=data, layout=layout)
    p1 = py.plot(fig, filename='weapon_type', auto_open=False)
    return p1
