#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

# Query 1
query1="Match(m:Movie)return m.title,m.releaseDate,m.genre,m.runtime"
movieYearGenre=[]
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query1)
for node in nodes:
    if(type(node["m.releaseDate"])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node["m.releaseDate"])/1000).year
        if(node["m.title"]=='Rodan'):
            movieYearGenre.append([node["m.title"],1956,node["m.genre"],node["m.runtime"]])
        else:
            movieYearGenre.append([node["m.title"],hellNo,node["m.genre"],node["m.runtime"]])
movieYearGenre.sort(key=lambda x: x[1])
year=[]
countMovies=[]
i=movieYearGenre[0][1]
j=0
print(i)
while(i<=movieYearGenre[len(movieYearGenre)-1][1]):
    count=0
    while(j<len(movieYearGenre)and i==movieYearGenre[j][1]):
        count+=1
        j+=1
    year.append(i)
    countMovies.append(count)
    i+=1

print(type(movieYearGenre[0][3]))
layout=go.Layout(
    title="First Query",
    yaxis=dict(title='Count'),
    xaxis=dict(title='Year'))



#Line 

trace1=go.Scatter(
    x=year,
    y=countMovies,
    mode='lines'

)

#Scatter

trace2=go.Scatter(
    x=year,
    y=countMovies,
    mode = 'markers'

)

#Scatter and Lines

trace3=go.Scatter(
    x=year,
    y=countMovies,
    mode='lines+markers'
)
fig=go.Figure(data=[trace3],layout=layout)
py.offline.iplot(fig)


# In[ ]:





# In[3]:


#Second Query

query2="MATCH (a:Actor),(m:Movie),(a)-[r:ACTS_IN]->(m) RETURN a.name,count(m) ORDER BY count(m)"
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query2)
result=[]
actors=[]
noOfMovies=[]
for node in nodes:
    actors.append(node["a.name"])
    noOfMovies.append(node["count(m)"])



layout5=go.Layout(
    title="Second Query",
    yaxis=dict(title='Total count of Movies'),
    xaxis=dict(title='Actors')
)


trace5=go.Bar(
    x=actors,
    y=noOfMovies,

)
trace = go.Scatter(
    x = actors,
    y = noOfMovies,
    mode='lines'
)



fig=go.Figure(data=[trace],layout=layout5)
py.offline.iplot(fig)




# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[8]:


#Query 3

def getListOfActorMovies(actor): 
        q3="Match(a:Actor{name:\""+actor+"\"}),(m:Movie),(a)-[:ACTS_IN]->(m) return m.title,m.releaseDate"
        with driver.session() as graphDB_Session:
            nodes = graphDB_Session.run(q3)
        movies=[]
        for node in nodes:
            movies.append([node["m.title"],datetime.datetime.fromtimestamp(int(node["m.releaseDate"])/1000).year])
        movies.sort(key=lambda x: x[1])
        return movies

query4="MATCH (a:Actor),(m:Movie),(a)-[r:ACTS_IN]->(m) RETURN a.name,count(m) ORDER BY count(m) Desc Limit 10"
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query4)
topActors=[]
tMovieNo=[]
countPerY=[]
for node in nodes:
    topActors.append(node["a.name"])
    tMovieNo.append(node["count(m)"])

actorCountYear=[]
for i in topActors:
    moviesofA=getListOfActorMovies(i[0])
    countYear=[]
    for j in year:
        count=0
        for k in moviesofA:
            if k[1]==j:
                count+=1
        countYear.append([count,j])
    actorCountYear.append([i,countYear])

    
        

# layout5=go.Layout(
#     title="Third Query",
#     yaxis=dict(title='Total count and count per year'),
#     xaxis=dict(title='Actors')
# )


# trace5=go.Bar(
#     x=topActors,
#     y=tMovieNoAt,

# )



# fig=go.Figure(data=[trace5],layout=layout5)
# py.offline.iplot(fig)


# In[4]:


#Query 4

query5="Match(m:Movie)return Distinct m.genre"
with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(query5)

genres=[]
for node in nodes:
    genres.append(node["m.genre"])
genreYearsCounts=[]
for i in genres:
    j=movieYearGenre[0][1]
    yearsCounts=[]
    k=0
    while j<=movieYearGenre[len(movieYearGenre)-1][1]:
        count=0
        while k<len(movieYearGenre) and j==movieYearGenre[k][1]:
            if movieYearGenre[k][2]==i:
                count+=1
            k+=1
        yearsCounts.append(count)
        j+=1
    genreYearsCounts.append([i,yearsCounts])
print(genres)



