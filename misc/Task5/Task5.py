#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Node Type return Node String Attribute, Node int attribute  
#First Query No of Movies per year
from neo4j import GraphDatabase
import pandas as pd  
import numpy as np  
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly
import plotly as py
import plotly.graph_objs as go
import datetime
py.offline.init_notebook_mode(connected=True)
get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')

url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "123456"))


# In[ ]:





# In[ ]:


# Query 1
nodeType="Movie"
nodeA1="m.title"
nodeA2="m.releaseDate"
query1="Match(m:"+nodeType+")return "+nodeA1+","+nodeA2

with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query1)

#Movie name year        
nodeA1A2=[]
for node in nodes:
    if(type(node[nodeA2])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node[nodeA2])/1000).year
        if(node[nodeA1]=='Rodan'):
            nodeA1A2.append([node[nodeA1],1956])
        else:
            nodeA1A2.append([node[nodeA1],hellNo])
            
nodeA1A2.sort(key=lambda x: x[1])

x=[]
y=[]
i=nodeA1A2[0][1]
j=0

while(i<=nodeA1A2[len(nodeA1A2)-1][1]):
    count=0
    while(j<len(nodeA1A2)and i==nodeA1A2[j][1]):
        count+=1
        j+=1
    x.append(i)
    y.append(count)
    i+=1


layout=go.Layout(
    title="First Query",
    yaxis=dict(title='Count'),
    xaxis=dict(title='Year'))



#Line 

trace1=go.Scatter(
    x=x,
    y=y,
    mode='lines'

)


fig=go.Figure(data=[trace1],layout=layout)
py.offline.iplot(fig)


# In[6]:


#Second Query
#Node Type1,Node Type2,relation between them return Node Type1 String Attribute, count Node Type2 order by count Node Type2 
#Second Query actors with the count of their movies

nodeType1="Actor"
nodeType2="Movie"
relation="(a)-[r:ACTS_IN]->(m)"
nodeT1A="a.name"

query2="MATCH (a:"+nodeType1+"),(m:"+nodeType2+"),"+relation+" RETURN "+nodeT1A+",count(m) ORDER BY  count(m) DESC"
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query2)
        
x=[]
y=[]
for node in nodes:
    x.append(node[nodeT1A])
    y.append(node["count(m)"])



layout=go.Layout(
    title="Second Query",
    yaxis=dict(title='Total count of Movies'),
    xaxis=dict(title='Actors')
)



trace = go.Scatter(
    x = x,
    y = y,
    mode='lines'
)

top10X=x[:10]
top10Y=y[:10]
trace = go.Pie(labels=top10X, values=top10Y)


fig=go.Figure(data=[trace],layout=layout)
py.offline.iplot(fig)




# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#Query Three


# In[11]:


#Query 4 Distribution of movies according to genre over years

#Node Type return Distinct Node Attribute
nodeType1="Movie"
nodeT1A="m.genre"
query4="Match(m:"+nodeType1+")return Distinct "+nodeT1A
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query4)

z=[]
for node in nodes:
    z.append(node[nodeT1A])



#Node Type1 return Node String Attribute, Node int attribute,Node String attribute 

nodeA1="m.title"
nodeA2="m.releaseDate"
nodeA3="m.genre"

query5="Match(m:"+nodeType1+")return "+nodeA1+","+nodeA2+","+nodeA3

nodeA1A2A3=[]

with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query5)
for node in nodes:
    if(type(node[nodeA2])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node[nodeA2])/1000).year
        if(node[nodeA1]=='Rodan'):
            nodeA1A2A3.append([node[nodeA1],1956,node[nodeA3]])
        else:
            nodeA1A2A3.append([node[nodeA1],hellNo,node[nodeA3]])
nodeA1A2A3.sort(key=lambda x: x[1])


