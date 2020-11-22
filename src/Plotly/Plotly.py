#!/usr/bin/env python
# coding: utf-8

# In[52]:


#import pacakges and set enviroment
from neo4j import GraphDatabase
import pandas as pd  
import numpy as np  
import numpy as np  
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly as py
import plotly.graph_objs as go
import datetime
py.offline.init_notebook_mode(connected=True)
get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')

#Create intiate driver for your database
url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "123456"))


# In[ ]:





# In[53]:


#First Query No of Movies per year

nodeType="Movie"
nodeA1="m.title"
nodeA2="m.releaseDate"
query1="Match(m:"+nodeType+")return "+nodeA1+","+nodeA2

#intiate session to run the query
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query1)

#nodeA1A2 -> list of [Movie name, year of release]       
nodeA1A2=[]

#in the movies data base there is a mistake in the date of release for Rodan movie
#filling nodeA1A2 list
for node in nodes:
    if(type(node[nodeA2])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node[nodeA2])/1000).year
        if(node[nodeA1]=='Rodan'):
            nodeA1A2.append([node[nodeA1],1956])
        else:
            nodeA1A2.append([node[nodeA1],hellNo])
            
#Sort the list according to year of release          
nodeA1A2.sort(key=lambda x: x[1])

#x-> x Axis data, y->Y Axis data
x=[]
y=[]
i=nodeA1A2[0][1]
j=0

#filling x and y lists with count in y and year in x
while(i<=nodeA1A2[len(nodeA1A2)-1][1]):
    count=0
    while(j<len(nodeA1A2)and i==nodeA1A2[j][1]):
        count+=1
        j+=1
    x.append(i)
    y.append(count)
    i+=1

#The Layout of the plot
layout=go.Layout(
    title="First Query",
    yaxis=dict(title='Count'),
    xaxis=dict(title='Year'))



#Type of the graph "Line"

trace1=go.Scatter(
    x=x,
    y=y,
    mode='lines'

)

#Create the figure with the layout and the data of x axis and y axis
fig=go.Figure(data=[trace1],layout=layout)
py.offline.iplot(fig)


# In[54]:


#Second Query
#Second Query actors with the count of their movies

nodeType1="Actor"
nodeType2="Movie"
relation="(a)-[r:ACTS_IN]->(m)"
nodeT1A="a.name"
query2="MATCH (a:"+nodeType1+"),(m:"+nodeType2+"),"+relation+" RETURN "+nodeT1A+",count(m) ORDER BY  count(m) DESC"

#intiate session to run the query
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query2)
        
#x-> x Axis data, y->Y Axis data        
x=[]
y=[]
#filling x and y lists with total coounts of movies in y and actors in x
for node in nodes:
    x.append(node[nodeT1A])
    y.append(node["count(m)"])


#The Layout of the plot
layout=go.Layout(
    title="Second Query",
    yaxis=dict(title='Total count of Movies'),
    xaxis=dict(title='Actors')
)


#Type of the graph "Pie chart" with top 10 actors with the highest number of movies"
top10X=x[:10]
top10Y=y[:10]
trace = go.Pie(labels=top10X, values=top10Y)

#Create the figure with the layout and the data of x axis and y axis
fig=go.Figure(data=[trace],layout=layout)
py.offline.iplot(fig)




# In[55]:


#Query 3 Distribution of movies according to genre over years

nodeType1="Movie"
nodeT1A="m.genre"
query4="Match(m:"+nodeType1+")return Distinct "+nodeT1A

#intiate session to run the query
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query4)
        
#Categories og genres
z=[]
#filling z list with genres 
for node in nodes:
    z.append(node[nodeT1A])

nodeA1="m.title"
nodeA2="m.releaseDate"
nodeA3="m.genre"
query5="Match(m:"+nodeType1+")return "+nodeA1+","+nodeA2+","+nodeA3