layout=go.Layout(
    title="Fouth Query",
    yaxis=dict(title='Count&Geners'),
    xaxis=dict(title='Year'))

trace1 = go.Bar(
    x=year,
    y=genreYearsCounts[0][1],
    name='Film Noir'
)
trace2 = go.Bar(
    x=year,
    y=genreYearsCounts[1][1],
    name='Musical'
)
trace3 = go.Bar(
    x=year,
    y=genreYearsCounts[2][1],
    name='Eastern'
)
trace4 = go.Bar(
    x=year,
    y=genreYearsCounts[3][1],
    name='History'
)
trace5 = go.Bar(
    x=year,
    y=genreYearsCounts[4][1],
    name='Thriller'
)
trace6 = go.Bar(
    x=year,
    y=genreYearsCounts[5][1],
    name='short'
)
trace7 = go.Bar(
    x=year,
    y=genreYearsCounts[6][1],
    name='Music'
)
trace8 = go.Bar(
    x=year,
    y=genreYearsCounts[7][1],
    name='Suspense'
)
trace9 = go.Bar(
    x=year,
    y=genreYearsCounts[8][1],
    name='Drama'
)
trace10 = go.Bar(
    x=year,
    y=genreYearsCounts[9][1],
    name='Disaster'
)
trace11 = go.Bar(
    x=year,
    y=genreYearsCounts[10][1],
    name='Western'
)
trace12 = go.Bar(
    x=year,
    y=genreYearsCounts[11][1],
    name='Erotic'
)
trace13 = go.Bar(
    x=year,
    y=genreYearsCounts[12][1],
    name='Adventure'
)
trace14 = go.Bar(
    x=year,
    y=genreYearsCounts[13][1],
    name='Road Movie'
)
trace15 = go.Bar(
    x=year,
    y=genreYearsCounts[14][1],
    name='Indie'
)
trace16 = go.Bar(
    x=year,
    y=genreYearsCounts[15][1],
    name='Mystery'
)
trace17 = go.Bar(
    x=year,
    y=genreYearsCounts[16][1],
    name='Science Fiction'
)
trace18 = go.Bar(
    x=year,
    y=genreYearsCounts[17][1],
    name='Horror'
)
trace19 = go.Bar(
    x=year,
    y=genreYearsCounts[18][1],
    name='British'
)
trace20 = go.Bar(
    x=year,
    y=genreYearsCounts[19][1],
    name='Documentry'
)
trace21 = go.Bar(
    x=year,
    y=genreYearsCounts[20][1],
    name='None'
)
trace22 = go.Bar(
    x=year,
    y=genreYearsCounts[21][1],
    name='Animation'
)

trace23 = go.Bar(
    x=year,
    y=genreYearsCounts[22][1],
    name='Family'
)
trace24 = go.Bar(
    x=year,
    y=genreYearsCounts[23][1],
    name='War'
)
trace25 = go.Bar(
    x=year,
    y=genreYearsCounts[24][1],
    name='Sporting Event'
)
trace26 = go.Bar(
    x=year,
    y=genreYearsCounts[25][1],
    name='Romance'
)
trace27 = go.Bar(
    x=year,
    y=genreYearsCounts[26][1],
    name='Crime'
)
trace28 = go.Bar(
    x=year,
    y=genreYearsCounts[27][1],
    name='Action'
)
trace29 = go.Bar(
    x=year,
    y=genreYearsCounts[28][1],
    name='Comedy'
)
trace30 = go.Bar(
    x=year,
    y=genreYearsCounts[29][1],
    name='Fantasy'
)
trace31 = go.Bar(
    x=year,
    y=genreYearsCounts[30][1],
    name='Sports Film'
)

data = [trace1, trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12,trace13,trace14,trace15,trace16,trace17,trace18,trace20,trace21,trace22,trace23,trace24,trace25,trace26,trace27,trace28,trace29,trace30,trace31]
layout = go.Layout(
    barmode='stack'
)


fig=go.Figure(data=data,layout=layout)
py.offline.iplot(fig)







# In[ ]:





# In[ ]:





# In[5]:


#Query 5
avTimeOverYear=[]
j=movieYearGenre[0][1]
k=0
while j<=movieYearGenre[len(movieYearGenre)-1][1]:
    sum=0
    count=0
    while k<len(movieYearGenre) and j==movieYearGenre[k][1]:
        count+=1
        if(type(movieYearGenre[k][3])==int and movieYearGenre[k][3]>0):
            sum+=movieYearGenre[k][3]
        k+=1
    if(count==0):
        count=1
    avTimeOverYear.append(sum/count)  
    j+=1
    

