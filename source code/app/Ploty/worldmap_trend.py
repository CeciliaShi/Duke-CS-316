import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
from sqlalchemy import *

def gt_freq(df, code):
    df[['weighted_avg']] = df[['weighted_avg']].astype(float)
    df = df[['weighted_avg', 'country']]
    df = df.groupby(['country'], as_index=False).mean()
    df_kw = pd.merge(df, code, how='left', left_on='country', right_on='country_txt').drop(['country_txt','country'],axis=1)
    #df_freq=df_kw.groupby(['COUNTRY','CODE']).size().reset_index(name="Freq")
    
    df=df_kw
    
    data = [ dict(
        type = 'choropleth',
        locations = df['CODE'],
        z = df['weighted_avg'],
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
            thickness = 10,
            autotick = False,
            title = 'Google Trend Weighted Average'),
      ) ]

    layout = dict(
    title = 'Google Trend of Terrorism Frequency:2004-2017',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    plot_url = py.plot( fig, validate=False, filename='d3-world-map1',auto_open = False)
    #iframe_string = '<iframe id="igraph" style="border:none" src="'  
    #iframe_string = iframe_string+plot_url+'/550/550" width="100%" height="700"></iframe>'

    return plot_url