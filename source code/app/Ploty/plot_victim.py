from models import Targeted
from models import db
from sqlalchemy import func
import plotly.plotly as py
import plotly.graph_objs as go 

#python -c "import plotly; plotly.tools.set_credentials_file(username='KimJin', api_key='kgTp9k4kEV7XfpUolr60')"

victim_type = db.session.query(func.count(Targeted.incident_id).label('count'), Targeted.victim_type).group_by(Targeted.victim_type).order_by(func.count(Targeted.incident_id)).all()

def plot_victim(res):
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