layout=go.Layout(
    title="Fifth Query",
    yaxis=dict(title='Average running time'),
    xaxis=dict(title='Year')) 
trace = go.Scatter(
    x=year,
    y=avTimeOverYear,
)
fig=go.Figure(data=[trace],layout=layout)
py.offline.iplot(fig)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[15]:


#Query 6
avTimeOverYearGs=[]
for i in genres:
    avTimeOverYearG=[]
    k=0
    j=movieYearGenre[0][1]
    while j<=movieYearGenre[len(movieYearGenre)-1][1]:
        sum=0
        count=0
        while k<len(movieYearGenre) and j==movieYearGenre[k][1]:
            if movieYearGenre[k][2]==i:
                count+=1
                if(type(movieYearGenre[k][3])==int and movieYearGenre[k][3]>0):
                    sum+=movieYearGenre[k][3]
            k+=1
        if(count==0):
            count=1
        avTimeOverYearG.append(sum/count)  
        j+=1
    avTimeOverYearGs.append([i,avTimeOverYearG])

layout=go.Layout(
    title="Query 6",
    yaxis=dict(title='avgRunTime&Geners'),
    xaxis=dict(title='Year'))

trace1 = go.Bar(
    x=year,
    y=avTimeOverYearGs[0][1],
    name='Film Noir'
)
trace2 = go.Bar(
    x=year,
    y=avTimeOverYearGs[1][1],
    name='Musical'
)
trace3 = go.Bar(
    x=year,
    y=avTimeOverYearGs[2][1],
    name='Eastern'
)
trace4 = go.Bar(
    x=year,
    y=avTimeOverYearGs[3][1],
    name='History'
)
trace5 = go.Bar(
    x=year,
    y=avTimeOverYearGs[4][1],
    name='Thriller'
)
trace6 = go.Bar(
    x=year,
    y=avTimeOverYearGs[5][1],
    name='short'
)
trace7 = go.Bar(
    x=year,
    y=avTimeOverYearGs[6][1],
    name='Music'
)
trace8 = go.Bar(
    x=year,
    y=avTimeOverYearGs[7][1],
    name='Suspense'
)
trace9 = go.Bar(
    x=year,
    y=avTimeOverYearGs[8][1],
    name='Drama'
)
trace10 = go.Bar(
    x=year,
    y=avTimeOverYearGs[9][1],
    name='Disaster'
)
trace11 = go.Bar(
    x=year,
    y=avTimeOverYearGs[10][1],
    name='Western'
)
trace12 = go.Bar(
    x=year,
    y=avTimeOverYearGs[11][1],
    name='Erotic'
)
trace13 = go.Bar(
    x=year,
    y=avTimeOverYearGs[12][1],
    name='Adventure'
)
trace14 = go.Bar(
    x=year,
    y=avTimeOverYearGs[13][1],
    name='Road Movie'
)
trace15 = go.Bar(
    x=year,
    y=avTimeOverYearGs[14][1],
    name='Indie'
)
trace16 = go.Bar(
    x=year,
    y=avTimeOverYearGs[15][1],
    name='Mystery'
)
trace17 = go.Bar(
    x=year,
    y=avTimeOverYearGs[16][1],
    name='Science Fiction'
)
trace18 = go.Bar(
    x=year,
    y=avTimeOverYearGs[17][1],
    name='Horror'
)
trace19 = go.Bar(
    x=year,
    y=avTimeOverYearGs[18][1],
    name='British'
)
trace20 = go.Bar(
    x=year,
    y=avTimeOverYearGs[19][1],
    name='Documentry'
)
trace21 = go.Bar(
    x=year,
    y=avTimeOverYearGs[20][1],
    name='None'
)
trace22 = go.Bar(
    x=year,
    y=avTimeOverYearGs[21][1],
    name='Animation'
)

trace23 = go.Bar(
    x=year,
    y=avTimeOverYearGs[22][1],
    name='Family'
)
trace24 = go.Bar(
    x=year,
    y=avTimeOverYearGs[23][1],
    name='War'
)
trace25 = go.Bar(
    x=year,
    y=avTimeOverYearGs[24][1],
    name='Sporting Event'
)
trace26 = go.Bar(
    x=year,
    y=avTimeOverYearGs[25][1],
    name='Romance'
)
trace27 = go.Bar(
    x=year,
    y=avTimeOverYearGs[26][1],
    name='Crime'
)
trace28 = go.Bar(
    x=year,
    y=avTimeOverYearGs[27][1],
    name='Action'
)
trace29 = go.Bar(
    x=year,
    y=avTimeOverYearGs[28][1],
    name='Comedy'
)
trace30 = go.Bar(
    x=year,
    y=avTimeOverYearGs[29][1],
    name='Fantasy'
)
trace31 = go.Bar(
    x=year,
    y=avTimeOverYearGs[30][1],
    name='Sports Film'
)

