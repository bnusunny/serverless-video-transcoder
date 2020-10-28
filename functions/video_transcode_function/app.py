import boto3
import os
import glob
import subprocess
import shutil
import uuid
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')
efs_path = os.environ['EFS_PATH']


def generate_thumbnails(video_file):
    img_prefix = video_file.split('.')[0]
    img_filenames = img_prefix + '%03d.png'

    # extract all i-frames as thumbnails
    cmd = ['ffmpeg', '-loglevel', 'error', '-i', video_file, '-f', 'image2', '-vf',
           "select='eq(pict_type,PICT_TYPE_I)'", '-vsync', 'vfr', img_filenames]

    # create thumbnails
    print("creating thumbnails ....")
    subprocess.call(cmd)

    return glob.glob(img_prefix + '*.png')


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        object_prefix = key[:key.rfind('/') + 1]
        object_name = key[key.rfind('/') + 1:]
        download_dir = os.path.join(efs_path, str(uuid.uuid4()))
        os.mkdir(download_dir)
        os.chdir(download_dir)
        s3_client.download_file(bucket, key, object_name)
        thumbnails = generate_thumbnails(object_name)
        print("uploading thumbnails to s3 ...")
        for thumbnail in thumbnails:
            s3_client.upload_file(thumbnail, bucket, object_prefix + thumbnail,
                                  ExtraArgs={"ContentType": "image/png"})
        shutil.rmtree(download_dir)