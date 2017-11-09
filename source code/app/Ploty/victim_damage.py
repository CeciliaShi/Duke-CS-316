from models import Targeted
from models import Incident
from models import db
from sqlalchemy import func
import plotly.plotly as py
import plotly.graph_objs as go 
import plotly

#plotly.tools.set_credentials_file(username='xiaozhou0614', api_key='nKS0ddIHYYjKmMf5AnRw')

base_query = (db.session.query(Targeted.victim_type, func.sum(Incident.nkill).label('fatality'), func.sum(Incident.nwound).label('injury'))
	.join(Targeted.incident)
	.group_by(Targeted.victim_type)
	.order_by(func.sum(Incident.nkill))
	).all()

def victim_damage(res):
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
    layout = go.Layout(title = "Fatality and Injury by Victim Type",
        autosize=False,
        width=1000,
        height=600,
        margin=go.Margin(l=200, r=50, b=100, t=100, pad=4),
        barmode='stack'
        )
    fig = go.Figure(data=data, layout=layout)
    p1=py.plot(fig, filename='victim_damage', auto_open=False)
    return(p1)



