import pandas as pd
from dash import dcc, callback, Output, Input, _dash_renderer
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

superstore = pd.read_excel("data/1. Superstore Dataset.xlsx")
superstore['Order Date'] = pd.to_datetime(superstore['Order Date'], format = "%m/%d/%Y")

_dash_renderer._set_react_version("18.2.0")

dash.register_page(__name__, path = "/productsanalysis")

# Creating our fourth chart
countryquantity = superstore.groupby('Country')['Quantity'].sum().reset_index()

countryquantitydistribution = px.scatter_geo(countryquantity, locations = countryquantity['Country'], locationmode = "country names", projection = "natural earth",
                                            size = countryquantity.groupby("Country")['Quantity'].sum().values, color = countryquantity.groupby("Country")['Quantity'].sum().values, color_continuous_scale = "magma_r")

countryquantitydistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", title = dict(font = dict(color = "white", size = 14)), geo = dict(bgcolor = "rgba(0, 0, 0, 0)", landcolor = "slategrey", showcountries = True))

countryquantitydistribution.update_geos(showframe = True)

countryquantitydistribution.update_coloraxes(colorbar_tickfont_color = "white", colorbar_title = "Quantity Sold", colorbar_title_font_color = "White")


# Creating our sixth chart
superstore['Order Date'] = pd.to_datetime(superstore['Order Date'], format = "%m/%d/%Y")

monthlycategorytrend = superstore.groupby(['Category', pd.Grouper(key = "Order Date", freq = "ME")])['Quantity'].sum().reset_index()

monthlycategorytrenddistribution = px.line(monthlycategorytrend, x = "Order Date", y = "Quantity", color = "Category", title = "Monthly Trend for Categories Sold", line_shape = "spline")

monthlycategorytrenddistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", plot_bgcolor = "rgba(0, 0, 0, 0)", title_font_color = "white", legend_font_color = "white",
                                            xaxis_tickfont_color = 'White', yaxis_tickfont_color = "white", xaxis_title = "", yaxis_title = "", yaxis_showticklabels = False)

monthlycategorytrenddistribution.update_yaxes(showgrid = False, zeroline = False)

monthlycategorytrenddistribution.update_xaxes(showgrid = False)

# Place your chart on dash
charts = dbc.Container(
            children = [
                dbc.Row(
                    dmc.Text("Products Sold Analysis", size="xl", c = "white", style={"fontSize": 40})
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                superstore.Segment.unique(),
                                id = "unique-segments",
                                placeholder = "Select a Segment",
                                className = "text-danger",
                                style = {
                                    "background-color" : "#000000",
                                    "border-color" : "yellow",
                                }
                            )
                        ),
                        dbc.Col(
                            dcc.RangeSlider(
                                superstore['Order Date'].dt.year.min(),
                                superstore['Order Date'].dt.year.max(),
                                step = 1,
                                value=[superstore['Order Date'].dt.year.min(), superstore['Order Date'].dt.year.max()],
                                tooltip={
                                    "always_visible": True,
                                    "template": "{value}"
                                },
                                id = "year-range"
                            )
                        ),
                    ],
                    class_name = "mt-5",
                ),
                dbc.Row(
                    children = [
                        dbc.Col(
                            dcc.Graph(id = "category_quantity_distribution")
                        ),
                        dbc.Col(
                            dcc.Graph(id = "category_subcategory_sales_distribution")
                        ),
                        dbc.Col(
                            dcc.Graph(id = "city_quantity_distribution")
                        )
                    ]
                ),
                dbc.Row(
                    children = [
                        dbc.Col(
                            dcc.Graph(figure = countryquantitydistribution)
                        ),
                        dbc.Col(
                            dcc.Graph(id = "city-subcategory-distribution")
                        )
                    ]
                ),
                dbc.Row(
                    children = [
                        dcc.Graph(figure = monthlycategorytrenddistribution)
                    ]
                ),
            ],
            fluid = True
        )

layout = charts

