# Movie_Suggestion_Bot

The Movie Suggestion Bot uses Gemini AI and Neo4j Graph Database to recommend movies based on user preferences and relationships between genres, actors, and ratings. It’s designed as a beginner-friendly project to explore AI-powered recommendations with a graph database backend.


1. Configuration
- Before running the Movie Suggestion Bot, you need to set up your credentials.
- Gemini API Key
- Create a file named key.txt in the project root.
- Paste your Gemini API key into it (only the key, nothing else).

2. Neo4j Database
- Create a Neo4j AuraDB account (or use a local Neo4j instance).
- Note down your database URI, username, and password.
- Update these values in the project configuration (graphdb.py).
- Run graphdb.py to initialize your graph in Neo4j. (python graphdb.py)

3. To run the Movie Suggestion Bot, execute:
- streamlit run prompt.py
