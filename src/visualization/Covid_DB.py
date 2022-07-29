import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import datetime
import os

df_final=pd.read_csv('C:\\Users\\SAGARICA\covid_19_project\\data\\processed\\COVID_df_final.csv')

fig = go.Figure()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]
                    #meta_tags=[{'name': 'viewport',
                        #        'content': 'width=device-width, initial-scale=1.0'}]
                )
app.title = 'Covid-19 Dashboard'

colors = {
    'background': '#2C3531',
    'bodyColor':'#EEE2DC',
    'text': '#D1E8E2'
}
def get_page_heading_style():
    return {'backgroundColor': colors['background']}


def get_page_heading_title():
    return html.H1(children='COVID-19 Dashboard',
                                        style={
                                        'textAlign': 'center',
                                        'color': colors['text']
                                    })

def get_page_heading_subtitle():
    return html.Div(children='Goal of the project is to learn data science by applying a cross industry standard process, \
    it covers the full walkthrough of: automated data gathering, data transformations, \
    filtering and machine learning to approximating the doubling time, and \
    (static) deployment of responsive dashboard.',
                                         style={
                                             'textAlign':'center',
                                             'color':colors['text']
                                         })

def generate_page_header():
    main_header =  dbc.Row(
                            [
                                dbc.Col(get_page_heading_title(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    subtitle_header = dbc.Row(
                            [
                                dbc.Col(get_page_heading_subtitle(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    header = (main_header,subtitle_header)
    return header


page_header = generate_page_header()
app.layout = dbc.Container([

            page_header[0],
            page_header[1],
            html.Hr(),



            dbc.Row([
                dbc.Col([
                    html.P("Select the Country(s) from the list"),
                    dcc.Dropdown(
                        id= 'country_drop_down',
                        options=[ {'label': each, 'value': each} for each in df_final['country'].unique()],
                        value=['India','US','Germany'],
                        multi= True
                    )
                ]),

                dbc.Col([
                    html.P("Select the option"),
                    dcc.Dropdown(
                        id='doubling_time',
                        options=[
                            {'label': 'Timeline Confirmed ', 'value': 'confirmed'},
                            {'label': 'Timeline Confirmed Filtered', 'value': 'confirmed_filtered'},
                            {'label': 'Timeline Doubling Rate', 'value': 'confirmed_DR'},
                            {'label': 'Timeline Doubling Rate Filtered', 'value': 'confirmed_filtered_DR'},
                            ],
                        value='confirmed',
                        multi=False
                    )

                    ])

            ]),

            html.Hr(),

            dbc.Row([
                dbc.Col([

                        dcc.Graph(id='main_window_slope',figure= fig)


                        ], width= {'size':5, 'offset': 1})

            ], align ='start'),

            html.Hr(),




        ], fluid=True,style={'backgroundColor': colors['bodyColor']})

@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('doubling_time', 'value')])


def update_figure(country_list,show_doubling):


    if 'confirmed_DR' in show_doubling:
        my_yaxis={'type':"log",
               'title':'Approximated doubling rate over 3 days '
              }
    else:
        my_yaxis={'type':"log",
                  'title':'Confirmed infected people (source johns hopkins csse, log-scale)'
              }


    traces = []
    for each in country_list:

        df_plot=df_final[df_final['country']==each]

        if show_doubling=='confirmed_filtered_DR':
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.mean).reset_index()
        else:
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.sum).reset_index()
       #print(show_doubling)


        traces.append(dict(x=df_plot.date,
                                y=df_plot[show_doubling],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                )
    return {
            'data': traces,
            'layout': dict (
                            width=1200,
                            height=700,

                            xaxis={'title':'Timeline',
                                    'tickangle':-45,
                                    'nticks':20,
                                    'tickfont':dict(size=14,color="#7f7f7f"),
                                    },

                            yaxis=my_yaxis

                            )
        }



if __name__ == '__main__':
    app.run_server(debug= True, port='8000')
