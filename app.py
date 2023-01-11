import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

state_names = pd.read_csv('stateAbbreviations.csv')
df = pd.read_csv('clean_data.csv')

colors = {
        'background': '#acacfc',
        'text': '#0f0f6b'
    }

app.layout = html.Div(children=[

    html.H1("EARTHQUAKE DASHBOARD WITH DASH", style={'text-align': 'center', 'color': colors['text']}),
    html.H2("Advanced Data Visualisation - Gruppe 5", style={'text-align': 'center', 'color': colors['text']}),
    html.H3("V. Elpeza, C. Marxer und A.Ruggia", style={'text-align': 'center', 'color': colors['text']}),

    html.H4("Wähle deine US-Bundesstaaten aus!", style={'text-align': 'left', 'color': colors['text']}),

    dcc.Dropdown(id='state',
                 options=[{"label": x, "value": x}
                          for x in df["state"].unique()],
                 multi=True,
                 value=['Texas', 'California'],
                 style={"width": "40%", 'color': colors['text'], 'color': colors['text']}),

    html.H4("Möchtest du nur ein bestimmtes Jahr genauer anschauen?", style={'text-align': 'left', 'color': colors['text']}),

    dcc.Dropdown(id='jahr',
                 options=[{"label": x, "value": x}
                          for x in df['year'].unique()],
                 style={"width": "40%", 'color': colors['text'], 'color': colors['text']}),

    html.H4("Wähle die Reichweite der Erdbebenstärken aus: ", style={'text-align': 'left', 'color': colors['text']}),

    dcc.RangeSlider(id='magn_range',
                    marks={i: 'Magnitude {}'.format(i) for i in range(11)},
                    min=0,
                    max=10,
                    value=[0, 10],
                    allowCross=False,
                    tooltip={'always visible': True,  # show current slider values
                             'placement': 'top'}),

    html.Div(children=[
        dcc.Graph(id='plot1', figure={}),
        dcc.Graph(id='plot2', figure={})],
        style={'display': 'inline-block',
               'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '3vw',
               'width': '40vw', 'height': '40vh'
               }),

    html.Div(children=[
        dcc.Graph(id='plot3', figure={}),
        dcc.Graph(id='plot4', figure={})],
        style={'display': 'inline-block',
               'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '3vw',
               'width': '40vw', 'height': '40vh'
               }),
])


@app.callback(
    [Output(component_id='plot1', component_property='figure'),
     Output(component_id='plot2', component_property='figure'),
     Output(component_id='plot3', component_property='figure'),
     Output(component_id='plot4', component_property='figure')],
    [Input(component_id='state', component_property='value'),
     Input(component_id='magn_range', component_property='value'),
     Input(component_id='jahr', component_property='value')]
)


def update_graph(state, magn_range, jahr):
    dff = df.copy()
    print(state)
    if bool(state):  # If nothing is selected, this is false so no filtering
        dff = dff[dff['state'].isin(state)]
    if bool(magn_range):  # Filterung durch die Slider-Values
        mag_min = magn_range[0]
        mag_max = magn_range[1]
        dff = dff[dff['mag'].between(mag_min, mag_max)]

    #TODO - Falls nur ein Jahr betrachtet wird können wir hier für die Jahresansicht andere Grafiken generieren
    #aktuell sind es noch dieselben ausser der Jahresverlauf welcher gelöscht wurde
    if bool(jahr):
        dff = dff[dff['year'] == jahr]
    # Plotly Express
        fig1 = px.scatter_mapbox(dff, title="Map-View of selected U.S. States", lat="latitude", lon="longitude",
                                 hover_name="state",
                                 template="ggplot2",
                                 hover_data=["mag"],
                                 color_discrete_sequence=["fuchsia"], zoom=2.5, height=800, color='mag',
                                 size='mag')
        fig1.update_layout(mapbox_style="open-street-map")

        fig2 = px.histogram(dff, x="state",
                            title="Vergleich der Anzahl Erdbeben der US-Bundesstaaten im ausgewählten Jahr",
                            height=800,
                            template="ggplot2",
                            color_discrete_sequence=['rgba(0,0,128,0.8)']).update_xaxes(
            categoryorder='total descending')

        fig3 = px.box(dff, x="state", y="mag")
        fig3.update_layout(
            title="Erdbeben in USA: Box-Plot",
            template="ggplot2",
            plot_bgcolor='rgba(255,255,255,0)',
            # width=1650,
            height=800,
            showlegend=False)

        fig4 = px.scatter(dff, x="depth", y="mag", color='mag',
                          title="Scatterplot bezügliche Erdbebenstärke und Entstehungstiefe", height=800,template="ggplot2")
        fig4.update_xaxes(ticksuffix=" km")




        return fig1, fig2, fig3, fig4

    else:
        # Plotly Express
        fig1 = px.scatter_mapbox(dff, title="Map-View of selected U.S. States", lat="latitude", lon="longitude",
                                 hover_name="state",
                                 template="ggplot2",
                                 hover_data=["mag"],
                                 color_discrete_sequence=["fuchsia"], zoom=2.5, height=800, color='mag',
                                 size='mag')
        fig1.update_layout(mapbox_style="open-street-map")

        fig2 = px.histogram(dff, x="state",
                            title="Vergleich der Anzahl Erdbeben der US-Bundesstaaten von 01.01.2016-31.12.2020",
                            height=800,
                            template="ggplot2",
                            color_discrete_sequence=['rgba(0,0,128,0.8)']).update_xaxes(categoryorder='total descending')
        # Timelinediagramm
        fig3 = go.Figure()
        # Gruppierung nach Erdbeben pro Jahr
        dff_year = dff.groupby('year', as_index=False).size()
        print(dff_year)
        fig3 = fig3.add_trace(go.Scatter(x=dff_year["year"], y=dff_year["size"],
                                         mode="lines+markers",
                                         name="Anzahl Erdbeben pro Jahr",
                                         marker_color="rgba(152, 0, 0, .8)",
                                         line=dict(color="rgba(0, 0, 128, .8)")
                                         ))
        fig3.update_layout(
            title="Anzahl Erdbeben pro Jahr",
            plot_bgcolor='rgba(137, 40, 212,0)',
            # width=1650,
            height=800,
            template="ggplot2",
            showlegend=False,
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1
            ))
        fig3.update_xaxes(showline=True, linewidth=2, linecolor="rgb(211, 211, 211)", gridcolor="rgb(211, 211, 211)")
        fig3.update_yaxes(showline=True, linewidth=2, linecolor="rgb(211, 211, 211)", gridcolor="rgb(211, 211, 211)")

        fig4 = px.scatter(dff, x="depth", y="mag", color='mag',
                          title="Scatterplot bezügliche Erdbebenstärke und Entstehungstiefe", height=800,template="ggplot2")
        fig4.update_xaxes(ticksuffix=" km")

        return fig1, fig2, fig3, fig4


if __name__ == '__main__':
    app.run_server(debug=False)