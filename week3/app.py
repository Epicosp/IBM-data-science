# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

drop_down_selections = [
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
    ]

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={
                'textAlign': 'center',
                'color': '#503D36',
                'font-size': 40
            }
        ),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
        dcc.Dropdown(
            id='site-dropdown',
            options=drop_down_selections,
            value='ALL',
            placeholder='select a launch site',
            searchable=True
        ),
        html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),
        html.Div(
            dcc.RangeSlider(
                id='payload-slider',
                min=0, max=10000, step=1000,
                value=[min_payload, max_payload]
            )
        ),
        html.P("Payload range (Kg):"),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig1 = px.pie(spacex_df, values='class', names='Launch Site', title='all launch successes')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].value_counts('class')
        fig1 = px.pie(filtered_df, values=filtered_df.values, names=filtered_df.index, title=f'{entered_site} successes')
    return fig1

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")])
def success_payload_scatter_chart(entered_site, entered_range):
    range_data = spacex_df[spacex_df['Payload Mass (kg)'].between(entered_range[0], entered_range[1])]
    if entered_site == 'ALL':
        fig2 = px.scatter(range_data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        filtered_df = range_data[range_data['Launch Site'] == entered_site]
        fig2 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
