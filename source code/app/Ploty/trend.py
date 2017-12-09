import plotly.plotly as py
import plotly.graph_objs as go

def trend(res):
	trace_high = go.Scatter(
		x=[v[0] for v in res],
		y=[v[1] for v in res],
		name = "fatality",
		line = dict(color = '#17BECF'),
		opacity = 0.8)

	trace_low = go.Scatter(
		x=[v[0] for v in res],
		y=[v[2] for v in res],
		name = "injury",
		line = dict(color = '#7F7F7F'),
		opacity = 0.8)

	data = [trace_high, trace_low]

	layout = dict(
		title='Fatality and Injury by Year',
		xaxis=dict(
			rangeslider=dict(),
			type='date'
			)
		)

	fig = dict(data=data, layout=layout)
	p1=py.plot(fig, filename = "trend plot", auto_open=False)
	return(p1)