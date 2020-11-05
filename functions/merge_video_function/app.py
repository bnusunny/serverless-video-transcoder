import boto3
import os
import subprocess
import shutil
import re
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')
efs_path = os.environ['EFS_PATH']


def merge_video(segment_list):
    media_file = segment_list[0]

    video_prefix = media_file.split('.')[0]
    video_filename = video_prefix + '_merged.mp4'

    with open("segmentlist.txt", "w") as f:
        for segment in segment_list:
            f.write('file {} \n'.format(segment))

    # merge video segments
    cmd = ['ffmpeg', '-loglevel', 'error', '-f', 'concat', '-safe',
           '0', '-i', 'segmentlist.txt', '-c', 'copy', video_filename]

    print("merge video segments ....")
    subprocess.call(cmd)

    return video_filename


def lambda_handler(event, context):

    if len(event) == 0:
        return {}

    download_dir = event[0][0]['download_dir']
    os.chdir(download_dir)

    segment_list = []

    for segment_group in event:
        for segment in segment_group:
            segment_list.append(segment['transcoded_segment'])

    merged_file = merge_video(segment_list)

    # upload merged media to S3
    job_id = download_dir.split("/")[-1]
    object_name = re.sub('_seg_.*', '.mp4', event[0][0]['transcoded_segment'])

    bucket = os.environ['MEDIA_BUCKET']
    key = 'output/{}/{}'.format(job_id, object_name)
    s3_client.upload_file(merged_file, bucket, key)
    # delete the temp download directory
    shutil.rmtree(download_dir)

    return {
        'download_dir': download_dir,
        'input_segments': len(segment_list),
        'merged_video': merged_file,
        'create_hls': 0
    }
