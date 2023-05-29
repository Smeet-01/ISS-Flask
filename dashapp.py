from dash import Dash, html, dcc
import pandas as pd
import requests
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "iframe"

url = 'http://api.open-notify.org/iss-now.json'

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Graph(config={'staticPlot': True}, id="graph"),
    dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0)
])

@app.callback(Output('graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_data(n):
    response = requests.get(url)
    data = response.json()  
    fig = go.Figure(go.Scattergeo())
    fig.add_scattergeo(lat=[float(data['iss_position']['latitude'])], 
                    lon=[float(data['iss_position']['longitude'])],
                    marker=dict(color='black', symbol='circle', size=8))
    fig.update_geos(landcolor='#3399ff', showocean=True, oceancolor='#CCE5FF')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)