from dash import html, dcc
from dash import Dash, Input, Output, State, callback_context, no_update
import dash_bootstrap_components as dbc
import random
import pandas as pd
import pathlib
from gtts import gTTS
import base64
import io
import openpyxl

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.15.4/css/all.css"])
server = app.server
app.title = "theec practice"

# Function to get data
def get_pandas_data(dfordenada: str) -> pd.DataFrame:
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath('../src/assets').resolve()
    return pd.read_excel(DATA_PATH.joinpath(dfordenada), sheet_name=None)

# GET THE DATA FROM EXCEL
dithe = get_pandas_data("the.xlsx")

# Data for the translation warm-up card
dfthe = dithe['warm']
lindex = list(dfthe.index)
lcol = dfthe['structure'].unique()
loptions = [{'label': str(option), 'value': option} for option in lcol]

card_style = {"width": "100%", "margin": "auto", "padding": "10px", "borderColor": "#d9534f", "borderWidth": "2px"}
# Card for the warm-up
card_warm = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-running fa-3x", style={'color': 'grey'}), ' ',
             'TRANSLATION WARM-UP    .', html.I(className="fas fa-running fa-3x", style={'color': 'grey'})],
            className="class-subtitle"
        ),
        dbc.CardBody(
            [
                html.H4('CHOOSE A STRUCTURE', className="card-title"),
                dcc.Dropdown(loptions, value='all', id='mydrop'),
                html.Div(id='container-button-timestamp0'),
                html.P('click button', className="card-text mt-2"),
                dbc.Button('SPANISH', id='btn-nclicks-1', n_clicks=0, color="info", className="me-1"),
                html.Div(id='container-button-timestamp'),
                dbc.Button('ENGLISH', id='btn-nclicks-2', n_clicks=0, color="primary", className="me-1"),
                html.Div(id='container-button-timestamp2'),
                html.Audio(id='tts-audio', controls=True, style={'width': '100%'})
            ],
        )
    ],
    color="danger",
    outline=True,
    style=card_style
)

# Data for the reported speech
dfreport = dithe['reportedsp']
lindexrep = list(dfreport.index)
lcolrep = dfreport['story'].unique()
loptionsrep = [{'label': str(option), 'value': option} for option in lcolrep]



# Card for the reported
card_rep = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-comments fa-3x", style={'color': 'grey'}), ' ',
             'REPORTED SPEECH     .', html.I(className="fas fa-comments fa-3x", style={'color': 'grey'})],
            className="class-subtitle"
        ),
        dbc.CardBody(
            [
                html.H4('CHOOSE A STORY', className="class-subtitle"),
                dcc.Dropdown(loptionsrep, value='karl and Ana', id='mydroprep'),
                html.Div(id='container-button-timestamp0rep'),
                html.P('click button', className="card-text mt-2"),
                dbc.Button('DIRECT', id='btn-nclicksrep-1', n_clicks=0, color="info", className="me-1"),
                html.Div(id='container-button-timestamprep'),
                dbc.Button('REPORTED', id='btn-nclicksrep-2', n_clicks=0, color="primary", className="me-1"),
                html.Div(id='container-button-timestamp2rep'),
            ],
        )
    ],
    color="danger",
    outline=True,
    style=card_style
)

# Data for the pictures
dfpic = dithe['pictures']
didfpic = dfpic.to_dict('records')

# Card for the pictures
card_pic = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-camera fa-3x", style={'color': 'grey'}), ' ',
             'DESCRIBE THE PICTURES', html.I(className="fas fa-camera fa-3x", style={'color': 'grey'})],
            className="class-subtitle"
        ),
        dbc.CardBody(
            [
                html.H4('CHOOSE A PICTURE', className="card-title"),
                html.P('click button', className="card-text mt-2"),
                dbc.Button('PICTURE', id='btn-nclickspic-1', n_clicks=0, color="info", className="me-1"),
                html.Div(id='container-button-timestamppic'),
                dbc.Button('DESCRIPTION', id='btn-nclickspic-2', n_clicks=0, color="primary", className="me-1"),
                html.Div(id='container-button-timestamp2pic'),
            ],
        )
    ],
    color="danger",
    outline=True,
    style=card_style
)

