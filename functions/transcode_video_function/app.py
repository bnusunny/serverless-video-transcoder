import os
import re
import subprocess
from urllib.parse import unquote_plus


def transcode_segment(video_file):
    img_prefix = video_file.split('.')[0]
    img_filenames = img_prefix + '_720p.mp4'

    # extract all i-frames as thumbnails
    cmd = ['ffmpeg', '-loglevel', 'error', '-i', video_file, '-vf', "scale=-1:720", '-c:a', 'copy', img_filenames]

    # create thumbnails
    print("trancoding the segment: " + video_file)
    subprocess.call(cmd)

    return img_filenames


def lambda_handler(event, context):
    download_dir = event['download_dir']
    os.chdir(download_dir)
    video_segment = event['video_segments']
    segment_order = video_segment['segment_order']

    result = transcode_segment(video_segment['segment_file'])

    return {
        'download_dir': download_dir,
        'transcoded_segment': result,
        'segment_order': segment_order
    }