@callback(
    Output('category_quantity_distribution', 'figure'),
    Output('category_subcategory_sales_distribution', 'figure'),
    Output('city_quantity_distribution', 'figure'),
    Input('unique-segments', 'value'),
    Input('year-range', 'value')
)
def segment_filtering(segment, yearrange):
    if segment and yearrange:
        superstore_segment = superstore[
            (superstore.Segment == segment) & 
            (superstore['Order Date'].dt.year >= yearrange[0]) &
            (superstore['Order Date'].dt.year <= yearrange[1])
        ]  
          
    elif segment:
        superstore_segment = superstore[
            (superstore.Segment == segment)
        ]

    elif yearrange:
        superstore_segment = superstore[
            (superstore['Order Date'].dt.year >= yearrange[0]) &
            (superstore['Order Date'].dt.year <= yearrange[1])
        ]

    else:
        superstore_segment = superstore


    # Creating our first dash chart
    category_sold_distribution = superstore_segment.groupby('Category')['Quantity'].sum()
    categories = category_sold_distribution.keys()
    categories_values = category_sold_distribution.values
    total_products_sold = '{:,}'.format(categories_values.sum())

    category_quantity_distribution = px.pie(names = categories, values = categories_values, title = "Categories Distribution", hole = .7, color_discrete_sequence = px.colors.qualitative.Dark24_r)

    category_quantity_distribution.add_annotation(text = "Total Sold", showarrow = False, y = 0.55, font_size = 14, font_color = 'white')
    category_quantity_distribution.add_annotation(text = total_products_sold, showarrow = False, y = 0.45, font_size = 14, font_color = 'white')

    category_quantity_distribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", title_font = dict(color = 'white', family = "Old Standard TT", size = 50), legend_font_color = 'white')

    # Creating our second dash chart
    category_subcategory_quantity_df = superstore_segment.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()
    category_subcategory_sales_distribution = px.sunburst(category_subcategory_quantity_df, path = ['Category', 'Sub-Category'], 
                values = "Quantity", title = "Category / Sub-Category Distribution")

    category_subcategory_sales_distribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", title = dict(font = dict(color = 'yellow')))

    category_subcategory_sales_distribution.update_traces(marker_colors = px.colors.qualitative.Dark24_r)

    # Creating our third dash chart
    quantitysold = superstore_segment.Quantity.sum()
    top3cities = superstore_segment.groupby('City')['Quantity'].sum().nlargest(3)
    top3citiesgrouped = top3cities.sum()
    percentagedistribution = (top3cities / quantitysold) * 100

    distributionlabels = [f"{city} : {percentage : .2f}%" for city, percentage in zip(top3cities.index, percentagedistribution)]
    cityquantitydistribution = px.pie(names = distributionlabels, values = top3cities.values, hole = 0.7, color_discrete_sequence=px.colors.qualitative.Dark24_r, title = "Top 3 Cities Sold To")

    cityquantitydistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", title = dict(font = dict(color = "white", size = 14)), legend_font_color = "white")

    cityquantitydistribution.add_annotation(text = "Top 3 Cities", showarrow = False, font = dict(size = 14, color = "white"), y = 0.6)
    cityquantitydistribution.add_annotation(text = "Total Sold", showarrow = False, font = dict(size = 14, color = "white"))
    cityquantitydistribution.add_annotation(text = '{:,}'.format(top3citiesgrouped), showarrow = False, font = dict(size = 14, color = "white"), y = 0.4)

    return category_quantity_distribution, category_subcategory_sales_distribution, cityquantitydistribution

@callback(
    Output('city-subcategory-distribution', 'figure'),
    Input('category_quantity_distribution', 'clickData'),
)
def cross_filtering(selectedcategory):
    if selectedcategory:
        superstore_category_crossfiltering = superstore[superstore.Category == selectedcategory['points'][0]['label']]
        city_subcategory_quantity = superstore_category_crossfiltering.groupby(['City', 'Sub-Category'])['Quantity'].sum().reset_index()
    else:
        city_subcategory_quantity = superstore.groupby(['City', 'Sub-Category'])['Quantity'].sum().reset_index()

    # Creating our fifth chart
    city_subcategory_quantity_top_3 = city_subcategory_quantity.groupby('City')['Quantity'].sum().nlargest(3).index

    city_subcategory_quantity_filtered = city_subcategory_quantity[city_subcategory_quantity['City'].isin(city_subcategory_quantity_top_3)]

    city_subcategory_distribution = px.bar(city_subcategory_quantity_filtered, x = "City", y = "Quantity", title = "Sub-Category Quantity Distribution by Top 3 Cities",
                                            color = "Sub-Category", barmode='group', text = "Quantity", color_discrete_sequence = px.colors.qualitative.Dark24_r)

    city_subcategory_distribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", plot_bgcolor = "rgba(0, 0, 0, 0)", title_font_color = "white", legend_font_color = "white",
                                                xaxis_tickfont_color = 'White', yaxis_tickfont_color = "white", xaxis_title = "", yaxis_title = "", yaxis_showticklabels = False, bargap = 0.1)

    city_subcategory_distribution.update_yaxes(showgrid = False, zeroline = False)

    city_subcategory_distribution.update_traces(marker_line_width = 0, textposition = "outside", textfont_color = 'white', textfont_size = 10)

    return city_subcategory_distribution
