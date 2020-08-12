import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import datetime

# example with multiple outputs: https://community.plotly.com/t/multiple-outputs-in-dash-now-available/19437

users = [{'label': "Polo", 'value': "Polo"},
         {'label': "Nastia", 'value': "Nastia"}]

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.Label('New user? Add your name to the list:'),
        html.Br(),
        dcc.Input(id='new-user', type='text', value=None),
        html.Br(),html.Br(),
        html.Button('Add new user', id='button', n_clicks=0),
        html.Br(),html.Br(),
        html.Div(id='new-user-feedback'),
        html.Br(),
        html.Label('Who is this?'),
        dcc.Dropdown(
            id='dropdown',
            options=users,
            value=None
        )],
        id = 'user-info'),

    html.Br(),

    html.Div([
        html.Label('How well did you sleep \
            today (0 = very poorly, 10 = perfectly well)?'),
        html.Br(),
        dcc.Slider(
            id = 'sleep-slider',
            min=0,
            max=11,
            marks={i: str(i) for i in range(1, 11)},
            value=5,
        ),
        html.Button('Save and show tracker', id='save_button', n_clicks=0),
        dcc.Graph(id = 'graph')],
        id = 'tracker-info'),
])


@app.callback(
    [Output('dropdown', 'options'),
     Output('new-user-feedback', 'children')],
    [Input('button', 'n_clicks')],
    [State('new-user', 'value'),
     State('dropdown', 'options')])
def update_users(n_clicks, value, existing_users):
    user_list = [user_entry['value'] for user_entry in existing_users]
    feedback = ''
    if n_clicks > 0:
        if value not in user_list:
            existing_users.append({'label': value, 'value': value})
            feedback = 'Your name is now in the database!'
        else:
            feedback = 'Your name already was in the database!'
    return existing_users, feedback

@app.callback(
    [Output('graph', 'figure')],
    [Input('save_button', 'n_clicks')],
    [State('sleep-slider', 'value')])
def update_output(n_clicks_slider, score):
    df = pd.DataFrame({'user': ['Polo', 'Nastia', 'Polo', 'Nastia', 'Polo'],
    'date': ['2020-08-01', '2020-08-02', '2020-08-03', '2020-08-04', '2020-08-05'],
    'sleep_score': [5, 6, 1, 2, 3]})
    df['date'] = pd.to_datetime(df['date'])
    if n_clicks_slider > 0:
        x = score
        tracker_dict = {}
        tracker_dict.update({'user': ['Lego'],
                               'date': [datetime.datetime.now().strftime('%Y-%m-%d')],
                               'sleep_score': [x]})
        day_df = pd.DataFrame.from_dict(tracker_dict)
        df = df.append(day_df, ignore_index = True)
        figure = px.line(df, x='date', y='sleep_score', title='Your sleep score')
        return [figure]
    else:
        raise PreventUpdate

if __name__ == '__main__':
    output = app.run_server(debug=True)