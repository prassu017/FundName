import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table  # Updated import for dash_table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Fund

# Database setup
engine = create_engine('sqlite:///funds.db')
Session = sessionmaker(bind=engine)
session = Session()

# Sample data for dropdown and initial load
fund_options = [
    {"label": "AB Global Core Equity Portfolio", "value": "AB Global Core Equity Portfolio"},
    {"label": "AB Sustainable Global Thematic Portfolio", "value": "AB Sustainable Global Thematic Portfolio"},
    {"label": "AB High Income Fund", "value": "AB High Income Fund"},
    {"label": "AB Municipal Income Fund", "value": "AB Municipal Income Fund"},
    {"label": "AB Large Cap Growth Fund", "value": "AB Large Cap Growth Fund"},
    {"label": "AB Small Cap Growth Portfolio", "value": "AB Small Cap Growth Portfolio"},
    {"label": "AB Sustainable US Thematic Portfolio", "value": "AB Sustainable US Thematic Portfolio"},
    {"label": "AB Short Duration High Yield Portfolio", "value": "AB Short Duration High Yield Portfolio"},
]

initial_data = [
    {"fund_name": "AB Global Core Equity Portfolio", "ticker": "N/A", "share_class": "Class A", "market_price": 100,
     "trader_login": "T001", "manager_login": "M001", "qty": 100, "price": 1000},
    {"fund_name": "AB Sustainable Global Thematic Portfolio", "ticker": "N/A", "share_class": "Class A",
     "market_price": 150, "trader_login": "T002", "manager_login": "M002", "qty": 200, "price": 2000},
    {"fund_name": "AB High Income Fund", "ticker": "AGDAX", "share_class": "Class A", "market_price": 75,
     "trader_login": "T003", "manager_login": "M003", "qty": 150, "price": 1125},
    # Add more rows as needed
]

# App initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Fund Management"), className="text-center mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id="fund-dropdown", options=fund_options, placeholder="Select Fund"), width=3),
        dbc.Col(dbc.Input(id="ticker", placeholder="Ticker", type="text"), width=2),
        dbc.Col(dbc.Input(id="share-class", placeholder="Share Class", type="text"), width=2),
        dbc.Col(dbc.Input(id="market-price", placeholder="Market Price", type="number"), width=2),
        dbc.Col(dbc.Input(id="trader-login", placeholder="Trader Login (5 chars)", type="text", maxLength=5), width=2),
        dbc.Col(dbc.Input(id="manager-login", placeholder="Manager Login", type="text"), width=2),
    ], className="mb-3"),
    dbc.Row([
        dbc.Col(dbc.Input(id="quantity", placeholder="Quantity", type="number"), width=2),
        dbc.Col(dbc.Input(id="price", placeholder="Price", type="number"), width=2),
    ], className="mb-3"),
    dbc.Row([
        dbc.Col(dbc.Button("Save Fund", id="save-button", color="primary"), width=2),
        dbc.Col(dbc.Button("Load Funds", id="load-button", color="secondary"), width=2),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Div(id="output"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='fund-table',
            columns=[
                {"name": "Fund Name", "id": "fund_name"},
                {"name": "Ticker", "id": "ticker"},
                {"name": "Share Class", "id": "share_class"},
                {"name": "Market Price", "id": "market_price"},
                {"name": "Trader Login", "id": "trader_login"},
                {"name": "Manager Login", "id": "manager_login"},
                {"name": "Quantity", "id": "qty"},
                {"name": "Price", "id": "price"},
            ],
            data=initial_data,
            editable=False,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
        ), width=12)
    ])
])


# Callback for managing funds
@app.callback(
    [Output("output", "children"),
     Output("fund-table", "data")],
    [Input("save-button", "n_clicks"), Input("load-button", "n_clicks")],
    [State("fund-dropdown", "value"), State("ticker", "value"), State("share-class", "value"),
     State("market-price", "value"), State("trader-login", "value"), State("manager-login", "value"),
     State("quantity", "value"), State("price", "value"),
     State("fund-table", "data")]
)
def manage_fund(save_clicks, load_clicks, selected_fund, ticker, share_class, market_price, trader_login,
                manager_login, quantity, price, table_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", table_data

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "save-button" and selected_fund and ticker and share_class and market_price and trader_login and manager_login and quantity and price:
        # Save the fund to the database and add to table data
        new_fund = Fund(name=selected_fund, type=share_class, amount=price)
        session.add(new_fund)
        session.commit()

        new_row = {
            "fund_name": selected_fund,
            "ticker": ticker,
            "share_class": share_class,
            "market_price": market_price,
            "trader_login": trader_login,
            "manager_login": manager_login,
            "qty": quantity,
            "price": price
        }
        table_data.append(new_row)
        return f"Fund '{selected_fund}' saved successfully.", table_data

    elif button_id == "load-button":
        # Load funds from the database and populate the table
        funds = session.query(Fund).all()
        loaded_data = [{"fund_name": fund.name, "ticker": "N/A", "share_class": "Class A", "market_price": 100,
                        "trader_login": "T001", "manager_login": "M001", "qty": 100, "price": fund.amount} for fund in
                       funds]

        if not loaded_data:
            return "No funds found.", initial_data

        return "Funds loaded successfully.", loaded_data

    return "", table_data


if __name__ == "__main__":
    app.run_server(debug=True)
