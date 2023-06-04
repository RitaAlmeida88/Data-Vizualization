#!/usr/bin/env python
# coding: utf-8

# In[426]:


import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


# In[427]:


import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import statsmodels.api as sm


# In[ ]:


df = pd.read_csv('accidents2016.csv')


# In[433]:


df.info()


# In[404]:


df['year'].unique()


# In[434]:


df.count()


# In[436]:


# Count the number of accidents per state
state_counts = df["State"].value_counts()

# Create a bar chart
fig1 = go.Figure(
    data=[go.Bar(x=state_counts.index, y=state_counts.values)],
    layout=go.Layout(title="Accidents per State")
)

fig1.show()


# In[437]:


# Convert the Start_Time column to datetime format
df["Start_Time"] = pd.to_datetime(df["Start_Time"])


# Extract the hour of day
df["Hour"] = df["Start_Time"].dt.hour

# Count the number of accidents per hour
hour_counts = df["Hour"].value_counts().sort_index()

# Create a line chart
fig2 = go.Figure(
    data=[go.Scatter(x=hour_counts.index, y=hour_counts.values, mode="lines")],
    layout=go.Layout(title="Accidents by Hour of Day")
)


# In[438]:


# Extract the day of week and hour of day
df["DayOfWeek"] = df["Start_Time"].dt.day_name()


# Create a pivot table of accident counts by day of week and hour of day
day_hour_counts = pd.pivot_table(df, values="ID", index="DayOfWeek", columns="Hour", aggfunc="count")

# Create a heatmap
fig3 = go.Figure(
    data=[go.Heatmap(x=day_hour_counts.columns, y=day_hour_counts.index, z=day_hour_counts.values)],
    layout=go.Layout(title="Accidents by Day of Week and Hour of Day")
)


# In[439]:


hour_count = df.groupby('Hour')['ID'].count().reset_index()
hour_count.columns = ['Hour', 'Count']

fig4 = px.pie(hour_count, values='Count', names='Hour', title='Distribution of Accidents by Hour of Day')


# In[440]:


# agrupar os dados por dia e calcular a contagem de acidentes e a precipitação média
daily_counts = df.groupby(df['Start_Time'].dt.date).agg({'ID':'count', 'Precipitation(in)':'mean'}).reset_index()
daily_counts = daily_counts.rename(columns={'Start_Time':'Date', 'ID':'Accident_Count'})

# plotar um gráfico de dispersão da contagem de acidentes x precipitação média
fig5 = px.scatter(daily_counts, x='Precipitation(in)', y='Accident_Count', trendline='ols')


# In[441]:


def categorize_severity(x):
    if x == 1:
        return 'Mínima'
    elif x == 2:
        return 'Moderada'
    elif x == 3:
        return 'Grave'
    elif x == 4:
        return 'Muito Grave'
    else:
        return 'Desconhecida'

df['Severity_cat'] = df['Severity'].apply(categorize_severity)


# In[442]:


df_state = df.groupby(['State', 'Severity_cat']).agg({'ID': 'count'}).reset_index()


# In[443]:


fig6 = px.scatter_geo(df_state, 
                     locations='State', 
                     color='Severity_cat', 
                     size='ID', 
                     locationmode='USA-states',
                     size_max=50,
                     scope='usa',
                     hover_name='Severity_cat',
                     projection='albers usa',
                     title='Severidade dos Acidentes nos EUA por Estado')


# In[444]:


df_city = df.groupby(['City', 'Severity_cat']).agg({'ID': 'count'}).reset_index()


# In[445]:


fig7 = px.scatter(df_city, 
                 x='City', 
                 y='ID', 
                 color='Severity_cat', 
                 size='ID',
                 size_max=50,
                 hover_name='Severity_cat',
                 title='Severidade dos Acidentes nos EUA por Cidade')


# In[446]:


df["Precipitation"] = df["Precipitation(in)"].apply(lambda x: "Yes" if x > 0 else "No")


# In[447]:


state_info = df.groupby("State").agg({"Severity": "count", "Precipitation": lambda x: sum(x == "Yes"), "ID": pd.Series.nunique}).reset_index()
state_info = state_info.rename(columns={"ID": "Accident Count"})


# In[448]:


fig8 = px.scatter_geo(state_info, locations="State", locationmode="USA-states", color="Precipitation", size="Accident Count", hover_name="State", hover_data=["Severity", "Precipitation", "Accident Count"], scope="usa", title="US Accidents by State - Severity, Precipitation and Accident Count")


# In[449]:


grouped = df.groupby("Weather_Condition")["ID"].count().reset_index(name="count")

# Criar uma figura do Plotly com o tipo de gráfico "bar"
fig9 = go.Figure()

# Adicionar um trace para cada estado do tempo, com a contagem de acidentes para esse estado
fig9.add_trace(go.Bar(
    x=grouped["Weather_Condition"],
    y=grouped["count"],
    name="Acidentes",
    marker_color="steelblue"
))

