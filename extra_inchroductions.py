import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import Flask

import os
import numpy as np
import math

import extra_inch_markov as mm
import extra_inch_grammar as cfg

server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

models = [
    {"label": "Context-Free Grammar", "value": "CFG"},
    {"label": "Markov Chain", "value": "MC"}
]

app.layout = dbc.Container(children=[
    html.Div(children=[
        html.H3("I'm joined by my sidekick and best friend Bardi, and..."),
        html.Div(id="opening")
    ], style={"padding":"50px","text-align":"center"}),
    html.Div(children=[
        dcc.Dropdown(
            id="model-choice",
            options=models,
            style={"width":"70%","margin":"auto"}
        ),
        html.Button('Generate', id="generate", n_clicks=0, disabled=True),
    ], style={"text-align":"center"}),
    html.Div(id="explanation", style={"padding":"20px"})
])

@app.callback(
    [dash.dependencies.Output("explanation","children"),
     dash.dependencies.Output("generate","disabled")],
    [dash.dependencies.Input("model-choice", "value")]
)
def choose_model(value) :
    if value=="MC" :
        div = html.Div( children=[
            html.H3("Markov Chain", style={'display':'none'}),
            html.H5("A Markov Chain is a simple way to generate text. I collected every introduction from The Extra Inch, and determined the probability of the the next letter in a sentence, given the previous 5. I then used this probabilistic model to generate new sentences. It has no understanding of words, or parts of speech or anything, so you'll see the output often doesn't make a whole lot of sense.")
        ])
    elif value=="CFG" :
        div = html.Div( children=[
            html.H3("Context-Free Grammar", style={'display':'none'}),
            html.H5("This doesn't use any statistics or machine learning at all. After I collected all the introductions from The Extra Inch, I made lists of the nouns, verbs, adjectives, adverbs, etc., and I made two template sentences. This simply generates a random sentence using the templates, and the lists of parts of speech.")
        ])
    else :
        div = html.Div( children=[
            html.H3("Oops! Something went wrong."),
            html.H5("It looks like you somehow selected a menu item that broke everything. It was: " + value)
        ])
    return div, False

@app.callback(
    dash.dependencies.Output("opening", "children"),
    [dash.dependencies.Input("generate", "n_clicks"),
     dash.dependencies.Input("explanation", "children")]
)
def choose_model(n_clicks, children):
    if n_clicks > 0 : # and also something is chosen on the list
        model = children['props']['children'][0]['props']['children']
        if model == "Markov Chain" :
            generated_text = mm.get_n_introductions(1)
            return html.H3(generated_text)
        elif model == "Context-Free Grammar" :
            generated_text = cfg.get_n_introductions(1)
            return html.H3(generated_text)
        else :
            return "Sorry, something went wrong!"
    else :
        return html.H3("")

if __name__ == '__main__' :
    app.run_server()
