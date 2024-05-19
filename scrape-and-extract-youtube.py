import threading
from concurrent.futures import ThreadPoolExecutor
from extract_youtube_keyframes import download_keyframes
from scrape_youtube import youtube_search
import time  # Import time module


def extract_keyframes_concurrently(video_id):
    with semaphore:
        download_keyframes(video_id)


def main(query):
    start_time = time.time()  # Start timing

    video_ids = youtube_search(query)
    semaphore = threading.Semaphore(5)  # Allows up to 5 concurrent threads

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(extract_keyframes_concurrently, video_ids)

    end_time = time.time()  # End timing
    # Print execution time
    print(f"Execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    query = "example search query"
    main(query)
