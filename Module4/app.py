######################################################################################
###################### CUNY DATA608 ##################################################
###################### HOMEWORK 4 ####################################################
###################### ZACHARY HEROLD ################################################
######################################################################################
# 
# # Build a dash app for a arborist studying the health of various tree species (as defined by the
# variable ‘spc_common’) across each borough (defined by the variable ‘borough’). This
# arborist would like to answer the following two questions for each species and in each borough:

# 1. What proportion of trees are in good, fair, or poor health according to the ‘health’ variable?
# 2. Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees?

# Notes: Total Number of Trees in db by Borough 
# Bronx max = 80584
# Manhattan max = 62427
# Queens max = 237970
# Staten Island max = 101442
# Brooklyn max = 169744

import dash
import dash_core_components as dcc
import dash_html_components as html
import chart_studio.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
boroughs = ['Queens', 'Bronx', 'Manhattan', 'Staten Island', 'Brooklyn']
health = ['Fair', 'Good', 'Poor']
steward_vals = ['1or2', '3or4', '4orMore', 'None']
species = ["'Schubert' chokecherry",'American beech','American elm','American hophornbeam','American hornbeam','American larch','American linden',\
 'Amur cork tree','Amur maackia','Amur maple','Atlantic white cedar','Atlas cedar','Callery pear','Chinese chestnut','Chinese elm',\
 'Chinese fringetree','Chinese tree lilac','Cornelian cherry','Douglas-fir','English oak','European alder','European beech','European hornbeam',\
 'Himalayan cedar','Japanese hornbeam','Japanese maple','Japanese snowbell','Japanese tree lilac','Japanese zelkova','Kentucky coffeetree',\
 'Kentucky yellowwood','London planetree','Norway maple','Norway spruce','Ohio buckeye','Oklahoma redbud','Osage-orange','Persian ironwood',\
 "Schumard's oak",'Scots pine','Shantung maple','Siberian elm','Sophora','Turkish hazelnut','Virginia pine','arborvitae','ash','bald cypress','bigtooth aspen','black cherry',\
 'black locust','black maple','black oak','black pine','black walnut','blackgum', 'blue spruce', 'boxelder', 'bur oak', 'catalpa',\
 'cherry', 'cockspur hawthorn', 'common hackberry', 'crab apple', 'crepe myrtle', 'crimson king maple', 'cucumber magnolia', 'dawn redwood',\
 'eastern cottonwood', 'eastern hemlock', 'eastern redbud', 'eastern redcedar', 'empress tree', 'false cypress', 'flowering dogwood', 'ginkgo',\
 'golden raintree', 'green ash', 'hardy rubber tree', 'hawthorn', 'hedge maple', 'holly', 'honeylocust', 'horse chestnut', 'katsura tree', 'kousa dogwood',\
 'littleleaf linden', 'magnolia', 'maple', 'mimosa', 'mulberry', 'northern red oak', 'pagoda dogwood', 'paper birch', 'paperbark maple',\
 'pignut hickory', 'pin oak', 'pine', 'pitch pine', 'pond cypress', 'purple-leaf plum', 'quaking aspen', 'red horse chestnut',\
 'red maple', 'red pine', 'river birch', 'sassafras', 'sawtooth oak', 'scarlet oak', 'serviceberry', 'shingle oak',\
 'silver birch', 'silver linden', 'silver maple', 'smoketree', 'southern magnolia', 'southern red oak', 'spruce',\
 'sugar maple', 'swamp white oak', 'sweetgum', 'sycamore maple', 'tartar maple', 'tree of heaven', 'trident maple',\
 'tulip-poplar', 'two-winged silverbell', 'weeping willow', 'white ash', 'white oak', 'white pine', 'willow oak']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def get_tree_data(boro, tree_cutoff):
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,health&' +\
        '$where=boroname=\'' + boro +\
        '\'&$limit=300000').replace(' ', '%20')
    soql_trees = pd.read_json(soql_url)
    soql_trees = soql_trees.dropna()
    df = pd.crosstab(soql_trees['spc_common'], soql_trees['health'], margins=True)
    df = df[df['All'] >= tree_cutoff]
    return df