# Data for the interrogative challenge
dfinter = dithe['question']
lindexinter = list(dfinter.index)
lcolinter = dfinter['word'].unique()
loptionsinter = [{'label': str(option), 'value': option} for option in lcolinter]

# Card for interrogative
card_inter = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-question fa-3x", style={'color': 'grey'}), ' ',
             'INTERROGATIVE CHALLENGE    .', html.I(className="fas fa-question fa-3x", style={'color': 'grey'})],
            className="class-subtitle"
        ),
        dbc.CardBody(
            [
                html.H4('CHOOSE A QUESTION WORD', className="card-title"),
                dcc.Dropdown(loptionsinter, value='all', id='mydropinter'),
                html.Div(id='container-button-timestamp0inter'),
                html.P('click button', className="card-text mt-2"),
                dbc.Button('ANSWER', id='btn-nclicksinter-1', n_clicks=0, color="info", className="me-1"),
                html.Div(id='container-button-timestampinter'),
                dbc.Button('QUESTION', id='btn-nclicksinter-2', n_clicks=0, color="primary", className="me-1"),
                html.Div(id='container-button-timestamp2inter'),
            ],
        )
    ],
    color="danger",
    outline=True,
    style=card_style
)

app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab(
            label='Translation Warm-Up', children=[
            dbc.Row([
                dbc.Col(card_warm, width={'size': 12})
            ], justify='center', align='center')
            ],
            selected_style={
                'backgroundColor': '#d9534f',
                'color': 'white',
                'fontWeight': 'bold',
                'padding': '5px',
                'border': '2px solid #d9534f',
                'borderRadius': '10px'
            },
            style={'backgroundColor': '#f5f5f5',
                'color': 'black',
                'padding': '5px',
                'border': '2px solid #d9534f',
                'borderRadius': '10px'}
        ),
        dcc.Tab(label='Reported Speech', children=[
            dbc.Row([
                dbc.Col(card_rep, width={'size': 12})
            ], justify='center', align='center')
        ],selected_style={
                'backgroundColor': '#d9534f',
                'color': 'white',
                'fontWeight': 'bold',
                'padding': '5px',
                'border': '2px solid #d9534f',
                'borderRadius': '10px'
            },
            style={'backgroundColor': '#f5f5f5',
                'color': 'black',
                'padding': '5px',
                'border': '2px solid #d9534f',
                'borderRadius': '10px'}),
        dcc.Tab(label='Interrogative Challenge', children=[
            dbc.Row([
                dbc.Col(card_inter, width={'size': 12})
            ], justify='center', align='center')
        ],selected_style={
                'backgroundColor': '#d9534f',
                'color': 'white',
                'fontWeight': 'bold',
                'padding': '5px',
                'border': '2px solid #d9534f',
                'borderRadius': '10px'
            },
            style={'backgroundColor': '#f5f5f5',
                'color': 'black',
                'padding': '5px',
                'border': '2px solid #d9534f',
                'borderRadius': '10px'}),
        dcc.Tab(label='Describe the Pictures', children=[
            dbc.Row([
                dbc.Col(card_pic, width={'size': 12})
            ], justify='center', align='center')
        ],selected_style={
                'backgroundColor': '#d9534f',
                'color': 'white',
                'fontWeight': 'bold',
                'padding': '5px',
                'border': '2px solid #d9534f',
                'borderRadius': '10px'
            },
            style={'backgroundColor': '#f5f5f5',
                'color': 'black',
                'padding': '5px',
                'border': '2px solid #d9534f',
                'borderRadius': '10px'})
    ]),
    dcc.Store(id="didfthe-stored", data=[]),
    dcc.Store(id="diordenadatoday-stored", data=[]),
    dcc.Store(id="didfreport-stored", data=[]),
    dcc.Store(id="diordenadarep-stored", data=[]),
    dcc.Store(id="diordenadatodaypic-stored", data=[]),
    dcc.Store(id="didfpic", data=didfpic),
    dcc.Store(id="didfinter-stored", data=[]),
    dcc.Store(id="diordenadatodayinter-stored", data=[]),
    dcc.Store(id="dirow", data=[]),
], fluid=True)

