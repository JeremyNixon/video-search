import os
import sys
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()


def youtube_search(query):
    # Replace with your API key
    api_key = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=50,
        type='video'
    )
    response = request.execute()

    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape-youtube.py '<search_query>'")
        sys.exit(1)
    search_query = sys.argv[1]
    youtube_search(search_query)
