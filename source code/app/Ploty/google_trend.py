from models import GoogleTrend
from models import db
import plotly.plotly as py
import plotly.graph_objs as go

base_query = (db.session.query(GoogleTrend.date, GoogleTrend.weighted_avg)).all()

def google_trend(res):
	trend_year = go.Scatter(
		x = [v[0] for v in res],
    	y = [v[1] for v in res],
    	name = "trend",
    	line = dict(color = '#17BECF'),
    	opacity = 0.8)

	data = [trend_year]
	
    layout = dict(
        title='Google Trend',
        xaxis=dict(
            rangeslider=dict(),
            type='date')
        )

    fig = dict(data=data, layout=layout)
    p1 = py.plot(fig, filename='google trend by date', auto_open=False)
    return(p1)

