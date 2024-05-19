import os
import subprocess


def download_keyframes(video_id, output_folder="keyframes", target_keyframes=60):
    def get_video_duration(video_id):
        command = ['yt-dlp', '--skip-download', '--print',
                   '%(duration)s', f'https://www.youtube.com/watch?v={video_id}']
        duration = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        return int(duration.stdout.strip())

    def extract_keyframes(video_path, duration, interval, video_id):
        video_specific_folder = os.path.join(output_folder, video_id)
        os.makedirs(video_specific_folder, exist_ok=True)
        for index, i in enumerate(range(0, duration, interval)):
            keyframe_filename = os.path.join(
                video_specific_folder, f"keyframe_{index}_{i}.jpg")
            subprocess.run(['ffmpeg', '-ss', str(i), '-i',
                           video_path, '-frames:v', '1', keyframe_filename])

    # Download the entire video
    video_path = f"{video_id}.mp4"
    subprocess.run(['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                   '-o', video_path, f'https://www.youtube.com/watch?v={video_id}'])

    duration = get_video_duration(video_id)
    print(f"video duration is {duration} seconds")

    # Calculate interval to achieve target keyframes
    interval = duration // target_keyframes
    print(f"Interval between keyframes is {interval} seconds")

    # Extract keyframes
    extract_keyframes(video_path, duration, interval, video_id)

    # Remove the downloaded video file
    os.remove(video_path)


# Example usage
video_id = "1lCOgFPtaZ4"
download_keyframes(video_id)
