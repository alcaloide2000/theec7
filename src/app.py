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
dfthe = dithe['warm'] # take the warm sheet excell
lcol = dfthe['structure'].unique() #list of the structures
loptions = [{'label': str(option), 'value': option} for option in lcol] # list of options for the dropdown

# styly of the cards
card_style = {"width": "100%",
              "margin": "auto",
              "padding": "10px",
              "borderColor": "#d9534f",
              "borderWidth": "2px"}
# Card for the warm-up
card_warm = dbc.Card(
    [
        html.H6(
            [
            html.I(className="fas fa-running fa-3x", style={'color': 'grey'}), ' ',
             'TRANSLATION WARM-UP    .',
            html.I(className="fas fa-running fa-3x", style={'color': 'grey'})
            ],
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
                html.Audio(id='tts-audiowarm', controls=True, style={'width': '100%'})
            ],
        )
    ],
    style=card_style
)
# Data for the reported speech
dfreport = dithe['reportedsp']
lcolrep = dfreport['story'].unique()
loptionsrep = [{'label': str(option), 'value': option} for option in lcolrep]

# Card for the reported
card_rep = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-comments fa-3x", style={'color': 'grey'}),
             ' ',
             'REPORTED SPEECH     .',
             html.I(className="fas fa-comments fa-3x", style={'color': 'grey'})
             ],
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
                html.Audio(id='tts-audiorep', controls=True, style={'width': '100%'})
            ],
        )
    ],
    style=card_style
)
# Data for the pictures
dfpic = dithe['pictures']
didfpic = dfpic.to_dict('records')
# Card for the pictures
card_pic = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-camera fa-3x", style={'color': 'grey'}),
             ' ',
             'DESCRIBE THE PICTURES',
             html.I(className="fas fa-camera fa-3x", style={'color': 'grey'})],
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
                html.Audio(id='tts-audiopic', controls=True, style={'width': '100%'})
            ],
        )
    ],
    style=card_style
)
# Data for the interrogative challenge
dfinter = dithe['question']
lcolinter = dfinter['word'].unique()
loptionsinter = [{'label': str(option), 'value': option} for option in lcolinter]
# Card for interrogative
card_inter = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-question fa-3x", style={'color': 'grey'}),
             ' ',
             'INTERROGATIVE CHALLENGE    .',
             html.I(className="fas fa-question fa-3x", style={'color': 'grey'})
             ],
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
                html.Audio(id='tts-audiointer', controls=True, style={'width': '100%'})
            ],
        )
    ],
    style=card_style
)

# Data for the question tag
dftag = dithe['tags']
didftag = dftag.to_dict('records')
# Card for the pictures
card_tag = dbc.Card(
    [
        html.H6(
            [html.I(className="fas fa-camera fa-3x", style={'color': 'grey'}),
             ' ',
             'GUESS THE QUESTION TAG',
             html.I(className="fas fa-camera fa-3x", style={'color': 'grey'})],
             className="class-subtitle"
        ),
        dbc.CardBody(
            [
                html.H4('CHOOSE A SENTENCE', className="card-title"),
                html.P('click button', className="card-text mt-2"),
                dbc.Button('SENTENCE', id='btn-nclickstag-1', n_clicks=0, color="info", className="me-1"),
                html.Div(id='container-button-timestamptag'),
                dbc.Button('TAG', id='btn-nclickstag-2', n_clicks=0, color="primary", className="me-1"),
                html.Div(id='container-button-timestamp2tag'),
                html.Audio(id='tts-audiotag', controls=True, style={'width': '100%'})
            ],
        )
    ],
    style=card_style
)

