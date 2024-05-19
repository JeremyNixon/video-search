import os
import subprocess
import shutil
import time


def download_keyframes(video_id, output_folder="keyframes", target_keyframes=60, static_folder="static"):
    start_time = time.time()  # Start timing

    def get_video_duration(video_id):
        command = ['yt-dlp', '--skip-download', '--print',
                   '%(duration)s', f'https://www.youtube.com/watch?v={video_id}']
        duration = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        return int(duration.stdout.strip())

    def extract_keyframes(video_path, duration, interval, video_id):
        video_specific_folder = os.path.join(output_folder, video_id)
        if os.path.exists(video_specific_folder):
            # Delete the folder if it exists
            shutil.rmtree(video_specific_folder)
        os.makedirs(video_specific_folder, exist_ok=True)
        # Ensure the static folder exists
        os.makedirs(static_folder, exist_ok=True)

        for index, i in enumerate(range(0, duration, interval)):
            keyframe_filename = f"keyframe_{index}_{i}.jpg"
            keyframe_path = os.path.join(
                video_specific_folder, keyframe_filename)
            subprocess.run(['ffmpeg', '-ss', str(i), '-i', video_path, '-frames:v', '1', keyframe_path],
                           stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # New code to copy and rename the keyframe
            new_filename = f"yt_{video_id}_{keyframe_filename}"
            new_filepath = os.path.join(static_folder, new_filename)
            # Copy and rename the file
            shutil.copy(keyframe_path, new_filepath)

    # Download the entire video
    video_path = f"{video_id}.mp4"
    subprocess.run(['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                   '-o', video_path, f'https://www.youtube.com/watch?v={video_id}'],
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    duration = get_video_duration(video_id)
    print(f"video duration is {duration} seconds")

    # Calculate interval to achieve target keyframes
    interval = duration // target_keyframes
    print(f"Interval between keyframes is {interval} seconds")

    # Extract keyframes
    extract_keyframes(video_path, duration, interval, video_id)

    # Remove the downloaded video file
    os.remove(video_path)

    end_time = time.time()  # End timing
    # Print the duration of the operation
    print(f"Operation completed in {end_time - start_time:.2f} seconds")


# Example usage
video_id = "1lCOgFPtaZ4"
download_keyframes(video_id)
