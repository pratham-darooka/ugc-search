from googleapiclient.discovery import build
from file_handling import save_transcript_to_file, save_post_to_file
from query_rewriting import rewrite_yt_query, rewrite_reddit_query
from rag import search, search_rddt, search_ytb
from globals import DIRECTORY, GOOGLE_DEV_KEY, REDDIT_USER_AGENT, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, GOOGLE_CUSTOM_SEARCH_ENGINE_KEY
from logger import logger
import json
import re
import praw


class YoutubeSearch:
    def _get_videos(self, query) -> dict:
        from youtube_search import YoutubeSearch

        res = YoutubeSearch(query, max_results=10).to_json()

        return json.loads(res)

    def _get_transcript(self, video_id, video_object):
        indian_languages = [
            "en",
            "as",  # Assamese
            "bho",  # Bhojpuri
            "bn",  # Bangla
            "gu",  # Gujarati
            "hi",  # Hindi
            "kn",  # Kannada
            "kok",  # Konkani
            "ks",  # Kashmiri
            "ml",  # Malayalam
            "mr",  # Marathi
            "mni",  # Manipuri
            "ne",  # Nepali
            "or",  # Odia
            "pa",  # Punjabi
            "sa",  # Sanskrit
            "sd",  # Sindhi
            "ta",  # Tamil
            "te",  # Telugu
            "ur"  # Urdu
        ]
        """Fetch transcript for a given YouTube video and save to a file."""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi

            # Fetch the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=indian_languages)
            # Convert transcript to a single string
            transcript_text = "\n".join([t['text'] for t in transcript])

            # Assuming video_object is a dictionary containing 'title' and 'channel' keys
            video_data = {
                "title": video_object['title'],
                "channel": video_object['channel'],
                "transcript": transcript_text
            }

            save_transcript_to_file(video_data=video_data, directory=DIRECTORY)
        except Exception as e:
            logger.exception(f"Error fetching transcript: {e}")

    def _get_relevant_youtube_transcripts(self, user_request: str) -> None:
        logger.info(f"User Request: {user_request}")

        search_results = self._get_videos(rewrite_yt_query(user_request))['videos']

        for search_result in search_results:
            video_id = search_result["id"]
            logger.debug(f"--> {video_id}")
            self._get_transcript(video_id, search_result)

    def search_yt(self, user_request: str) -> str:
        self._get_relevant_youtube_transcripts(user_request)
        return search_ytb(user_request)

class RedditSearch:
    def _get_reddit_posts(self, query: str) -> dict:
        service = build(
            "customsearch", "v1", developerKey=GOOGLE_DEV_KEY
        )
        logger.info(f"Fetching Reddit Posts for: {query}")
        res = (
            service.cse()
            .list(
                q=query,
                cx=GOOGLE_CUSTOM_SEARCH_ENGINE_KEY,
            )
            .execute()
        )
        logger.debug("Results Obtained:")
        logger.debug(res)
        return res

    def _get_post_content_and_comments(self, url: str) -> tuple:
        # Initialize the Reddit API wrapper
        reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                             client_secret=REDDIT_CLIENT_SECRET,
                             user_agent=REDDIT_USER_AGENT)

        # Extract submission ID from the URL
        submission_id = url.split('/')[-3]
        # Fetch the submission (post)
        submission = reddit.submission(id=submission_id)
        # Extract post content
        post_title = url.split('/')[-2]
        post_content = submission.selftext

        # Extract comments
        comments = []
        submission.comments.replace_more(limit=None)  # Retrieve all comments
        for comment in submission.comments.list():
            comments.append(comment.body)

        return post_title, post_content, comments

    def _get_relevant_reddit_posts(self, user_request: str) -> None:
        logger.info(f"User Request: {user_request}")

        query = rewrite_reddit_query(user_request)
        search_results = self._get_reddit_posts(query=query)['items']

        for search_result in search_results:
            url = search_result['link']

            post_title, post_content, comments = self._get_post_content_and_comments(url)
            logger.debug(f"--> {post_title}")

            save_post_to_file(url, post_title, post_content, comments, directory=DIRECTORY)

    def search_reddit(self, user_request: str, directory: str) -> str:
        self._get_relevant_reddit_posts(user_request)
        return search_rddt(user_request)

class Search:
    def search(self, rddt: RedditSearch, yt: YoutubeSearch, query):
        rddt._get_relevant_reddit_posts(query)
        yt._get_relevant_youtube_transcripts(query)
        
        return search(query)

    def search_parallel(self, rddt: RedditSearch, yt: YoutubeSearch, query):
        from multiprocessing import Process

        p1 = Process(target=rddt._get_relevant_reddit_posts, args=(query,))
        p2 = Process(target=yt._get_relevant_youtube_transcripts, args=(query,))
        
        # Start both processes
        p1.start()
        p2.start()
        
        # Wait for both processes to finish
        p1.join()
        p2.join()
        
        # Your return statement seems to be calling the search method recursively, which might be incorrect.
        # Assuming you want to return some search results, you might want to return something else here.
        return search(query)