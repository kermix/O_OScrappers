from re import I
from dash import dcc, html, Input, Output, State, callback, clientside_callback
import dash_bootstrap_components as dbc

from scrappers import paa

from exceptions.scrapper import NoResultError, ElementIsNotPaaQuestionError, SearchInitError


layout = html.Div([
    dbc.Row([
        html.H3('People also ask'),
        dcc.Link('Go to main menu', href='/'),
    ], className="mb-5"),
    dbc.Row([
        dbc.Col(html.Div(
            [
                dbc.Label("Query"),
                dbc.Input(id="input_query",
                          placeholder="Input goes here...", type="text"),
                dbc.FormText("Typ something you want to search for above"),
            ]
        ), width=10),
        dbc.Col(html.Div(
            [
                dbc.Label("Language"),
                dbc.Select(
                    id="select_language",
                    options=[
                        {"label": "PL", "value": "pl"},
                        {"label": "EN", "value": "en"},
                        {"label": "DE", "value": "de"},
                    ],
                    value="en"
                ),
                dbc.FormText("Choose the language for the search"),
            ]
        ), width=2, className="mb-2"),
    ]),
    dbc.Row([
        html.Div(
            [
                dbc.Button("Search", id="button_search", color="primary"),
            ],
            className="d-grid gap-2 mb-2",
        ),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Loading(id="ls-loading-1", children=[
                dbc.Textarea(id="paa_questions_textarea",
                             placeholder="Results...", readonly=True, className="mb-3"),
                dcc.Clipboard(
                    target_id="paa_questions_textarea",
                    title="copy",
                    style={
                        "display": "inline-block",
                        "fontSize": 20,
                        "verticalAlign": "top",
                        "position": "absolute",
                        "top": 0,
                        "right": "20px",
                    },
                ),
            ], type="default"),

        ], class_name="position-relative"),
    ]),

])


@callback(
    Output('paa_questions_textarea', 'value'),
    Input('input_query', 'n_submit'),
    Input('button_search', 'n_clicks'),
    State('input_query', 'value'),
    State('select_language', 'value'))
def display_value(n_clicks, n_submit, query, lang):
    if not n_clicks and not n_submit:
        return ""

    if not query or not lang:
        return "Query and language have to be specified."

    try:    
        paa_search = paa.PaaSearch(lang=lang)
        paa_search.search(query=query)
        paa_search.expand()
        questions = paa_search.get_questions()
    except (NoResultError, ElementIsNotPaaQuestionError, SearchInitError) as ex:
        return str(f"Error: {ex}")

    return "\n\n".join(questions)


clientside_callback(
    """
    function(value) {
        return value.split(/\\r\\n|\\r|\\n/).length;
    }
    """,
    Output("paa_questions_textarea", "rows"),
    Input('paa_questions_textarea', 'value'),
)
