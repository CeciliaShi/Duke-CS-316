from models import *
from sqlalchemy import func
from sqlalchemy import and_
import plotly.plotly as py
import plotly.graph_objs as go 
import pandas as pd

#python -c "import plotly; plotly.tools.set_credentials_file(username='KimJin', api_key='kgTp9k4kEV7XfpUolr60')"

wk = (db.session.query(Incident.nkill, Incident.nwound, Location.country).
	join(Happened, and_(Happened.incident_id==Incident.id)).
	join(Location, and_(Location.latitude==Happened.latitude, Location.longitude == Happened.longitude)).
	all())
wk = pd.DataFrame(wk)
code = pd.read_csv('code_correct.csv')

def kill_wound(df, code):
    df_kw = pd.merge(df, code, how='left', left_on='country', right_on='country_txt').drop(['country_txt','country'],axis=1)
    df_kw[['nwound', 'nkill']]=df_kw[['nwound', 'nkill']].fillna(0)
    df_kw['total'] = df_kw['nwound'] + df_kw['nkill']
    df_kwgroup=df_kw[['COUNTRY', 'total','CODE']].groupby(['COUNTRY', 'CODE']).sum()
    df_kwgroup.reset_index(inplace=True)
    
    df=df_kwgroup
    
    data = [dict(
        type = 'choropleth',
        locations = df['CODE'],
        z = df['total'],
        text = df['COUNTRY'],
        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'Intensity<br>Combining fatalities and injuries'),
      			) 
    		]

    layout = dict(
    	title = '45 Years of Terrorism:1970-2015',
    	geo = dict(
    		showframe = False,
    		showcoastlines = False,
    		projection = dict(
    			type = 'Mercator')	
    		)		
    	)

    fig = dict(data=data, layout=layout )
    plot_url = py.plot(fig, validate=False, filename='d3-world-map',auto_open=False)
    iframe_string = '<iframe id="igraph" style="border:none" src="'  
    iframe_string = iframe_string+plot_url+'/550/550" width="100%" height="700"></iframe>'
    
    return iframe_string


