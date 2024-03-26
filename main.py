# brew services start docker
# docker build -t ugc-search .
# docker run -d -p 8000:8000 --name ugc-search-container ugc-search

__author__ = "pdarooka1011@gmail.com (Pratham Darooka)"

from fastapi import FastAPI
from search_utils import YoutubeSearch, RedditSearch, Search
from globals import DIRECTORY
from file_handling import reset_directory

app = FastAPI()

@app.get("/search/")
def search_endpoint(user_request: str):
    reset_directory(directory=DIRECTORY)

    yt = YoutubeSearch()
    rt = RedditSearch()
    s = Search()

    # Call search_yt function
    response = s.search_parallel(rt, yt, user_request)
    return {"answer": response.encode().decode('unicode_escape')}

@app.get("/search_yt/")
def search_youtube_endpoint(user_request: str):
    reset_directory(directory=DIRECTORY)

    yt = YoutubeSearch()

    # Call search_yt function
    response = yt.search_yt(user_request)
    return {"answer": response.encode().decode('unicode_escape')}

@app.get("/search_reddit/")
def search_reddit_endpoint(user_request: str):
    reset_directory(directory=DIRECTORY)

    rt = RedditSearch()

    # Call search_reddit function
    response = rt.search_reddit(user_request, DIRECTORY)
    return {"answer": response.encode().decode('unicode_escape')}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
