# CUNY DATA608 - Final Project - Zachary Herold
# In this project, the author creates a equity dashboard for the 49 Chinse B-share stocks
# listed on the Shanghai Stock Exchange. The dashboard includes the following panels:
# - Line graph of A-share versus B-share price differential (expressed in RMB at daily exchange rate)
# - Scatterplot of A and B-share monthly return (over 3 years) versus market index, with regression line
# - Hypothetical investment of $1000 of A-share/ B-share stock and respective market indices over user-selected time period.
# - Pie chart of Market capitalization break-down by floating share-type
# - Pie chart of latest stock volume (in dollars) as a percentage of total market volume

import pandas as pd
import numpy as np 
from datetime import datetime as dt
from sklearn.linear_model import LinearRegression
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
import chart_studio.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
pd.options.display.float_format = '{:.2f}'.format

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
file = 'https://raw.githubusercontent.com/ZacharyHerold/CUNY-DATA-608/master/daily_data.csv'

df = pd.read_csv(file, sep=',')
df = df[df.close_x != 0]
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["b_change"], how="all")

# Creating list of ticker-company name tuples
tickers = np.unique(np.array(df.ticker))
companies = []
for t in tickers:
    co = df[df.ticker==t]['company_name_en_x'].to_list()
    co = np.unique(co)
    companies.append(co)
companies = [y for x in companies for y in x]
t = tuple(zip(tickers, companies))

# total_market_cap = []
# for t in tickers:
#     total_market_cap.append(get_market_cap(t))
# sum(total_market_cap[1])

def get_first_dates(data):
    data = data[data['close_x'] != 0]
    data = data.loc[data.groupby(data.index.to_period('M')).apply(lambda x: x.index.min())]
    return data

def process_monthly(ticker):
    df2 = df[df.ticker == ticker]
    df2 = df2.assign(date = pd.to_datetime(df2['date'], format='%Y-%m-%d'))
    df2.set_index('date', inplace=True)
    df3 = get_first_dates(df2)
    df3 = df3.assign(return_monthly_b = df3['close_x'].pct_change())
    df3 = df3.assign(return_monthly_a = df3['close_y'].pct_change())
    df3 = df3.assign(return_monthly_ix1 = df3['ix1_close'].pct_change())
    df3 = df3.assign(return_monthly_ix3 = df3['ix3_close'].pct_change())
    df3 = df3.dropna()
    return df3

def hypothetical_return(data, type):
    investment = 1000
    data = data.assign(ix3_change = data.ix3_close.pct_change())
    data = data.assign(ix1_change = data.ix1_close.pct_change())
    if type == 'b':
        r = data.b_change
    if type == 'a':
        r = data.a_change
    if type == 'ix3':
        r = data.ix3_change
    if type == 'ix1':
        r = data.ix1_change
    returns_plus_one = r.add(1)
    cumulative_return = returns_plus_one.cumprod()
    inv = cumulative_return.mul(investment)
    return inv

def get_market_cap(t):
    df2 = df.replace(np.nan, 0)
    end_date = df2[df2.ticker==t]['date'].max()
    no_shares_b = df2[(df2.ticker==t) & (df2.date==end_date)]['shares_outstanding_b_x'].values[0]
    price_b =df2[(df2.ticker==t) & (df2.date==end_date)]['close_rmb'].values[0]
    b_cap = no_shares_b * price_b
    no_shares_a = df2[(df.ticker==t) & (df2.date==end_date)]['shares_outstanding_a_x'].values[0]
    price_a = df2[(df2.ticker==t) & (df2.date==end_date)]['close_y'].values[0]
    a_cap = no_shares_a * price_a
    total_cap = b_cap + a_cap
    return total_cap, b_cap, a_cap

def get_stock_volume(t):
    end_date = df[df.ticker==t]['date'].max()
    volume_stock = df[(df.ticker==t) & (df.date==end_date)]['volume_usd_x'].values[0]
    volume_market = get_market_volume()
    volume_other = volume_market - volume_stock 
    return volume_stock, volume_other

def get_market_volume():
    end_date = df[df.ticker==900901]['date'].max()
    volume=[]
    tickers = np.unique(np.array(df.ticker))
    for t in tickers:
        vol = df[(df.ticker==t) & (df.date==end_date)]['volume_usd_x'].values[0]
        volume.append(vol)
    volume_market = sum(volume)
    return volume_market