#nodeA1A2A3 -> list of [Movie name, year of release,genre]  
nodeA1A2A3=[]

#intiate session to run the query
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query5)
        
#filling nodeA1A2A3 list
for node in nodes:
    if(type(node[nodeA2])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node[nodeA2])/1000).year
        if(node[nodeA1]=='Rodan'):
            nodeA1A2A3.append([node[nodeA1],1956,node[nodeA3]])
        else:
            nodeA1A2A3.append([node[nodeA1],hellNo,node[nodeA3]])
            
#Sort the list according to year of release          
nodeA1A2A3.sort(key=lambda x: x[1])

#y -> Y Axis data with counts
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

#Layout of the plot
layout=go.Layout(
    title="Fouth Query",
    yaxis=dict(title='Count&Geners'),
    xaxis=dict(title='Year'),
    barmode='stack',
)

#x -> x Axis data with years from oldest year to the recent year in the data
x=list(range(nodeA1A2A3[0][1],nodeA1A2A3[len(nodeA1A2A3)-1][1]))

#List of graphs for each category type of graph is area chart
zA=[]
#Filling zA list
for i in range(len(z)):
    trace = go.Scatter(
     x=x,
     y=y[i][1],
     mode='lines',
     name=z[i],
     stackgroup='one')
    zA.append(trace)



#Create the figure with the layout and the data of x axis and y axis
fig=go.Figure(data=zA,layout=layout)
py.offline.iplot(fig)







# In[56]:


#Query 4 Average running time of films over time

nodeType="Movie"
nodeA1="m.title"
nodeA2="m.releaseDate"
nodeA3="m.runtime"
query1="Match(m:"+nodeType+")return "+nodeA1+","+nodeA2+","+nodeA3

#intiate session to run the query
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query1)

#Movie name year        
nodeA1A2A3=[]
#filling nodeA1A2A3 list
for node in nodes:
    if(type(node[nodeA2])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node[nodeA2])/1000).year
        if(node[nodeA1]=='Rodan'):
            nodeA1A2A3.append([node[nodeA1],1956,node[nodeA3]])
        else:
            nodeA1A2A3.append([node[nodeA1],hellNo,node[nodeA3]])
            
#Sorting nodeA1A2A3 by year in ascending order            
nodeA1A2A3.sort(key=lambda x: x[1])
#y -> y axis data 
y=[]
j=nodeA1A2A3[0][1]
k=0
#filling y list with the average running year for each year
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
    
#x -> x Axis data with years from oldest year to the recent year in the data 
x=list(range(nodeA1A2A3[0][1],nodeA1A2A3[len(nodeA1A2A3)-1][1]))

#Layout of the plot
layout=go.Layout(
    title="Fifth Query",
    yaxis=dict(title='Average running time'),
    xaxis=dict(title='Year'))

#Type of the graph "Line"
trace = go.Scatter(
    x=x,
    y=y,
)

#Create the figure with the layout and the data of x axis and y axis
fig=go.Figure(data=[trace],layout=layout)
py.offline.iplot(fig)


# In[57]:


#Query 5 Average running time of films based on genre over time

nodeType1="Movie"
nodeT1A="m.genre"
query4="Match(m:"+nodeType1+")return Distinct "+nodeT1A

#intiate session to run the query
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query4)
        
#Categories of genres
z=[]
#filling z list with genres
for node in nodes:
    z.append(node[nodeT1A])

nodeType="Movie"
nodeA1="m.title"
nodeA2="m.releaseDate"
nodeA3="m.genre"
nodeA4="m.runtime"
query1="Match(m:"+nodeType+")return "+nodeA1+","+nodeA2+","+nodeA3+","+nodeA4

#intiate session to run the query
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query1)
        
