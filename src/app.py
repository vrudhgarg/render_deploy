from dash import Dash, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
from vega_datasets import data


cars = data.cars()

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='x-col', options=cars.columns, value='Horsepower'), md=4),
        dbc.Col(
            dbc.Tabs(
                [
                    dbc.Tab(
                        [
                            dbc.Card(id='card-avg'),
                            dvc.Vega(id='scatter', spec={}),
                        ],
                        label='Chart'
                    ),
                    dbc.Tab(
                        [
                            dcc.Markdown(cars.describe().to_markdown()),
                        ],
                        label='Data summary'
                    )
                ],
            ),
            md=8
        )
    ])
])

# Server side callbacks/reactivity
@callback(
    Output('scatter', 'spec'),
    Output('card-avg', 'children'),
    Input('x-col', 'value')
)
def create_chart(x_col):
    chart = alt.Chart(cars).mark_point().encode(
            x=x_col,
            y='Miles_per_Gallon',
            tooltip='Origin'
        ).interactive().to_dict()

    card_avg = [
        dbc.CardHeader(f'Average {x_col}'),
        dbc.CardBody(f'{cars[x_col].mean() :.1f}')
    ]
    
    return chart, card_avg


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=False)