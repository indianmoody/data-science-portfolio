import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os


#df = pd.read_csv('drug-use-by-age.csv')
df = pd.read_csv('https://raw.githubusercontent.com/indianmoody/hosted-data/master/drug_app_dash/drug-use-by-age.csv')


description = '''
Drug abuse is one of biggest problems faced by US. This is not limited to a single age group. Data from website 538 and National Survey on Drug Use reveals distribution of alcohol, marijuana and various illicit drugs among 17 different age groups. 
'''


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[

    html.H1(children=[
	    html.P('Drug Use By Age'),
    ], style={'textAlign': 'center'}),

    html.H4(children=[
        html.P(description),
    ], style={'marginBottom': 50, 'marginTop': 25}),

    
    html.Div(children=[	
        html.Label('Select an Age Group from dropdown menu to see specific Drug Usage facts:'),

	    html.P(' '),

        dcc.Dropdown(
	        options=[
	            {'label' : '12', 'value' : '12'},
	            {'label' : '13', 'value' : '13'},
                {'label' : '14', 'value' : '14'},
                {'label' : '15', 'value' : '15'},
                {'label' : '16', 'value' : '16'},
                {'label' : '17', 'value' : '17'},
                {'label' : '18', 'value' : '18'},
                {'label' : '19', 'value' : '19'},
                {'label' : '20', 'value' : '20'},
                {'label' : '21', 'value' : '21'},
                {'label' : '22-23', 'value' : '22-23'},
                {'label' : '24-25', 'value' : '24-25'},
                {'label' : '26-29', 'value' : '26-29'},
                {'label' : '30-34', 'value' : '30-34'},
                {'label' : '35-49', 'value' : '35-49'},
                {'label' : '50-64', 'value' : '50-64'},
                {'label' : '65+', 'value' : '65+'}
	        ],
	        value='15',
	        id='input-id'
        )
    ], style={'marginBottom': 50, 'marginTop': 25}),

    dcc.Graph(id='my-div'),

    dcc.Graph(id='my-div-2')

])


@app.callback(
    Output(component_id='my-div', component_property='figure'),
    [Input(component_id='input-id', component_property='value')]

)
def updating_op(in_value):

    temp_df = df[df['age'] == in_value]
    columns1 = ['alcohol-use', 'marijuana-use','cocaine-use','crack-use','heroin-use','hallucinogen-use','inhalant-use','pain-releiver-use', 'oxycontin-use','tranquilizer-use','stimulant-use','meth-use','sedative-use']
    #columns2 = [x.replace('-use', '-frequency') for x in columns1]
    use_df = temp_df[columns1]
    #freq_df = temp_df[columns2]
    use_df = use_df.transpose()
    use_df.columns = ['use_col']
    #freq_df = freq_df.transpose()
    #freq_df.columns = ['freq_col']
    use_df.sort_values(by='use_col', inplace=True)
    #freq_df.sort_values(by='freq_col', inplace=True)
    use_df.index = use_df.index.map(lambda x: ' '.join(x.split('-')[:-1]).title())
    #freq_df.index = freq_df.index.map(lambda x: ' '.join(x.split('-')[:-1]).title())
    
    extra_layout = go.Layout(
        title='Percentage of Americans in selected age group who siad in a 2012 survey that they had used the following drugs in the past year',
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            ticks='outside'
        )
    )



    traces = []

    traces.append(go.Bar(
        x = use_df['use_col'],
        y = use_df.index.tolist(),
        orientation='h',
        text=use_df['use_col'].apply(lambda s: str(s)+'%'),
        textposition='outside'
    ))

    return {
        'data' : traces,
        'layout' : extra_layout
    }



@app.callback(
    Output(component_id='my-div-2', component_property='figure'),
    [Input(component_id='input-id', component_property='value')]

)
def updating_op2(in_value):
    temp_df = df[df['age'] == in_value]
    columns1 = ['alcohol-use', 'marijuana-use', 'cocaine-use', 'crack-use', 'heroin-use', 'hallucinogen-use',
                'inhalant-use', 'pain-releiver-use', 'oxycontin-use', 'tranquilizer-use', 'stimulant-use', 'meth-use',
                'sedative-use']
    columns2 = [x.replace('-use', '-frequency') for x in columns1]
    #use_df = temp_df[columns1]
    freq_df = temp_df[columns2]
    #use_df = use_df.transpose()
    #use_df.columns = ['use_col']
    freq_df = freq_df.transpose()
    freq_df.columns = ['freq_col']
    #use_df.sort_values(by='use_col', inplace=True)
    freq_df = freq_df.apply(pd.to_numeric, errors='coerce')
    freq_df.fillna(value=0, inplace=True)
    freq_df.sort_values(by='freq_col', inplace=True)
    #use_df.index = use_df.index.map(lambda x: ' '.join(x.split('-')[:-1]).title())
    freq_df.index = freq_df.index.map(lambda x: ' '.join(x.split('-')[:-1]).title())

    extra_layout2 = go.Layout(
        title='Median number of times a user in selected age group used following drugs in the past year',
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            ticks='outside'
        )
    )

    traces = []

    traces.append(go.Bar(
        x=freq_df['freq_col'],
        y=freq_df.index.tolist(),
        orientation='h',
        text=freq_df['freq_col'],
        textposition='outside'
    ))

    return {
        'data': traces,
        'layout': extra_layout2
    }



if __name__ == '__main__':
    app.run_server(debug=True)