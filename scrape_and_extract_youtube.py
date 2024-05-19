import threading
from concurrent.futures import ThreadPoolExecutor
from extract_youtube_keyframes import download_keyframes
from scrape_youtube import youtube_search
import time
import sys

def extract_keyframes_concurrently(video_id, semaphore):
    with semaphore:
        print(f"Downloading keyframes for video ID: {video_id}")
        download_keyframes(video_id)

def main(query):
    start_time = time.time()  # Start timing

    video_ids = youtube_search(query)
    print(video_ids)
    input("Press Enter to continue...")
    semaphore = threading.Semaphore(5)  # Allows up to 5 concurrent threads

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Pass semaphore as part of the function arguments
        executor.map(lambda vid: extract_keyframes_concurrently(vid, semaphore), video_ids)

    end_time = time.time()  # End timing
    # Print execution time
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_and_extract_youtube.py '<search_query>'")
        sys.exit(1)
    search_query = sys.argv[1]
    main(search_query)
