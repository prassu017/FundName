import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Fund

engine = create_engine('sqlite:///funds.db')
Session = sessionmaker(bind=engine)
session = Session()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Fund Management"), className="text-center mb-4")
    ]),
    dbc.Row([
        dbc.Col(dbc.Input(id="fund-name", placeholder="Fund Name", type="text"), width=4),
        dbc.Col(dbc.Input(id="fund-type", placeholder="Fund Type", type="text"), width=4),
        dbc.Col(dbc.Input(id="fund-amount", placeholder="Fund Amount", type="number"), width=4),
    ], className="mb-3"),
    dbc.Row([
        dbc.Col(dbc.Button("Save Fund", id="save-button", color="primary"), width=2),
        dbc.Col(dbc.Button("Load Funds", id="load-button", color="secondary"), width=2),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Div(id="output"))
    ])
])

@app.callback(
    Output("output", "children"),
    [Input("save-button", "n_clicks"), Input("load-button", "n_clicks")],
    [State("fund-name", "value"), State("fund-type", "value"), State("fund-amount", "value")]
)
def manage_fund(save_clicks, load_clicks, name, fund_type, amount):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ""

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "save-button" and name and fund_type and amount:
        # Save the fund to the database
        new_fund = Fund(name=name, type=fund_type, amount=float(amount))
        session.add(new_fund)
        session.commit()
        return f"Fund '{name}' saved successfully."

    elif button_id == "load-button":
        # Load funds from the database
        funds = session.query(Fund).all()
        if not funds:
            return "No funds found."
        return html.Ul([html.Li(f"{fund.name}: {fund.type}, Amount: {fund.amount}") for fund in funds])

    return ""

if __name__ == "__main__":
    app.run_server(debug=True)
