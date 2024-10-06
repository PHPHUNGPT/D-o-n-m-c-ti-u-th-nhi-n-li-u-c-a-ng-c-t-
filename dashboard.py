import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Đọc dữ liệu đã tiền xử lý
df = pd.read_csv('auto-mpg-processed.csv')

# Tạo ứng dụng Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Khởi tạo đối tượng server cho Gunicorn và Waitress
server = app.server

# Lấy danh sách các biến
variables = df.columns

# Layout của dashboard
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Dashboard Auto MPG", className="text-center mb-4"), width=12)),

    # Dropdown để chọn biến cho biểu đồ phân tán
    dbc.Row([
        dbc.Col([
            html.Label("Chọn biến X cho biểu đồ phân tán:"),
            dcc.Dropdown(
                id='scatter-x-dropdown',
                options=[{'label': var, 'value': var} for var in variables],
                value='weight'  # Giá trị mặc định
            ),
            html.Label("Chọn biến Y cho biểu đồ phân tán:"),
            dcc.Dropdown(
                id='scatter-y-dropdown',
                options=[{'label': var, 'value': var} for var in variables],
                value='mpg'  # Giá trị mặc định
            ),
            dcc.Graph(id='scatter-plot'),
        ], width=6),

        # Dropdown để chọn biến cho biểu đồ Pie
        dbc.Col([
            html.Label("Chọn biến cho biểu đồ Pie:"),
            dcc.Dropdown(
                id='pie-dropdown',
                options=[{'label': var, 'value': var} for var in variables],
                value='origin'  # Giá trị mặc định
            ),
            dcc.Graph(id='pie-chart'),
        ], width=6),
    ]),

    # Biểu đồ cột phân bố (histogram) và ma trận tương quan
    dbc.Row([
        dbc.Col([
            html.Label("Chọn biến cho biểu đồ phân bố:"),
            dcc.Dropdown(
                id='hist-dropdown',
                options=[{'label': var, 'value': var} for var in variables],
                value='mpg'  # Giá trị mặc định
            ),
            dcc.Graph(id='hist-plot'),
        ], width=6),

        dbc.Col(dcc.Graph(figure=px.imshow(df.corr(), text_auto=True, title="Ma trận tương quan")), width=6),
    ]),

    # Biểu đồ đường và Boxplot
    dbc.Row([
        dbc.Col([
            html.Label("Chọn biến Y cho biểu đồ đường:"),
            dcc.Dropdown(
                id='line-y-dropdown',
                options=[{'label': var, 'value': var} for var in variables],
                value='mpg'  # Giá trị mặc định
            ),
            dcc.Graph(id='line-plot'),
        ], width=6),

        dbc.Col([
            html.Label("Chọn biến cho Boxplot:"),
            dcc.Dropdown(
                id='boxplot-dropdown',
                options=[{'label': var, 'value': var} for var in variables],
                value='mpg'  # Giá trị mặc định
            ),
            dcc.Graph(id='boxplot'),
        ], width=6),
    ])
])

# Callbacks để cập nhật biểu đồ phân tán
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('scatter-x-dropdown', 'value'),
     Input('scatter-y-dropdown', 'value')]
)
def update_scatter_plot(x_var, y_var):
    fig = px.scatter(df, x=x_var, y=y_var, color='cylinders', title=f"Biểu đồ phân tán: {x_var} vs {y_var}")
    return fig

# Callback để cập nhật biểu đồ Pie
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('pie-dropdown', 'value')]
)
def update_pie_chart(pie_var):
    fig = px.pie(df, names=pie_var, title=f"Biểu đồ Pie: {pie_var}")
    return fig

# Callback để cập nhật biểu đồ phân bố (Histogram)
@app.callback(
    Output('hist-plot', 'figure'),
    [Input('hist-dropdown', 'value')]
)
def update_histogram(hist_var):
    fig = px.histogram(df, x=hist_var, title=f"Biểu đồ cột phân bố: {hist_var}")
    return fig

# Callback để cập nhật biểu đồ đường
@app.callback(
    Output('line-plot', 'figure'),
    [Input('line-y-dropdown', 'value')]
)
def update_line_plot(y_var):
    fig = px.line(df, x='model year', y=y_var, title=f"Biểu đồ đường: {y_var} theo năm")
    return fig

# Callback để cập nhật Boxplot
@app.callback(
    Output('boxplot', 'figure'),
    [Input('boxplot-dropdown', 'value')]
)
def update_boxplot(box_var):
    fig = px.box(df, y=box_var, title=f"Boxplot: {box_var}")
    return fig

# Chạy ứng dụng
if __name__ == '__main__':
    app.run_server(debug=True)
