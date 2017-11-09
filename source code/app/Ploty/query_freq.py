from models import *
from sqlalchemy import func
from sqlalchemy import and_
import plotly.plotly as py
import plotly.graph_objs as go 
import pandas as pd
import plotly
plotly.tools.set_credentials_file(username='xiaozhou0614', api_key='nKS0ddIHYYjKmMf5AnRw')

fq = (db.session.query(Location.country).
	join(Happened, and_(Location.latitude==Happened.latitude, Location.longitude == Happened.longitude)).
	all())


def freq(df, code):
    df = pd.DataFrame(df)
    df_kw = pd.merge(df, code, how='left', left_on='country', right_on='country_txt').drop(['country_txt','country'],axis=1)
    df_freq=df_kw.groupby(['COUNTRY','CODE']).size().reset_index(name="Freq")
    
    df=df_freq
    
    data = [ dict(
        type = 'choropleth',
        locations = df['CODE'],
        z = df['Freq'],
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
            title = 'Frequency'),
      ) ]

    layout = dict(
    title = '45 Years of Terrorism Frequency:1970-2015',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        showlegend = False,
        projection = dict(
            type = 'Mercator'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    plot_url = py.plot( fig, validate=False, filename='d3-world-map',auto_open = False)
    #iframe_string = '<iframe id="igraph" style="border:none" src="'  
    #iframe_string = iframe_string+plot_url+'/550/550" width="100%" height="700"></iframe>'
    
    return plot_url
