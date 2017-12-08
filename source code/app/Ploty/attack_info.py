from models import Incident
from models import BelongedTo
from models import db
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

#plotly.tools.set_credentials_file(username='Xingyu', api_key='xcgDva8EbQkqviNhVXYS')

#python -c "import plotly; plotly.tools.set_credentials_file(username='KimJin', api_key='kgTp9k4kEV7XfpUolr60')"



#attack_type = (db.session.query(Incident.international,Incident.property_damage, BelongedTo.suicide_attack, BelongedTo.succussful_attack).
#               join(BelongedTo, Incident.id == BelongedTo.incident_id).all()) 
#
#attack_type =  pd.DataFrame(attack_type)

def attack_info(df):

    intn_y = round(float(np.float64(((df['international'] == 1).sum()/(df['international'] != -9).sum())*100)),2)
    prop_y = round(float(np.float64(((df['property_damage'] == 1).sum()/(df['property_damage'] != -9).sum())*100)),2)
    suicide_y = round(float(np.float64(((df['suicide_attack'] == 1).sum()/(df['suicide_attack'] != -9).sum())*100)),2)
    succuss_y = round(float(np.float64(((df['succussful_attack'] == 1).sum()/(df['succussful_attack'] != -9).sum())))*100,2)
    
    intn_n = 100 - intn_y
    prop_n = 100 - prop_y
    suicide_n =100 - suicide_y
    succuss_n =100 - succuss_y
    
    trace1 = go.Bar(
    x=['International', 'Property Damage', 'Suicide Attack', 'Successful Attack'],
    y=[intn_y,prop_y,suicide_y,succuss_y],
    name='Yes',
    marker = dict(color = '#1883B2',),
    opacity = 0.8
    )
    trace2 = go.Bar(
    x=['International', 'Property Damage', 'Suicide Attack','Successful Attack'],
    y=[intn_n,prop_n,suicide_n,succuss_n],
    name='No',
    marker = dict(color = '#A4E3FF',),
    opacity = 0.8
    )

    data = [trace1, trace2]
    layout = go.Layout(
        title = 'Attack Distributions in Percentage',
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='attacks_info',auto_open = False)
    return plot_url
        
        


