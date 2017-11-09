from models import Targeted
from models import Incident
from models import db
from sqlalchemy import func
import plotly.plotly as py
import plotly.graph_objs as go 

query_subtype = (db.session.query(Targeted.subtype, func.sum(Incident.nkill), func.sum(Incident.nwound))
    .filter(Targeted.victim_type=="Private Citizens & Property")
    .join(Targeted.incident)
    .group_by(Targeted.subtype)
    ).all()

def victim_subtype(res):
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
        name = "fatality",
        hoverinfo="label+percent+name",
        hole= .4,
        type= "pie",
        textinfo='none'
        )
    data = [nkill, nwound]
    layout = go.Layout(
        legend = dict(font=dict(size=10)),
        title="Subtypes within Private Citizens & Property",
        annotations= [
        dict(
            font= dict(
                size= 15
                ),
            showarrow= False,
            text= "fatality",
            x= 0.195,
            y= 0.5
            ),
        dict(
            font= dict(
                size= 15
                ),
            showarrow= False,
            text= "injury",
            x= 0.805,
            y= 0.5
            )
        ]
        )
    fig = go.Figure(data=data, layout=layout)
    p1 = py.plot(fig, filename='victim_subtype', auto_open=False)
    return(p1)
