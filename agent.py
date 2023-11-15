# LangChain
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.utilities.requests import TextRequestsWrapper
from langchain.document_loaders import AsyncChromiumLoader
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.embeddings import GooglePalmEmbeddings
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.agents import Tool
from langchain.llms import GooglePalm

#Other
from urllib.parse import quote
from bs4 import BeautifulSoup
import lyricsgenius
import requests
import json
import os
import re

with open("keys.json", "r") as api_keys_f: 
  api_keys = json.loads(api_keys_f.read())
  for key in api_keys.keys():
    os.environ[key] = api_keys[key]

del api_keys_f, api_keys, key

search = GoogleSerperAPIWrapper()
genius = lyricsgenius.Genius()

def query_music(x):
  site_data = requests.get(f"https://api.genius.com/search?q={quote(x)}&access_token={os.environ['GENIUS_ACCESS_TOKEN']}").text
  music_json = json.loads(site_data)["response"]["hits"][0]["result"]
  return [music_json]

def about_lyrics(x):
  #music = query_music(x)
  site_data = requests.get(f"https://api.genius.com/referents?song_id={x}&access_token={os.environ['GENIUS_ACCESS_TOKEN']}").text
  annotations_json = json.loads(site_data)
  return [
      {"music_fragment":annotation["fragment"],
      "fragment_interpretation":[interpretation["body"]["dom"]["children"][0]["children"] for interpretation in annotation["annotations"]][0][0]}
      for annotation in annotations_json["response"]["referents"][0:5]]

serper_tool = Tool(
        name="Search Answer",
        func=search.run,
        description="useful for when you need to ask with recent information",
)

search_music = Tool(
        name="Genius Querry",
        func= query_music,
        description="useful need to know about a specific music",
)

search_annotations = Tool(
        name="Anotations Querry",
        func= about_lyrics,
        description="useful need to know more about the lyrics and meaning of an specific music giving the genius music id",
)


## Defining the agent
llm = GooglePalm()
llm.temperature = 0.1

tools = load_tools(
    ["llm-math", "requests_get"],
    llm=llm
)
tools += [serper_tool, search_music, search_annotations]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.run("What you have to say about Numb by Linkin Park?")