app.layout = html.Div([
    html.Div([
        html.H1('China B-Shares Dashboard')], 
    style={'align':'center'}),

    html.Div([
        html.H3('Select Stock'),
        dcc.RadioItems(
            id='ticker',
            options=[{'label': (str(i[0]) + ' - ' + str(i[1]) + '\n'), 'value': i[0]} for i in t],
            value=900901,
            labelStyle={'display': 'block', 'color': 'black', 'fontSize': 13})
    ],
    style={'width': '15%', 'margin': 10, 'float': 'left', 'display': 'inline-block', 'font': t
    #'backgroundColor': '#DC143C'
    }),
    
    html.Div([
        html.Div([
            html.H2('B- and A- Shares Price Differential'),
            dcc.Graph(id='price-chart')], 
        style={'width': '40%', 'display': 'inline-block'}),

        html.Div([       
            html.H2('Beta for B- and A- Shares'),
            dcc.Graph(id='beta-chart')],
            # html.label('Beta of B-Share:'),
            # html.label('Beta of A-Share:'),
        style={'width': '40%', 'float': 'right', 'display': 'inline-block'})
    
    ], style={
        #'borderBottom': 'thin lightgrey solid',
        #'backgroundColor': '#000000',
        #'padding': '100px 5px'
    }),

    html.Div([
        html.Div([
            html.H2('Return on Hypothetical Investment'),
            dcc.Graph(id='investment-chart'),
            html.H3('Select a starting date'),
            dcc.DatePickerSingle(
                id='date-picker-single',
                min_date_allowed=dt(2016, 9, 1),
                max_date_allowed=dt(2019, 11, 28),
                date=dt(2016, 9, 1)
            )
        ],
        style={'width': '40%', 'display': 'inline-block'}),

        html.Div([
            html.H2('Market Capitalization'),
            dcc.Graph(id='donut-chart')
        ],
        style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),

        html.Div([
            html.H2('Share of Market Volume'),
            dcc.Graph(id='donut-chart2'),
            html.H4('On 11/29/2019')
        ],
        style={'width': '20%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        #'padding': '100px 5px'
    })
],
    style={
        'backgroundColor': '#B0C4DE',
    })

@app.callback(
    Output('price-chart', 'figure'),
    [Input('ticker', 'value')])
def update_price_chart(ticker):
    df2 = df[df.ticker == ticker]
    trace1 = go.Scatter(
        x=df2['date'],
        y=df2['close_rmb'],
        mode='lines',
        name='B-share price (in RMB)')
    trace2 = go.Scatter(
        x=df2['date'],
        y=df2['close_y'],
        mode='lines',
        name='A-share price')

    data = [trace1, trace2]
    fig = go.Figure(data)
    return fig

@app.callback(
    Output('beta-chart', 'figure'),
    [Input('ticker', 'value')])
def update_beta_chart(ticker):
    df = process_monthly(ticker)
    # reg = LinearRegression().fit(df['return_monthly_ix3'], df['return_monthly_b'])
    # df['bestfit_b'] = reg.predict(df['return_monthly_ix3'])
    reg = LinearRegression().fit(np.vstack(df['return_monthly_ix3']), df['return_monthly_b'])
    df['bestfit_b'] = reg.predict(np.vstack(df['return_monthly_ix3']))
    #if df['return_monthly_a'].notnull():
    reg2 = LinearRegression().fit(np.vstack(df['return_monthly_ix1']), df['return_monthly_a'])
    df['bestfit_a'] = reg2.predict(np.vstack(df['return_monthly_ix1']))
    # https://stackoverflow.com/questions/58708230/plotly-how-to-plot-a-regression-line-using-plotly

    trace1 = go.Scatter(
        x=df['return_monthly_ix3'],
        y=df['return_monthly_b'],
        mode='markers',
        marker=dict(
            size=10,
            color='red'),
        name='B-share returns')
    trace2 = go.Scatter(
        x=df['return_monthly_ix1'],
        y=df['return_monthly_a'],
        mode='markers',
        marker=dict(
            size=10,
            color='blue'),
        name='A-share returns')
    trace3 = go.Scatter(
        x=df['return_monthly_ix3'],
        y=df['bestfit_b'],
        mode='lines',
        name='B-share regression line')
    trace4 = go.Scatter(
        x=df['return_monthly_ix1'],
        y=df['bestfit_a'], 
        mode='lines',
        name='A-share regression line')

    data = [trace1, trace2, trace3, trace4]
    fig = go.Figure(data)
    return fig

@app.callback(
    Output('investment-chart', 'figure'),
    [Input('ticker', 'value'),
    Input('date-picker-single', 'date')])
def update_investment_chart(ticker, d):
    df2 = df[(df['ticker'] == ticker) & (df['date'] >= d)]

    trace1 = go.Scatter(
        x=df2['date'],
        y=hypothetical_return(df2, 'b'),
        mode='lines',
        name='B-share Stock')
    trace2 = go.Scatter(
        x=df2['date'],
        y=hypothetical_return(df2, 'a'),
        mode='lines',
        name='A-share Stock')
    trace3 = go.Scatter(
        x=df2['date'],
        y=hypothetical_return(df2, 'ix3'),
        mode='lines',
        name='B-share Index')
    trace4 = go.Scatter(
        x=df2['date'],
        y=hypothetical_return(df2, 'ix1'),
        mode='lines',
        name='A-share Index')
    # trace5 = go.Scatter(
    #     x=df2['date'],
    #     y=1000,
    #     mode='lines',
    #     name='baseline')
    #     #linecolor = 'black')
    #     #line=dict(color='black', width=4,, dash='dash'))

    data = [trace1, trace2, trace3, trace4]
    fig = go.Figure(data)
    return fig

@app.callback(
    Output('donut-chart', 'figure'),
    [Input('ticker', 'value')])
def update_pie_chart(ticker):
    labels = ['B-share Market Cap', 'A-share Market Cap']
    total_cap, b_cap, a_cap = get_market_cap(ticker)
    values = [b_cap, a_cap]
    fig = go.Figure(
        data=go.Pie(labels=labels, values=values, hole=.3))
    return fig

@app.callback(
    Output('donut-chart2', 'figure'),
    [Input('ticker', 'value')])
def update_pie_chart(ticker):
    labels = ['Trading Volume', 'Other Stocks']
    df2 = df[df.ticker == ticker]
    volume_stock, volume_other = get_stock_volume(ticker)
    values = [volume_stock, volume_other]

    fig = go.Figure(
        data=go.Pie(labels=labels, values=values, hole=.3))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

