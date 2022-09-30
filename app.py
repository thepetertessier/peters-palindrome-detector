# Visit http://127.0.0.1:8050/ when running locally

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

# Variables
tabtitle = 'palindrome detector'
githublink = 'https://github.com/thepetertessier/peters-palindrome-detector'
mywebsitelink = 'https://petertessier.com'
starting_text = 'Was it a cat I saw?'
image_options = ['assets/palindrome-definition.png','assets/palindrome-definition-1.png','assets/palindrome-definition-2.png']
image = image_options[1]

# Helper functions
def clean_text(text, case_sens, space_sens, punc_sens):
    # Modify text according to checked parameters
    punctuation_chars = '''!()-[]{};:'"\,<>./?@#$%^&*_~–—…|+='''
    if not case_sens:
        text = text.lower()
    if not space_sens:
        text = text.replace(' ', '')
    if not punc_sens:
        for char in punctuation_chars:
            text = text.replace(char, '')
    return text

def palindrome_test(text, case_sens, space_sens, punc_sens):
    # Logic for testing if palindrome
    text = clean_text(text, case_sens, space_sens, punc_sens)
    for i, letter in enumerate(text[:(len(text)//2)]):
        if letter != text[-i - 1]:
            return False
    return True

# Initiate app
app = Dash(__name__)
server = app.server
app.title = tabtitle

colors = {
    'background': 'white',
    'theme': '#388ec7'
}

app.layout = html.Div([
    html.H1(
        children='Palindrome Detector',
        style={
            'color': colors['theme']
        }
    ),
    html.Img(src=image, height=140),
    html.Div(children=[
        html.H6('Enter text here (example given):'),
        dcc.Input(id='input_text', value=starting_text, type='text', style={'width':350}),
        html.Br(),
        html.Br(),
        html.H6('Should the detection be...'),
        dcc.Checklist(['case sensitive?', 'space sensitive?', 'punctuation sensitive?'],
                       value=[],
                       id='sensitivities'),
        html.Br(),
        html.Div(id='output-div', style={'font-weight':'bold', 'font-size':'20px'}),
        html.Br(),
        html.Br(),
        html.A('Code on GitHub', href=githublink),
        html.Br(),
        html.A('About me', href=mywebsitelink)
    ])
], style={'textAlign': 'center', 'backgroundColor': colors['background']})

# If the button is clicked, detect if the inputted text is a palindrome
@app.callback(
    Output('output-div','children'),
    Input('input_text', 'value'),
    Input('sensitivities', 'value'),
)
def say_if_its_palindrome(input_text, sensitivities):
    if input_text == '':
        return html.Br()
    if palindrome_test(input_text,
                       'case sensitive?' in sensitivities,
                       'space sensitive?' in sensitivities,
                       'punctuation sensitive?' in sensitivities):
        return 'It\'s a palindrome!'
    return 'It\'s not a palindrome.'


if __name__ == '__main__':
    app.run_server(debug=True)
