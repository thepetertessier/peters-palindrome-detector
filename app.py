# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

# Variables
tabtitle = 'palindrome detector'
githublink = 'https://github.com/thepetertessier/peters-palindrome-detector'
mywebsitelink = 'https://google.com'

# Helper functions
def clean_text(text, case_sens, space_sens, punc_sens):
    punctuation_chars = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    if not case_sens:
        text = text.lower()
    if not space_sens:
        text = text.replace(' ', '')
    if not punc_sens:
        for char in punctuation_chars:
            text = text.replace(char, '')
    return text

def palindrome_test(text, case_sens, space_sens, punc_sens):
    text = clean_text(text, case_sens, space_sens, punc_sens)
    for i, letter in enumerate(text[:(len(text)//2)]):
        if letter != text[-i - 1]:
            return False
    return True

# Initiate app
app = Dash(__name__)
server = app.server
app.title=tabtitle

colors = {
    'background': '#111111',
    'theme': '#388ec7'
}

app.layout = html.Div([
    html.H1(
        children='Palindrome Detector',
        style={
            'textAlign': 'center',
            'color': colors['theme']
        }
    ),

    html.Div(children=[
        html.H6('Parameters:',style={"size":25}),
        dcc.Checklist(['case sensitive?', 'space sensitive?', 'punctuation sensitive?'],
                       value=[],
                       id='sensitivities'),

        html.Br(),

        dcc.Input(id='input_text', value='kayak', type='text'),
        html.Button(children='Go!', id='go_button', n_clicks=0,
                    style={
                    'background-color': colors['theme'],
                    'color': 'white',
                    'margin-left': '5px',
                    'verticalAlign': 'center',
                    'horizontalAlign': 'center'}
                    ),
        html.Br(),
        html.Br(),
        html.Div(id='output-div'),

        html.Br(),
        html.Br(),
        html.A('Code on GitHub', href=githublink),
        html.Br(),
        html.A('About me', href=mywebsitelink)
    ])
], style={'textAlign': 'center', 'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output('output-div','children'),
    Input('go_button', 'n_clicks'),
    State('sensitivities', 'value'),
    State('input_text', 'value')
)
def say_if_its_palindrome(clicks, sensitivities, input_text):
    if clicks == 0:
        return 'Waiting for input...'
    if palindrome_test(input_text,
                       'case sensitive?' in sensitivities,
                       'space sensitive?' in sensitivities,
                       'punctuation sensitive?' in sensitivities):
        return 'It is a palindrome!'
    return 'It is not a palindrome.'


if __name__ == '__main__':
    app.run_server(debug=True)
