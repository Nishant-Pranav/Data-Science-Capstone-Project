from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("historical_automobile_sales.csv")

app = Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# Dropdown options
report_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in sorted(df['Year'].unique())]

# Layout
app.layout = html.Div([

    html.H1(
        "Automobile Statistics Dashboard",
        style={'textAlign': 'center'}
    ),

    html.Div([
        html.Label("Select Statistics Type"),
        dcc.Dropdown(
            id='statistics-dropdown',
            options=report_options,
            value='Yearly Statistics'
        )
    ]),

    html.Br(),

    html.Div([
        html.Label("Select Year"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': i, 'value': i} for i in year_list],
            value=year_list[0]
        )
    ]),

    html.Br(),

    html.Div(id='output-container')
])

# Callback
@app.callback(
    Output('output-container', 'children'),
    Input('statistics-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_graphs(statistics, selected_year):

    # Recession Statistics
    if statistics == 'Recession Period Statistics':

        rec_data = df[df['Recession'] == 1]

        fig1 = px.bar(
            rec_data.groupby('Year')['Automobile_Sales']
            .mean()
            .reset_index(),
            x='Year',
            y='Automobile_Sales',
            title='Average Automobile Sales During Recession'
        )

        fig2 = px.pie(
            rec_data,
            names='Vehicle_Type',
            values='Automobile_Sales',
            title='Vehicle Type Distribution During Recession'
        )

        fig3 = px.scatter(
            rec_data,
            x='Consumer_Confidence',
            y='Automobile_Sales',
            color='Vehicle_Type',
            title='Consumer Confidence vs Automobile Sales'
        )

        fig4 = px.line(
            rec_data.groupby('Year')['GDP']
            .mean()
            .reset_index(),
            x='Year',
            y='GDP',
            title='GDP During Recession'
        )

        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ])

    # Yearly Statistics
    else:

        yearly_data = df[df['Year'] == selected_year]

        fig1 = px.bar(
            yearly_data.groupby('Month')['Automobile_Sales']
            .mean()
            .reset_index(),
            x='Month',
            y='Automobile_Sales',
            title=f'Monthly Sales ({selected_year})'
        )

        fig2 = px.pie(
            yearly_data,
            names='Vehicle_Type',
            values='Automobile_Sales',
            title=f'Vehicle Sales Distribution ({selected_year})'
        )

        fig3 = px.scatter(
            yearly_data,
            x='Price',
            y='Automobile_Sales',
            color='Vehicle_Type',
            title=f'Price vs Sales ({selected_year})'
        )

        fig4 = px.line(
            yearly_data.groupby('Month')['Advertising_Expenditure']
            .mean()
            .reset_index(),
            x='Month',
            y='Advertising_Expenditure',
            title=f'Advertising Expenditure ({selected_year})'
        )

        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ])


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=8051)