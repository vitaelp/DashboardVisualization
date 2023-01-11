import pandas as pd
import plotly.express as px


df = pd.read_csv('clean_data.csv')


fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="state", hover_data=["mag"],
                        color_discrete_sequence=["fuchsia"], zoom=2.5, height=800, color='mag',
                        size='mag', animation_frame="date")
fig.update_layout(mapbox_style="open-street-map")
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