def get_steward_data(boro, tree_type):
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,steward&' +\
        'boroname=' + str(boro) +\
        '&spc_common=' + str(tree_type) +\
        '&$limit=300000').replace(' ', '%20')
    soql_trees = pd.read_json(soql_url)
    soql_trees = soql_trees.dropna()
    df = pd.crosstab(soql_trees['steward'], soql_trees['health'], margins=True)
    return df

def convert_conditional_proba(df):
    df = df.drop(['All'], axis=1) #Removes total column
    df = df.apply(lambda r: round(r/r.sum() * 100,2), axis=1) #Calculates conditional probabilities
    df = df.drop(df.index[len(df)-1]) #Drops last row (summation)
    df = df.reset_index()
    return df

app.layout = html.Div([
    html.H1('CUNY DATA608 Module 4'),

    html.Div([
        html.Label('QUESTION 1 -- Choose Cutoff Point for Min. Tree Quantity of Species'),
        dcc.Slider(
            id='tree_cutoff',
            marks={i: '{}'.format(i) for i in range(0,1000,100)},
            min=0,
            max=1000,
            value=50,
            step=25)
    ],   
    style={'width': '30%', 'margin': 20, 'display': 'inline-block'}),
    
    html.Div([
        html.Label('QUESTION 1&2 -- Choose Borough'),
        dcc.Dropdown(
            id='boro',
            options=[{'label': i, 'value': i} for i in boroughs],
            value='Manhattan')
    ],
    style={'width': '25%', 'margin': 20, 'display': 'inline-block'}),

    html.Div([
        html.Label('QUESTION 2 -- Choose Tree Species'),
        dcc.Dropdown(
            id='tree_type',
            options=[{'label': i, 'value': i} for i in species],
            value='maple')
    ],
    style={'width': '25%', 'margin': 20, 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='stacked-barchart')
    ],
    style={'width': '65%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='stacked-barchart2')
    ],
    style={'width': '30%', 'display': 'inline-block'}),
])

@app.callback(
    dash.dependencies.Output('stacked-barchart', 'figure'),
    [dash.dependencies.Input('boro', 'value'),
    dash.dependencies.Input('tree_cutoff', 'value')])
def update_graph(boro, tree_cutoff):
        df = get_tree_data(boro, tree_cutoff)
        df = convert_conditional_proba(df).sort_values(by='Poor', ascending=False)
        df.iloc[:,0] = df.iloc[:,0].str.upper()

        trace1 = go.Bar(
            x=df.iloc[:,0],
            y=df.iloc[:,2],
            name='Good',
            #orientation='h'
        )
        trace2 = go.Bar(
            x=df.iloc[:,0],
            y=df.iloc[:,1],
            name='Fair',
            #orientation='h'
        )
        trace3 = go.Bar(
            x=df.iloc[:,0],
            y=df.iloc[:,3],
            name='Poor',
            #orientation='h'
        )
        data = [trace1, trace2, trace3]
        layout = go.Layout(title='<b>Tree Health in {}</b>'.format(boro), 
            height= 600, margin = dict(b= 180),
            barmode='stack'
        )
        return {"data": data, "layout": layout}
        

@app.callback(
    dash.dependencies.Output('stacked-barchart2', 'figure'),
    [dash.dependencies.Input('boro', 'value'),
    dash.dependencies.Input('tree_type', 'value')])
def update_graph(boro, tree_type):
        df = get_steward_data(boro, tree_type)
        df = convert_conditional_proba(df).sort_values(by='Poor', ascending=False)

        trace1 = go.Bar(
            y=df.iloc[:,2],
            x=df.iloc[:,0],
            name='Good',
            #orientation='h'
        )
        trace2 = go.Bar(
            y=df.iloc[:,1],
            x=df.iloc[:,0],
            name='Fair',
            #orientation='h'
        )
        trace3 = go.Bar(
            y=df.iloc[:,3],
            x=df.iloc[:,0],
            name='Poor',
            #orientation='h'
        )
        data = [trace1, trace2, trace3]
        layout = go.Layout(
            title='<b>Condition for {} based on # Stewards</b>'.format(tree_type), 
            height= 600, margin = dict(b= 180),
            barmode='stack'
        )
        return {"data": data, "layout": layout}

if __name__ == '__main__':
    app.run_server(debug=True)