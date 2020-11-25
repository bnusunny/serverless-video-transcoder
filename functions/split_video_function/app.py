import boto3
import os
import re
import glob
import subprocess
from urllib.parse import unquote_plus
from botocore.config import Config

s3_client = boto3.client('s3', os.environ['AWS_REGION'], config=Config(s3={'addressing_style': 'path'}))
efs_path = os.environ['EFS_PATH']
parallel_groups = int(os.environ['PARALLEL_GROUPS'])
segment_time = os.environ['SEGMENT_TIME']

def slice_video(bucket, key, video_file):
    segment_prefix = video_file.split('.')[0]
    segment_filename = segment_prefix + '_seg_%03d.mp4'
    video_file_presigned_url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=30
    )

    # slice video to segments.
    cmd = ['ffmpeg', '-loglevel', 'error', '-i', video_file_presigned_url, '-map', '0', '-c', 'copy',
           '-f', 'segment', '-segment_time', segment_time, '-reset_timestamps', '1', segment_filename]

    print("slice the video into segments ....")
    subprocess.call(cmd)

    segment_files = glob.glob(segment_prefix + '_seg_*.mp4')

    segement_list = [None]*len(segment_files)
    for segment_file in segment_files:
        segment_order = int(re.search('_(\d+)\.', segment_file).group(1))
        segement_list[segment_order] = ({
            'segment_order': segment_order,
            'segment_file': segment_file
        })

    return segement_list


def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']
    object_prefix = event['object_prefix']
    object_name = event['object_name']
    download_dir = os.path.join(efs_path, event['job_id'])
    try:
        os.mkdir(download_dir)
    except FileExistsError as error:
        print('directory exist')

    os.chdir(download_dir)
    video_segments = slice_video(bucket, key, object_name)
    results = [
        {
            "download_dir": download_dir,
            'video_segments': []
        }
    ] * parallel_groups
    group_size = int(len(video_segments)/parallel_groups + 1)
    groups = [video_segments[x:x+group_size]
              for x in range(0, len(video_segments), group_size)]

    for index in range(0, len(groups)):
        results[index] = (
            {
                "download_dir": download_dir,
                'video_segments': groups[index]
            }
        )

    print("save media metadata to dynamodb ...")
    # TODO save state to ddb

    return results