# callbacks for the warm up
@app.callback(
    [Output('container-button-timestamp0', 'children'),
     Output("didfthe-stored", 'data')],
    [Input('mydrop', 'value')],
    # prevent_initial_call=True
)
def update_output(selected_options):
    if 'all' in selected_options:
        msg = 'You have selected: All option'
        didfthe = dfthe.to_dict('records')
        return html.Div(msg), didfthe
    else:
        msg = f'You have selected: {selected_options}'
        dffiltrada = dfthe.loc[dfthe['structure'] == selected_options]
        didfthe = dffiltrada.to_dict('records')
        return html.Div(msg), didfthe


@app.callback(
    [Output('container-button-timestamp', 'children'),
     Output('diordenadatoday-stored', 'data'),
     Output('container-button-timestamp2', 'children')],
    Output('tts-audio', 'src'),
    [Input('btn-nclicks-1', 'n_clicks'),
     Input('btn-nclicks-2', 'n_clicks')],
    [State("didfthe-stored", 'data'),
     State('diordenadatoday-stored', 'data')],
    prevent_initial_call=True
)
def display_sentence(btn1, btn2, didfthe, diordenadatoday):
    ctx = callback_context
    if not ctx.triggered:
        return html.Div(), [], ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-nclicks-1":
        dfthe = pd.DataFrame(didfthe)
        randomn = random.choice(list(dfthe.index))
        row = dfthe.iloc[[randomn]]
        esp = row.loc[:, 'esp']
        msg = esp
        diordenadatoday = row.to_dict('records')
        return html.Div(msg), diordenadatoday, "",""

    elif button_id == "btn-nclicks-2":
        row = pd.DataFrame(diordenadatoday)
        eng = row.loc[:, 'eng']
        speech_text = eng[0]
        print(speech_text)

        # Convert text to speech using gTTS
        tts = gTTS(text=speech_text, lang='en',tld='ca')

        # Save the audio to a bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)

        # Encode the audio in base64
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')

        # Create a data URI for the audio
        audio_src = f"data:audio/mp3;base64,{audio_base64}"
        return no_update, diordenadatoday, html.Div(eng), audio_src

    return html.Div(), [], "",""


# @app.callback(
#     Output('tts-audio', 'src'),
#     Input('btn-tts', 'n_clicks'),
#     State('container-button-timestamp2', 'children')
# )
# def text_to_speech(n_clicks, text):
#     if n_clicks == 0 or not text:
#         raise PreventUpdate
#
#     # Extract text from the Div component
#     speech_text = text['props']['children'][0]
#     print(speech_text)
#
#     # Convert text to speech using gTTS
#     tts = gTTS(text=speech_text, lang='en')
#
#     # Save the audio to a bytes buffer
#     audio_buffer = io.BytesIO()
#     tts.write_to_fp(audio_buffer)
#
#     # Encode the audio in base64
#     audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
#
#     # Create a data URI for the audio
#     audio_src = f"data:audio/mp3;base64,{audio_base64}"
#
#     return audio_src
# callbacks for the reported speech
@app.callback(
    [Output('container-button-timestamp0rep', 'children'),
     Output("didfreport-stored", 'data')],
    [Input('mydroprep', 'value')],
    # prevent_initial_call=True
)
def update_output(selected_options):
    # if 'all' in selected_options:
    #     msg = 'You have selected: All option'
    #     didfreport = dfreport.to_dict('records')
    #     return html.Div(msg), didfreport
    # else:
        msg = f'You have selected: {selected_options}'
        dffiltrada = dfreport.loc[dfreport['story'] == selected_options]
        didfreport = dffiltrada.to_dict('records')
        return html.Div(msg), didfreport


@app.callback(
    [Output('container-button-timestamprep', 'children'),
     Output('diordenadarep-stored', 'data'),
     Output('dirow', 'data')],
    [Input('btn-nclicksrep-1', 'n_clicks')],
    [State("didfreport-stored", 'data'),
     State("diordenadarep-stored", 'data')],
    prevent_initial_call=True
)
def displayClick(btn1, didfreport,diordenadarep):
    msg = "pulsa boton para una frase"

    if "btn-nclicksrep-1" in callback_context.triggered_id:
        dfreport = pd.DataFrame(didfreport)
        diordenadarep = diordenadarep or {'last_index': -1}  # Initialize state if not present
        last_index = diordenadarep.get('last_index', -1)  # Get last selected index
        if last_index + 1 >= len(dfreport):
            # Reset index if we reach the end
            last_index = -1
        next_index = last_index + 1
        row = dfreport.iloc[[next_index]]
        direct = row.loc[:, 'direct']
        msg = direct
        diordenadarep = {'last_index': next_index}  # Update state with new index
        last_index = diordenadarep['last_index']
        row = dfreport.iloc[[last_index]]
        dirow = row.to_dict('records')
        return html.Div(msg), diordenadarep, dirow


