from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = [
    html.H1(children="My First Dash Application", className = "text-warning fst-italic pt-5"),
    html.Br(),
    html.Span("This is my first paragraph", className="parapraph-style"),
    html.H2(children="H2 Heading", className = "header-style"),
    html.H3(children="H3 Heading", className = "header-style"),
    html.Footer(children = "Link to Flask", className = "other-style"),
    html.H4(children="H4 Heading")
]

if __name__ == '__main__':
    app.run(debug = True, use_reloader = True)