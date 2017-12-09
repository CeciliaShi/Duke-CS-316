import plotly
import plotly.plotly as py
import pandas as pd
#plotly.tools.set_credentials_file(username='KimJin', api_key='kgTp9k4kEV7XfpUolr60')

def freq(df, code):
    df = df[pd.notnull(df['date'])]
    df_kw = pd.merge(df, code, how='left', left_on='country_txt', right_on='country_txt').drop(['country_txt'],axis=1)
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
        projection = dict(
            type = 'Mercator'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    plot_url = py.plot( fig, validate=False, filename='d3-world-map2',auto_open = False)
    #iframe_string = '<iframe id="igraph" style="border:none" src="'  
    #iframe_string = iframe_string+plot_url+'/550/550" width="100%" height="700"></iframe>'
    
    return plot_url