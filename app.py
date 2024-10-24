from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

superstore = pd.read_excel("data/1. Superstore Dataset.xlsx")

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = dbc.Col(
    children = [
        dcc.Link(
            children = "Page 2",
            href = ""
        )
    ],
    class_name = "bg-success min-vh-100",
    width = 2
)

# Creating our first dash chart
category_sold_distribution = superstore.groupby('Category')['Quantity'].sum()

categories = category_sold_distribution.keys()
categories_values = category_sold_distribution.values
total_products_sold = '{:,}'.format(categories_values.sum())

category_quantity_distribution = px.pie(names = categories, values = categories_values, title = "Categories Distribution", hole = .7, color_discrete_sequence = px.colors.qualitative.Dark24_r)

category_quantity_distribution.add_annotation(text = "Total Sold", showarrow = False, y = 0.55, font_size = 14, font_color = 'white')
category_quantity_distribution.add_annotation(text = total_products_sold, showarrow = False, y = 0.45, font_size = 14, font_color = 'white')

category_quantity_distribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", title_font = dict(color = 'white', family = "Old Standard TT", size = 50), legend_font_color = 'white')

# Creating our second dash chart
category_subcategory_quantity_df = superstore.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()

category_subcategory_sales_distribution = px.sunburst(category_subcategory_quantity_df, path = ['Category', 'Sub-Category'], 
            values = "Quantity", title = "Category / Sub-Category Distribution")

# category_subcategory_sales_distribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", title_font_color = 'white')
category_subcategory_sales_distribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", title = dict(font = dict(color = 'yellow')))

category_subcategory_sales_distribution.update_traces(marker_colors = px.colors.qualitative.Dark24_r)

# Place your chart on dash
charts = dbc.Col(
    children = [
        dbc.Container(
            dbc.Row(
                children = [
                    dbc.Col(
                        dcc.Graph(figure = category_quantity_distribution)
                    ),
                    dbc.Col(
                        dcc.Graph(figure = category_subcategory_sales_distribution)
                    )
                ]
            ),
            fluid = True
        )
    ]
)

app.layout = dbc.Container(
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

if __name__ == '__main__':
    app.run(debug = True, use_reloader = True)