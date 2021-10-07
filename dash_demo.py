import plotly.express as px
import pandas as pd

# data import

datetime_gp_hour = pd.read_csv('/home/rainermesi/Documents/myfitness_capacity/group_by_hour.csv')
venues_df = pd.read_csv('/home/rainermesi/Documents/myfitness_capacity/venues_list.csv')
venues_list = venues_df.values.tolist()

# data prep

fig1_table = datetime_gp_hour[datetime_gp_hour['tz_hour'] != 0]
#fig2_table = datetime_gp_hour[datetime_gp_hour['venue'].isin(venues_list[1])]
#fig2_table = fig2_table[fig2_table['tz_hour'] != 0]
#fig3_table = datetime_gp_hour[datetime_gp_hour['venue'].isin(venues_list[0])]
#fig3_table = fig3_table[fig1_table['tz_hour'] != 0]

# charts

fig1 = px.bar(fig1_table, x="tz_hour", y="cap",
                    barmode="group",
                    facet_col="venue",
                    facet_col_wrap=4,
                    width=800,
                    height=800,
                    labels={
                     "cap": "Capacity %",
                     "tz_hour": "Hour",
                     "venue": ""
                 })
fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig1.update_yaxes(title_font_size=10)

#fig2 = px.bar(fig2_table, x="tz_hour", y="cap",
#                    barmode="group",
#                    facet_col="venue",
#                    labels={
#                     "cap": "Capacity %",
#                     "tz_hour": "Hour",
#                     "venue": ""
#                 })
#fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

#for i in venues_df.values.tolist():
#    plot_table =  datetime_gp_hour[datetime_gp_hour['venue'].isin(i)]
#    plot_table = plot_table[plot_table['tz_hour'] != 0]
#    fig4 = px.bar(plot_table, x="tz_hour", y="cap",
#                    barmode="group",
#                    facet_col="venue",
#                    labels={
#                     "cap": "Capacity %",
#                     "tz_hour": "Hour",
#                     "venue": ""
#                 })
#    fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
#    fig4.show()

# plotly dash

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# for deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash(__name__)

app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls',
                                            children = [
                                                html.H2('Dash - Gym Popular Visit Times'),
                                                html.P('''Visualising MyFitness gym capacity with Plotly - Dash'''),
                                                html.P('''Pick one or more options from the dropdown below.''')
                                                        ]),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey',
                                    children = [
                                        html.H2('Graph - capacity'),
                                        html.P(
                                            dbc.Col(html.Div([dcc.Graph(id='bc1',figure=fig1)]))
                                            )
                                        ]
                                  ),  # Define the right element
                                  ])
                                ])