# Configurar o layout do gráfico
fig9.update_layout(
    title="Número de Acidentes por Estado do Tempo",
    xaxis_title="Estado do Tempo",
    yaxis_title="Número de Acidentes",
    barmode="stack",
    bargap=0.1,
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)


# In[450]:


# Define os dias da semana
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
months_of_year = ['January', 'February', 'March', 'April', 'May', 'June', 'Jully', 'August', 'September', 'October', 'November', 'December']


# In[451]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__, assets_folder='Assets')
server = app.server

# Estilos CSS personalizados
styles = {
    'container': {
        'width': '90%',
        'max-width': '1200px',
        'margin': '0 auto',
        'background-color': '#F7F7F7',
        'padding': '20px'
    },
    'header': {
        'text-align': 'center',
        'padding-top': '30px',
        'padding-bottom': '20px',
        'font-size': '36px',
        'font-weight': 'bold',
        'color': '#333333'
    },
    'title': {
        'text-align': 'center',
        'font-size': '24px',
        'color': '#666666',
        'margin-bottom': '20px'
    },
    'subtitle': {
        'text-align': 'center',
        'font-size': '18px',
        'color': '#666666',
        'margin-bottom': '20px'
    },
    'graph-container': {
        'display': 'flex',
        'flex-wrap': 'wrap',
        'justify-content': 'space-between',
        'margin-bottom': '30px'
    },
    'graph': {
        'width': '48%',
        'margin-bottom': '20px',
        'background-color': '#FFFFFF',
        'border-radius': '5px',
        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
    },
    'dropdown': {
        'width': '200px',
        'margin-bottom': '20px'
    }
}

# Layout do painel
app.layout = html.Div(style=styles['container'], children=[
    html.H1("Análise de Acidentes", style=styles['header']),
    html.H2("Data visualization", style=styles['subtitle']),
    html.H3("Rita Almeida", style=styles['subtitle']),
    
    html.Div(style=styles['graph-container'], children=[
        html.Div(style=styles['graph'], children=[
            dcc.Graph(id="fig1", figure=fig1)
        ]),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(id="fig2", figure=fig2),
            dcc.Dropdown(
                id="day-dropdown-fig2",
                options=[{"label": day, "value": day} for day in days_of_week],
                value="Monday",
                placeholder="Select a day of the week",
                style=styles['dropdown']
            )
        ]),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(figure=fig3)
        ]),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(id="fig4", figure=fig4),
            dcc.Dropdown(
                id="day-dropdown-fig4",
                options=[{"label": day, "value": day} for day in days_of_week],
                value="Monday",
                placeholder="Select a day of the week",
                style=styles['dropdown']
            )
        ]),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(figure=fig5)
        ]),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(figure=fig6)
        ]),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(id="fig7", figure=fig7),
            dcc.Dropdown(
                id="month-dropdown-fig7",
                options=[{"label": month, "value": month} for month in months_of_year],
                value="January",
                placeholder="Select a month",
                style=styles['dropdown']
            )
        ]),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(id="fig8", figure=fig8)
        ]),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(id="fig9", figure=fig9)
        ])
    ])
])

@app.callback(
    Output("fig2", "figure"),
    Input("day-dropdown-fig2", "value")
)
def update_fig2(selected_day):
    # Filtra os dados pelo dia da semana selecionado
    filtered_df = df[df["Start_Time"].dt.day_name() == selected_day]
    
    # Conta o número de acidentes por hora
    hour_counts = filtered_df["Hour"].value_counts().sort_index()
    
    # Atualiza a figura fig2 com os dados filtrados
    fig = go.Figure(data=[go.Scatter(x=hour_counts.index, y=hour_counts.values, mode="lines")],
                    layout=go.Layout(title=f"Accidents by Hour of Day - {selected_day}"))
    
    return fig

@app.callback(
    Output("fig4", "figure"),
    Input("day-dropdown-fig4", "value")
)
def update_fig4(selected_day):
    # Filtra os dados pelo dia da semana selecionado
    filtered_df = df[df["Start_Time"].dt.day_name() == selected_day]
    
    # Agrupa os dados por hora e calcula a contagem de acidentes por hora
    hour_counts = filtered_df.groupby('Hour')['ID'].count().reset_index()
    hour_counts.columns = ['Hour', 'Count']
    
    # Atualiza a figura fig4 com os dados filtrados
    fig = px.pie(hour_counts, values='Count', names='Hour', title=f'Distribution of Accidents by Hour of Day - {selected_day}')
    
    return fig

@app.callback(
    Output("fig7", "figure"),
    Input("month-dropdown-fig7", "value")
)
def update_fig7(selected_month):
    # Filtra os dados pelo mês selecionado
    filtered_df = df[df["Start_Time"].dt.month_name() == selected_month]
    
    # Conta o número de acidentes por dia
    day_counts = filtered_df["Start_Time"].dt.day.value_counts().sort_index()
    
    # Atualiza a figura fig7 com os dados filtrados
    fig = go.Figure(data=[go.Scatter(x=day_counts.index, y=day_counts.values, mode="lines")],
                    layout=go.Layout(title=f"Accidents by Day of Month - {selected_month}"))
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