#nodeA1A2A3A4 list of[Movie name ,year]       
nodeA1A2A3A4=[]
#filling nodeA1A2A3A4 list
for node in nodes:
    if(type(node[nodeA2])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node[nodeA2])/1000).year
        if(node[nodeA1]=='Rodan'):
            nodeA1A2A3A4.append([node[nodeA1],1956,node[nodeA3],node[nodeA4]])
        else:
            nodeA1A2A3A4.append([node[nodeA1],hellNo,node[nodeA3],node[nodeA4]])
            
#Sort the list according to year of release                     
nodeA1A2A3A4.sort(key=lambda x: x[1])
#y-> y axis data
y=[]
#filling y axis data with average running time over years for each genre 
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
    
#Layput of the plot    
layout=go.Layout(
    title="Query 6",
    yaxis=dict(title='avgRunTime&Geners'),
    xaxis=dict(title='Year'),
barmode='stack')

#List of graphs for each category graph type is bar chart
zA=[]
#filling zA list
for i in range(len(y)):
    trace = go.Bar(
    x=x,
    y=y[i][1],
    name=z[i]
    )
    zA.append(trace)

#Create the figure with the layout and the data of x axis and y axis
fig=go.Figure(data=zA,layout=layout)
py.offline.iplot(fig)

    


# In[60]:


#Query6 Number of Ratings of films based on genre, over year

#Methode to change time stamp to date time
def changeTimeStampToDate(node):
    if(type(node["m.releaseDate"])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node["m.releaseDate"])/1000).year
        if(node["m.title"]=='Rodan'):
            return 1956
        else:
            return hellNo
            


#Take movie nama as parameter and return the count of the rates of this movie
def getGRCount(movie): 
    nodeType1="Movie"
    relation="(m)<-[r:RATED]-()"
    q6="MATCH (m:"+nodeType1+"{title:\""+movie+"\"}),"+relation+" RETURN  count(r)"
    count=0
    #intiate session to run the query
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(q6)
    for node in nodes:
            count+=node["count(r)"]
    return count
    
def getMoviesWithRates():
    nodeyType1="Movie"
    relation="<-[r:RATED]-()"
    nodeT1A1="m.title"
    nodeT1A2="m.genre"
    nodeT1A3="m.releaseDate"
    q7="MATCH (m:"+nodeyType1+")"+relation+" RETURN  Distinct "+nodeT1A1+","+nodeT1A2+","+nodeT1A3
    #intiate session to run the query
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(q7)
    #list of genres of rated movies
    nodeT1A2s=[]
    #list of [movie name, genre, released date]
    nodeT1A1A2A3=[]
    #list of years
    y=[]
    #filling
    for node in nodes:
        nodeT1A1A2A3.append([node[nodeT1A1],node[nodeT1A2],changeTimeStampToDate(node)])
        nodeT1A2s.append(node[nodeT1A2])
        if(not(changeTimeStampToDate(node) in y)):
            y.append(changeTimeStampToDate(node))
    return nodeT1A1A2A3,list(dict.fromkeys(nodeT1A2s)),y

moviesWithRates,gens,yearsWRates=getMoviesWithRates()

#Sort the list according to year of release
moviesWithRates.sort(key=lambda x: x[2])

#Sort x in ascending order  and x is x axis data years
yearsWRates.sort()

#movieRPGY -> Y axis data list of each genre with count of rates for each year
movieRPGY=[]

#filling movieRPGY data

movieRPGY=[]
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
    movieRPGY.append([i,countPY])
    
#Laypot of the plot   
layout=go.Layout(
    title="6th Query",
    yaxis=dict(title='Count of Rates'),
    xaxis=dict(title='Year'),
    barmode='stack',
    
) 

#List of graphs for each category type is bar chart
zA=[]
for i in range(len(movieRPGY)):
    trace= go.Bar(
        x=yearsWRates,
        y=movieRPGY[i][1],
        name=gens[i]
    )
    zA.append(trace)


#Create the figure with the layout and the data of x axis and y axis
fig=go.Figure(data=zA,layout=layout)
py.offline.iplot(fig)

