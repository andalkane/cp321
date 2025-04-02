#!/usr/bin/env python
# coding: utf-8

# In[5]:


#libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

 
app = dash.Dash(__name__, server=app.server)

#dataset from wiki
wc_data = [
    {"Year": 2018, "Winner": "France", "Runner-up": "Croatia"},
    {"Year": 2014, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 2010, "Winner": "Spain", "Runner-up": "Netherlands"},
    {"Year": 2006, "Winner": "Italy", "Runner-up": "France"},
    {"Year": 2002, "Winner": "Brazil", "Runner-up": "Germany"},
    {"Year": 1998, "Winner": "France", "Runner-up": "Brazil"},
    {"Year": 1994, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1990, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 1986, "Winner": "Argentina", "Runner-up": "Germany"},
    {"Year": 1982, "Winner": "Italy", "Runner-up": "Germany"},
    {"Year": 1978, "Winner": "Argentina", "Runner-up": "Netherlands"},
    {"Year": 1974, "Winner": "Germany", "Runner-up": "Netherlands"},
    {"Year": 1970, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1966, "Winner": "England", "Runner-up": "Germany"},
    {"Year": 1962, "Winner": "Brazil", "Runner-up": "Czechoslovakia"},
    {"Year": 1958, "Winner": "Brazil", "Runner-up": "Sweden"},
    {"Year": 1954, "Winner": "Germany", "Runner-up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "Runner-up": "Brazil"},
    {"Year": 1938, "Winner": "Italy", "Runner-up": "Hungary"},
    {"Year": 1934, "Winner": "Italy", "Runner-up": "Czechoslovakia"},
    {"Year": 1930, "Winner": "Uruguay", "Runner-up": "Argentina"}
]

df = pd.DataFrame(wc_data) #convert to pandas

#a function to count WC wins (grouped by country)
def wincounts():
    win_count = df['Winner'].value_counts().reset_index() 
    win_count.columns = ['Country', 'Wins']
    return win_count

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Winners:"), #title
    
    dcc.Graph(id='world-map'),#world map position

    #dropdown 1 (selecting a country to view wins)
    html.Label("Select a country to see their wins:"),
    dcc.Dropdown(id='country-dropdown', options=[
        {'label': c, 'value': c} for c in wincounts()['Country']
    ], placeholder="Select a country"),
    
    dcc.Graph(id='wins-bar-chart'), #graph for countries wins

    #drop down to select year for win and R-U
    html.Label("Select a year to see the winner & runner-up:"),
    dcc.Dropdown(id='year-dropdown', options=[
        {'label': y, 'value': y} for y in df['Year']
    ], placeholder="Select a year:"),
    
    html.Div(id='year-info') #print the winner and R-U for year
])

#THE WORLD MAP
@app.callback( #updating the world map with selection
    Output('world-map', 'figure'),
    Input('country-dropdown', 'value')
)

def world_map(_):
    data = wincounts()
    fig = px.choropleth(data, locations="Country", 
                        locationmode='country names',
                        color="Wins", 
                        title="World Cup Wins by Country")
    return fig

#THE BAR GRAPH
@app.callback(
    Output('wins-bar-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def bar_chart(country):
    data = wincounts()
    if country:
        data = data[data['Country'] == country]
    fig = px.bar(data, x='Country', y='Wins', title=f"World Cup Wins for {country}" if country else "Total Wins")
    return fig
    
#PRINTING THE YEAR
@app.callback(
    Output('year-info', 'children'),
    Input('year-dropdown', 'value')
)
def year_info(year):
    if year:
        row = df[df['Year'] == year].iloc[0]
        return html.P(f"{year} Winner: {row['Winner']}, Runner-up: {row['Runner-up']}")
    return ""

if __name__ == "__main__":
    app.run(debug=True, port=8051, host="0.0.0.0")

# In[ ]:

