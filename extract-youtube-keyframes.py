import os
import subprocess

import os
import subprocess


def download_keyframes(video_id, output_folder="keyframes", target_keyframes=60):
    # Determine the number of keyframes based on the video duration
    def get_video_duration(video_id):
        command = ['yt-dlp', '--skip-download', '--print',
                   '%(duration)s', f'https://www.youtube.com/watch?v={video_id}']
        duration = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        return int(duration.stdout.strip())

    # Download and extract keyframes
    def download_segment(start, index, video_id):
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        segment_filename = f"segment_{index}.mp4"
        yt_dlp_args = f"-ss {start} -t 1 -avoid_negative_ts make_zero"  # Download only 1 second
        # Download segment
        subprocess.run([
            'yt-dlp', '-f', 'bestvideo[ext=mp4]', '--external-downloader', 'ffmpeg',
            '--external-downloader-args', yt_dlp_args, '-o', segment_filename, video_url
        ])
        # Extract keyframes
        video_specific_folder = os.path.join(output_folder, video_id)
        os.makedirs(video_specific_folder, exist_ok=True)
        keyframe_filename = os.path.join(
            video_specific_folder, f"keyframe_{index}_{start}.jpg")
        # Extract only the first keyframe
        subprocess.run(['ffmpeg', '-i', segment_filename, '-vf',
                       "select='eq(pict_type\\,I)'", '-vframes', '1', keyframe_filename])
        # Optionally remove the segment file after extracting keyframes
        os.remove(segment_filename)

    duration = get_video_duration(video_id)
    print(f"video duration is {duration} seconds")

    # Calculate interval to achieve target keyframes
    interval = duration // target_keyframes
    print(f"Interval between segments is {interval} seconds")

    for i in range(0, duration, interval):
        download_segment(i, i // interval, video_id)

        # Example usage
video_id = "1lCOgFPtaZ4"
download_keyframes(video_id)
