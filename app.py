import dash
from dash import Dash, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP] + dmc.styles.ALL, use_pages=True)
server = app.server

sidebar = dbc.Col(
    children = [
        dmc.Flex(
            [
                dmc.Button(
                    dcc.Link(
                        f"{page['name']}",
                        href=page["relative_path"],
                        className = "link-underline-opacity-0 link-info")
                ) for page in dash.page_registry.values()
            ],
            direction={"base": "column"},
            gap={"base": "sm"}
        )
    ],
    class_name = "bg-success min-vh-100",
    width = 2
)

charts = dbc.Col(
    dash.page_container
)

app.layout = dmc.MantineProvider(
    dbc.Container(
        children = [
            dbc.Row(
                children = [
                    sidebar,
                    charts
                ]
            )
        ],
        class_name = "bg-black min-vh-100",
        fluid = True
    )
)

if __name__ == '__main__':
    app.run_server(debug = False, use_reloader = True)