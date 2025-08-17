import pandas as pd
from neo4j import GraphDatabase

url = '' #Enter your neo4j url here
username = '' #Enter your neo4j username
password = '' #Enter your password

driver=GraphDatabase.driver(url,auth=(username,password))



def create_movie(tx,row):
    tx.run("MERGE (f:Film {title: $title, year: $year, audience_score: $audience_score, profitability: $profitability, rotten_tomatoes: $rotten_tomatoes, worldwide_gross: $worldwide_gross})",
           title=row['Film'], year=int(row['Year']), audience_score=int(row['Audience score %']), profitability=row['Profitability'], rotten_tomatoes=int(row['Rotten Tomatoes %']), worldwide_gross=row['Worldwide Gross'])
    
    tx.run("MERGE(s:Studio{name:$studio})",studio=row['Lead Studio'])
    
    tx.run("MERGE(g:Genre{name:$genre})",genre=row['Genre'])

    tx.run("""
           MATCH (f:Film{title:$title}),(g:Genre{name:$genre})
           MERGE (f)-[:BELONGS_TO]->(g)
           """,title=row['Film'],genre=row['Genre'])
    
    tx.run("""
           MATCH (f:Film{title:$title}),(s:Studio{name:$studio})
           MERGE (f)-[:PRODUCED_BY]->(s)
           """,title=row['Film'],studio=row['Lead Studio']
            )
    
    
def add_data_from_csv(file_path):
    df=pd.read_csv(file_path)
    with driver.session() as session:
        for rowid,row in df.iterrows():
            session.execute_write(create_movie,row)

add_data_from_csv("movies.csv")
driver.close()