y=[]
for i in z:
    j=nodeA1A2A3[0][1]
    yearsCounts=[]
    k=0
    while j<=nodeA1A2A3[len(nodeA1A2A3)-1][1]:
        count=0
        while k<len(nodeA1A2A3) and j==nodeA1A2A3[k][1]:
            if nodeA1A2A3[k][2]==i:
                count+=1
            k+=1
        yearsCounts.append(count)
        j+=1
    y.append([i,yearsCounts])

layout=go.Layout(
    title="Fouth Query",
    yaxis=dict(title='Count&Geners'),
    xaxis=dict(title='Year'),
barmode='stack',
)
x=list(range(nodeA1A2A3[0][1],nodeA1A2A3[len(nodeA1A2A3)-1][1]))
print(x)
zA=[]

for i in range(len(z)):
    trace = go.Scatter(
     x=x,
     y=y[i][1],
     mode='lines',
     name=z[i],
     stackgroup='one')
    zA.append(trace)




fig=go.Figure(data=zA,layout=layout)
py.offline.iplot(fig)







# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[56]:


#Query 5 Average running time of films over time
#Node Type return Node String Attribute, Node int attribute,Node double attribute
nodeType="Movie"
nodeA1="m.title"
nodeA2="m.releaseDate"
nodeA3="m.runtime"
query1="Match(m:"+nodeType+")return "+nodeA1+","+nodeA2+","+nodeA3

with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query1)

#Movie name year        
nodeA1A2A3=[]
for node in nodes:
    if(type(node[nodeA2])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node[nodeA2])/1000).year
        if(node[nodeA1]=='Rodan'):
            nodeA1A2A3.append([node[nodeA1],1956,node[nodeA3]])
        else:
            nodeA1A2A3.append([node[nodeA1],hellNo,node[nodeA3]])
            
nodeA1A2A3.sort(key=lambda x: x[1])
y=[]
j=nodeA1A2A3[0][1]
k=0
while j<=nodeA1A2A3[len(nodeA1A2A3)-1][1]:
    sum=0
    count=0
    while k<len(nodeA1A2A3) and j==nodeA1A2A3[k][1]:
        count+=1
        if(type(nodeA1A2A3[k][2])==int and nodeA1A2A3[k][2]>0):
            sum+=nodeA1A2A3[k][2]
        k+=1
    if(count==0):
        count=1
    y.append(sum/count)  
    j+=1
    
x=list(range(nodeA1A2A3[0][1],nodeA1A2A3[len(nodeA1A2A3)-1][1]))
layout=go.Layout(
    title="Fifth Query",
    yaxis=dict(title='Average running time'),
    xaxis=dict(title='Year')) 
trace = go.Scatter(
    x=x,
    y=y,
)
fig=go.Figure(data=[trace],layout=layout)
py.offline.iplot(fig)


# In[ ]:





# In[68]:


#Query 6
#Node Type return Distinct Node Attribute
nodeType1="Movie"
nodeT1A="m.genre"
query4="Match(m:"+nodeType1+")return Distinct "+nodeT1A
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query4)

z=[]
for node in nodes:
    z.append(node[nodeT1A])

#Node Type return Node String Attribute, Node int attribute,Node double attribute

nodeType="Movie"
nodeA1="m.title"
nodeA2="m.releaseDate"
nodeA3="m.genre"
nodeA4="m.runtime"

query1="Match(m:"+nodeType+")return "+nodeA1+","+nodeA2+","+nodeA3+","+nodeA4

with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query1)
#Movie name year        
nodeA1A2A3A4=[]
for node in nodes:
    if(type(node[nodeA2])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node[nodeA2])/1000).year
        if(node[nodeA1]=='Rodan'):
            nodeA1A2A3A4.append([node[nodeA1],1956,node[nodeA3],node[nodeA4]])
        else:
            nodeA1A2A3A4.append([node[nodeA1],hellNo,node[nodeA3],node[nodeA4]])
            
nodeA1A2A3A4.sort(key=lambda x: x[1])