data = [trace1, trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12,trace13,trace14,trace15,trace16,trace17,trace18,trace20,trace21,trace22,trace23,trace24,trace25,trace26,trace27,trace28,trace29,trace30,trace31]
layout = go.Layout(
    barmode='stack'
)


fig=go.Figure(data=data,layout=layout)
py.offline.iplot(fig)


# In[12]:


#Query 7

rygs=[]
def getGRCount(movie): 
        q6="MATCH (m:Movie{title:\""+movie+"\"})<-[r:RATED]-() RETURN  count(r)"
        count=0
        with driver.session() as graphDB_Session:
            nodes = graphDB_Session.run(q6)
        for node in nodes:
            count+=node["count(r)"]
        return count

for i in genres:
    j=movieYearGenre[0][1]
    k=0
    ryg=[]
    while j<=movieYearGenre[len(movieYearGenre)-1][1]:
        count =0
        while k< len(movieYearGenre)and movieYearGenre[k][1]==j:
            if(movieYearGenre[k][2]==i):
                count+=getGRCount(movieYearGenre[k][0])             
            k+=1
            ryg.append(count)
        j+=1
        rygs.append([i,ryg])
        
                
    


# In[35]:


def changeTimeStampToDate(node):
    if(type(node["m.releaseDate"])==str):
        hellNo=datetime.datetime.fromtimestamp(int(node["m.releaseDate"])/1000).year
        if(node["m.title"]=='Rodan'):
            return 1956
        else:
            return hellNo
            


def getGRCount(movie): 
        q6="MATCH (m:Movie{title:\""+movie+"\"})<-[r:RATED]-() RETURN  count(r)"
        count=0
        with driver.session() as graphDB_Session:
            nodes = graphDB_Session.run(q6)
            for node in nodes:
                count+=node["count(r)"]
        return count
    
def getMoviesWithRates():
    moviesNYGWithRates=[]
    gens=[]
    yearsWRates=[]
    q7="MATCH (m:Movie)<-[r:RATED]-() RETURN  Distinct m.title,m.genre,m.releaseDate"
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(q7)
    for node in nodes:
        moviesNYGWithRates.append([node["m.title"],node["m.genre"],changeTimeStampToDate(node)])
        gens.append(node["m.genre"])
        if(not(changeTimeStampToDate(node) in yearsWRates)):
            yearsWRates.append(changeTimeStampToDate(node))
    return moviesNYGWithRates,list(dict.fromkeys(gens)),yearsWRates

moviesWithRates,gens,yearsWRates=getMoviesWithRates()
moviesWithRates.sort(key=lambda x: x[2])
yearsWRates.sort() 
print(yearsWRates)


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
    
    
layout=go.Layout(
    title="7th Query",
    yaxis=dict(title='Count of Rates'),
    xaxis=dict(title='Year'),
    barmode='stack',
    
) 

trace71 = go.Bar(
   x=yearsWRates,
   y=movieRPGY[0][1],
   name='Action'
)
trace72 = go.Bar(
   x=yearsWRates,
   y=movieRPGY[1][1],
   name='Drama'
)
trace73 = go.Bar(
   x=yearsWRates,
   y=movieRPGY[2][1],
   name='Animation'
)
trace74 = go.Bar(
   x=yearsWRates,
   y=movieRPGY[3][1],
   name='Crime'
)
trace75 = go.Bar(
   x=yearsWRates,
   y=movieRPGY[4][1],
   name='Comedy'
)
trace76 = go.Bar(
   x=yearsWRates,
   y=movieRPGY[5][1],
   name='None'
)
fig=go.Figure(data=[trace71,trace72,trace73,trace74,trace75,trace76],layout=layout)
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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[22]:


count=0
print(len(movieYearGenre))
for i in range (len(movieYearGenre)):
    print("Hi->"+str(i))
    q6="MATCH (m:Movie{title:\""+movieYearGenre[i][0]+"\"})<-[r:RATED]-() RETURN  count(r)"
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(q6)
    for node in nodes:
        count+=node["count(r)"]
    print(count)
        
        
    
    


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





# In[36]:





# In[37]:






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





# In[ ]:





# In[ ]:





# In[87]:


readable = datetime.datetime.fromtimestamp(882486000000/1000).year
print(type(readable))


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




