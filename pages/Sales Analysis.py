import pandas as pd
from dash import dcc, _dash_renderer
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dash_table
import dash_ag_grid as dag

superstore = pd.read_excel("data/1. Superstore Dataset.xlsx")
superstore['Order Date'] = pd.to_datetime(superstore['Order Date'], format = "%m/%d/%Y")

_dash_renderer._set_react_version("18.2.0")

dash.register_page(__name__, path = "/salesanalysis")

# Creating first chart

categorysales = superstore.groupby('Category')['Sales'].sum().reset_index()

categorysalesdistribution = px.pie(categorysales, names = "Category", values = "Sales", hole = 0.7, color_discrete_sequence = px.colors.qualitative.Dark24_r)

categorysalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", legend_font_color = "white")

totalsales = '${:,}'.format(round(categorysales['Sales'].sum(), 2))

categorysalesdistribution.add_annotation(text = "Total Sales by Category", showarrow = False, font = dict(color = "white", size = 14), y = 0.55)
categorysalesdistribution.add_annotation(text = totalsales, showarrow = False, font = dict(color = "white", size = 14), y = 0.45)

# Creating second chart
segmentsales = superstore.groupby('Segment')['Sales'].sum().reset_index()

segmentsalesdistribution = px.pie(segmentsales, names = "Segment", values = "Sales", hole = 0.7, color_discrete_sequence = px.colors.qualitative.Dark24_r)

segmentsalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", legend_font_color = "white")

segmentsalesdistribution.add_annotation(text = "Total Sales by Segment", showarrow = False, font = dict(color = "white", size = 14), y = 0.55)
segmentsalesdistribution.add_annotation(text = totalsales, showarrow = False, font = dict(color = "white", size = 14), y = 0.45)

# Creating our third chart
segmentcategorysales = superstore.groupby(['Segment', 'Category', 'Sub-Category'])['Sales'].sum().reset_index()

segmentcategorysalesdistribution = px.sunburst(segmentcategorysales, path = ['Segment', 'Category', 'Sub-Category'], values= "Sales", color_discrete_sequence = px.colors.qualitative.Dark24_r)

segmentcategorysalesdistribution.update_layout(title = "Categories and Sub-Categories Sales by Segment",
                                              title_font_color = 'White',
                                              paper_bgcolor = 'rgba(0,0,0,0)')

segmentcategorysalesdistribution.update_traces(marker_colors = px.colors.qualitative.Dark24_r)

# Creating out products data table
productstable = dash_table.DataTable(
                            superstore.to_dict('records'),
                            columns = [
                                {"name" : "Product ID", "id" : "Product ID"},
                                {"name" : "Product Name", "id" : "Product Name"},
                                {"name" : "Category", "id" : "Category"},
                                {"name" : "Sub-Category", "id" : "Sub-Category"},
                                {"name" : "Profit", "id" : "Profit"},
                            ],
                            page_size = 10,
                            style_table={
                                'height': 'auto',
                                'overflowY': 'auto'
                            },
                            fixed_rows={'headers': True},
                        )

# Creating our products dash ag grid table
column_names = [
    {'field' : 'Product ID'},
    {'field' : 'Product Name', "filter": "agTextColumnFilter",},
    {'field' : 'Category'},
    {'field' : 'Sub-Category', "filter" : True},
    {'field' : 'Profit', "filter": "agNumberColumnFilter"},
]

products_ag_grid_table = dag.AgGrid(
    rowData=superstore.to_dict("records"),
    columnDefs=column_names,
    className = "ag-theme-alpine-dark",
    dashGridOptions = {
        "pagination" : True
    }
)

charts = dbc.Container(
            children = [
                dbc.Row(
                    dmc.Text("Sales Made Analysis", size="xl", c = "white", style={"fontSize": 40})
                ),
                dbc.Row(
                    children = [
                        dbc.Col(
                            dcc.Graph(figure = categorysalesdistribution, responsive = True)
                        ),
                        dbc.Col(
                            dcc.Graph(figure = segmentsalesdistribution, responsive = True)
                        ),
                        dbc.Col(
                            dcc.Graph(figure = segmentcategorysalesdistribution, responsive = True)
                        )
                    ]
                ),
                dbc.Row(
                    children = [
                        dbc.Col(
                            productstable
                        )
                    ]
                ),
                dbc.Row(
                    children = [
                        dbc.Col(
                            products_ag_grid_table
                        )
                    ]
                )
            ],
            fluid = True
        )

layout = charts