app.layout = dbc.Container([
    dcc.Tabs(
        [
        dcc.Tab(
            label='Translation Warm-Up',
            children=[dbc.Row([
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
                'borderRadius': '10px'}),
            dcc.Tab(label='Question tags', children=[
                dbc.Row([
                    dbc.Col(card_tag, width={'size': 12})
                ], justify='center', align='center')
            ], selected_style={
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
    ]),
    dcc.Store(id="didfthe-stored", data=[]),
    dcc.Store(id="diordenadatoday-stored", data=[]),
    dcc.Store(id="didfreport-stored", data=[]),
    dcc.Store(id="diordenadarep-stored", data=[]),
    dcc.Store(id="diordenadatodaypic-stored", data=[]),
    dcc.Store(id="didfpic", data=didfpic),
    dcc.Store(id="didfinter-stored", data=[]),
    dcc.Store(id="diordenadatodayinter-stored", data=[]),
    dcc.Store(id="diordenadatodaytag-stored", data=[]),
    dcc.Store(id="didftag", data=didftag),
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
    Output('tts-audiowarm', 'src'),
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
# callbacks for reported
# select an option
@app.callback(
    [Output('container-button-timestamp0rep', 'children'),
     Output("didfreport-stored", 'data')],
    [Input('mydroprep', 'value')],
    # prevent_initial_call=True
)
def update_output(selected_options):
        msg = f'You have selected: {selected_options}'
        dffiltrada = dfreport.loc[dfreport['story'] == selected_options]
        didfreport = dffiltrada.to_dict('records')
        return html.Div(msg), didfreport

@app.callback(
    [Output('container-button-timestamprep', 'children'),
     Output('diordenadarep-stored', 'data'),
     Output('container-button-timestamp2rep', 'children')],
    Output('tts-audiorep', 'src'),
    [Input('btn-nclicksrep-1', 'n_clicks'),
     Input('btn-nclicksrep-2', 'n_clicks')],
    [State("didfreport-stored", 'data'),
     State('diordenadarep-stored', 'data')],
    prevent_initial_call=True
)
def display_sentence(btn1, btn2, didfreport, diordenadarep):
    ctx = callback_context
    if not ctx.triggered:
        return html.Div(), [], "", ""
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if didfreport is None:
        return html.Div("No data available"), [], "", ""

    dfreport = pd.DataFrame(didfreport)
    diordenadarep = diordenadarep or {'last_index': -1}  # Initialize state if not present
    last_index = diordenadarep.get('last_index', -1)  # Get last selected index

    if button_id == "btn-nclicksrep-1":
        if last_index + 1 >= len(dfreport):
            last_index = -1  # Reset index if we reach the end
        next_index = last_index + 1
        row = dfreport.iloc[next_index]
        direct = row['direct']
        msg = direct
        speech_text = direct
        nameless = speech_text.split(":", 1)[1].strip()

        # Convert text to speech using gTTS
        tts = gTTS(text=nameless, lang='en', tld='ca')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        audiodir_src = f"data:audio/mp3;base64,{audio_base64}"

        diordenadarep = {'last_index': next_index}  # Update state with new index
        return html.Div(msg), diordenadarep, "", audiodir_src

    elif button_id == "btn-nclicksrep-2":
        if last_index < 0:
            return html.Div("No previous sentence available"), diordenadarep, "", ""

        row = dfreport.iloc[last_index]
        reported = row['reported']
        msg = reported
        speech_text = reported

        # Convert text to speech using gTTS
        tts = gTTS(text=speech_text, lang='en', tld='ca')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        audiorep_src = f"data:audio/mp3;base64,{audio_base64}"

        return "", diordenadarep, html.Div(msg), audiorep_src

    return html.Div(), [], "", ""

# callbacks for the interrogative
#select question type
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

# anwer question
@app.callback(
    [Output('container-button-timestampinter', 'children'),
     Output('diordenadatodayinter-stored', 'data'),
     Output('container-button-timestamp2inter', 'children')],
    Output('tts-audiointer', 'src'),
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
        speech_text = ans.iloc[0]

        # Convert text to speech using gTTS
        tts = gTTS(text=speech_text, lang='en', tld='ca')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        audioans_src = f"data:audio/mp3;base64,{audio_base64}"
        diordenadatodayinter = row.to_dict('records')
        return html.Div(msg), diordenadatodayinter, "",audioans_src

    elif button_id == "btn-nclicksinter-2":
        row = pd.DataFrame(diordenadatodayinter)
        que = row.loc[:, 'question']
        speech_text = que.iloc[0]
        # Convert text to speech using gTTS
        tts = gTTS(text=speech_text, lang='en', tld='ca')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        audioque_src = f"data:audio/mp3;base64,{audio_base64}"
        return no_update, diordenadatodayinter, html.Div(que),audioque_src

    return html.Div(), [], ""," "



# callback for the pictures
@app.callback(
    [Output('container-button-timestamppic', 'children'),
    Output('diordenadatodaypic-stored', 'data'),
     Output('container-button-timestamp2pic', 'children')],
    Output('tts-audiopic', 'src'),
    [Input('btn-nclickspic-1', 'n_clicks'),
     Input('btn-nclickspic-2', 'n_clicks')],
    [State("didfpic", 'data')],
    [State("diordenadatodaypic-stored", 'data')],
    prevent_initial_call=True
)
def display_sentence(btn1, btn2, didfpic,diordenadatodaypic):
    ctx = callback_context
    if not ctx.triggered:
        return html.Div(), [], "" ,""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-nclickspic-1":
        dfpic = pd.DataFrame(didfpic)
        randomn = random.choice(list(dfpic.index))
        row = dfpic.iloc[[randomn]]
        pic = list(row.loc[:, 'name'])[0]
        msg = pic
        diordenadatodaypic = row.to_dict('records')
        return html.Img(src="/assets/{}".format(msg), style={'width': '40%', 'max-width': '600px', 'margin': 'auto'}), diordenadatodaypic, "",""

    elif button_id == "btn-nclickspic-2":
        row = pd.DataFrame(diordenadatodaypic)
        eng = row.loc[:, 'eng']
        speech_text = eng.iloc[0]
        # Convert text to speech using gTTS
        tts = gTTS(text=speech_text, lang='en', tld='ca')
        # Save the audio to a bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        # Encode the audio in base64
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        # Create a data URI for the audio
        audiopic_src = f"data:audio/mp3;base64,{audio_base64}"
        return no_update, diordenadatodaypic, html.Div(eng), audiopic_src

    return html.Div(), [], "",""

# callback for the tag
@app.callback(
    [Output('container-button-timestamptag', 'children'),
    Output('diordenadatodaytag-stored', 'data'),
     Output('container-button-timestamp2tag', 'children')],
    Output('tts-audiotag', 'src'),
    [Input('btn-nclickstag-1', 'n_clicks'),
     Input('btn-nclickstag-2', 'n_clicks')],
    [State("didftag", 'data')],
    [State("diordenadatodaytag-stored", 'data')],
    prevent_initial_call=True
)
def display_sentence(btn1, btn2, didftag,diordenadatodaytag):
    ctx = callback_context
    if not ctx.triggered:
        return html.Div(), [], "" ,""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-nclickstag-1":
        dftag = pd.DataFrame(didftag)
        randomn = random.choice(list(dftag.index))
        row = dftag.iloc[[randomn]]
        sen = list(row.loc[:, 'sentence'])[0]
        msg = sen
        diordenadatodaytag = row.to_dict('records')
        return html.Div(msg), diordenadatodaytag, "",""

    elif button_id == "btn-nclickstag-2":
        row = pd.DataFrame(diordenadatodaytag)
        tag = row.loc[:, 'tag']
        speech_text = tag.iloc[0]
        # Convert text to speech using gTTS
        tts = gTTS(text=speech_text, lang='en', tld='ca')
        # Save the audio to a bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        # Encode the audio in base64
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        # Create a data URI for the audio
        audiopic_src = f"data:audio/mp3;base64,{audio_base64}"
        return no_update, diordenadatodaytag, html.Div(tag), audiopic_src

    return html.Div(), [], "",""

if __name__ == '__main__':
    app.run_server(debug=True,port =871)