@app.callback(
    Output('container-button-timestamp2rep', 'children'),
    [Input('btn-nclicksrep-2', 'n_clicks')],
    [State('dirow', 'data')],
    prevent_initial_call=True
)
def displayClick2(btn2, dirow):
    msg = "pulsa boton para obtener solución"
    if "btn-nclicksrep-2" in callback_context.triggered_id:
        row = pd.DataFrame(dirow)
        reported = row.loc[:,'reported']
        msg = reported

    return html.Div(msg)

# callbacks for the interrogative
@app.callback(
    [Output('container-button-timestamp0inter', 'children'),
     Output("didfinter-stored", 'data')],
    [Input('mydropinter', 'value')],
    # prevent_initial_call=True
)
def update_output(selected_options):
    if 'all' in selected_options:
        msg = 'You have selected: All option'
        didfinter = dfinter.to_dict('records')
        return html.Div(msg), didfinter
    else:
        msg = f'You have selected: {selected_options}'
        dffiltrada = dfinter.loc[dfinter['word'] == selected_options]
        didfinter = dffiltrada.to_dict('records')
        return html.Div(msg), didfinter


@app.callback(
    [Output('container-button-timestampinter', 'children'),
     Output('diordenadatodayinter-stored', 'data'),
     Output('container-button-timestamp2inter', 'children')],
    [Input('btn-nclicksinter-1', 'n_clicks'),
     Input('btn-nclicksinter-2', 'n_clicks')],
    [State("didfinter-stored", 'data'),
     State('diordenadatodayinter-stored', 'data')],
    prevent_initial_call=True
)
def display_sentence(btn1, btn2, didfinter, diordenadatodayinter):
    ctx = callback_context
    if not ctx.triggered:
        return html.Div(), [], ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-nclicksinter-1":
        dfinter = pd.DataFrame(didfinter)
        randomn = random.choice(list(dfinter.index))
        row = dfinter.iloc[[randomn]]
        ans = row.loc[:, 'answer']
        msg = ans
        diordenadatodayinter = row.to_dict('records')
        return html.Div(msg), diordenadatodayinter, ""

    elif button_id == "btn-nclicksinter-2":
        row = pd.DataFrame(diordenadatodayinter)
        que = row.loc[:, 'question']
        return no_update, diordenadatodayinter, html.Div(que)

    return html.Div(), [], ""



# callback for the pictures
@app.callback(
    [Output('container-button-timestamppic', 'children'),
    Output('diordenadatodaypic-stored', 'data'),
     Output('container-button-timestamp2pic', 'children')],
    [Input('btn-nclickspic-1', 'n_clicks'),
     Input('btn-nclickspic-2', 'n_clicks')],
    [State("didfpic", 'data')],
    [State("diordenadatodaypic-stored", 'data')],
    prevent_initial_call=True
)
def display_sentence(btn1, btn2, didfpic,diordenadatodaypic):
    ctx = callback_context
    if not ctx.triggered:
        return html.Div(), [], ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-nclickspic-1":
        dfpic = pd.DataFrame(didfpic)
        randomn = random.choice(list(dfpic.index))
        row = dfpic.iloc[[randomn]]
        pic = list(row.loc[:, 'name'])[0]
        msg = pic
        diordenadatodaypic = row.to_dict('records')
        return html.Img(src="/assets/{}".format(msg), style={'width': '40%', 'max-width': '600px', 'margin': 'auto'}), diordenadatodaypic, ""

    elif button_id == "btn-nclickspic-2":
        row = pd.DataFrame(diordenadatodaypic)
        eng = row.loc[:, 'eng']
        return no_update, diordenadatodaypic, html.Div(eng)

    return html.Div(), [], ""



if __name__ == '__main__':
    app.run_server(debug=True,port =871)