y=[]
for i in z:
    avTimeOverYearG=[]
    k=0
    j=nodeA1A2A3A4[0][1]
    while j<=nodeA1A2A3A4[len(nodeA1A2A3A4)-1][1]:
        sum=0
        count=0
        while k<len(nodeA1A2A3A4) and j==nodeA1A2A3A4[k][1]:
            if nodeA1A2A3A4[k][2]==i:
                count+=1
                if(type(nodeA1A2A3A4[k][3])==int and nodeA1A2A3A4[k][3]>0):
                    sum+=nodeA1A2A3A4[k][3]
            k+=1
        if(count==0):
            count=1
        avTimeOverYearG.append(sum/count)  
        j+=1
    y.append([i,avTimeOverYearG])
layout=go.Layout(
    title="Query 6",
    yaxis=dict(title='avgRunTime&Geners'),
    xaxis=dict(title='Year'),
barmode='stack')
zA=[]
for i in range(len(y)):
    trace = go.Bar(
    x=x,
    y=y[i][1],
    name=z[i]
    )
    zA.append(trace)


fig=go.Figure(data=zA,layout=layout)
py.offline.iplot(fig)

    


# In[70]:


#Query7


def changeTimeStampToDate(node):
    if(type(node["m.releaseDate"])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node["m.releaseDate"])/1000).year
        if(node["m.title"]=='Rodan'):
            return 1956
        else:
            return hellNo
            

#Node Type1, Relation and return count relation
def getGRCount(movie): 
    nodeType1="Movie"
    relation="(m)<-[r:RATED]-()"
        q6="MATCH (m:"+nodeType1+"{title:\""+movie+"\"}),"+relation+" RETURN  count(r)"
        count=0
        with driver.session() as graphDB_Session:
            nodes = graphDB_Session.run(q6)
            for node in nodes:
                count+=node["count(r)"]
        return count

#Node Type1, relation return Distinct Node Type 1String attribute,Node Type String attribute,Node Type String attribute
def getMoviesWithRates():
    nodeT1A2s=[]
    y=[]
    nodeyType1="Movie"
    relation="(m)<-[r:RATED]-()"
    nodeT1A1="m.title"
    nodeT1A3="m.genre"
    nodeT1A3="m.releaseDate"
    nodeT1A1A2A3=[]
    
    q7="MATCH (m:Movie),(m)<-[r:RATED]-() RETURN  Distinct m.title,m.genre,m.releaseDate"
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(q7)
    for node in nodes:
        nodeT1A1A2A3.append([node["m.title"],node["m.genre"],changeTimeStampToDate(node)])
        nodeT1A2s.append(node["m.genre"])
        if(not(changeTimeStampToDate(node) in yearsWRates)):
            y.append(changeTimeStampToDate(node))
    return nodeT1A1A2A3,list(dict.fromkeys(nodeT1A2s)),y

nodeT1A1A2A3,nodeT1A2s,x=getMoviesWithRates()
moviesWithRates.sort(key=lambda x: x[2])
x.sort() 


y=[]
for i in gens:
    j=moviesWithRates[0][2]
    k=0
    countPY=[]
    for j in yearsWRates:
        count=0
        while k<len(moviesWithRates) and moviesWithRates[k][2]==j:
            if i==moviesWithRates[k][1]:
                count+=getGRCount(moviesWithRates[k][0])
            k+=1
        countPY.append(count)
    y.append([i,countPY])
    
    
layout=go.Layout(
    title="7th Query",
    yaxis=dict(title='Count of Rates'),
    xaxis=dict(title='Year'),
    barmode='stack',
    
) 
zA=[]
for i in range(len(movieRPGY)):
    trace= go.Bar(
        x=yearsWRates,
        y=y[i][1],
        name=gens[i]
    )
    zA.append(trace)



fig=go.Figure(data=zA,layout=layout)
py.offline.iplot(fig)


    
    
    
    
    
    
    
    
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




