import dash
import dash_core_components as dcc
import dash_html_components as html
from neo4j import GraphDatabase
url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "123456"))
result=[]
years=[]
for i in range(21):
    cql="Match(m:Movie) where m.released="+str(1980+i)+" return  count(*) "
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(cql)
    for node in nodes:
        result.append(node["count(*)"])
        years.append(str(1980+i))
print(result)
print(years)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': years, 'y': result, 'type': 'bar'},
                    {'x': years, 'y': result, 'type': 'bar','color':'Green'},

            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
