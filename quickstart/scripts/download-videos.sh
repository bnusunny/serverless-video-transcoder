#!/bin/bash -ex

mkdir -p videos
aws s3 cp s3://serverless-video-transcoder-pdx/videos/topgun_8m_1080p.mp4 ./videos
aws s3 cp s3://serverless-video-transcoder-pdx/videos/topgun_8m_2160p60.mp4 ./videos
aws s3 cp s3://serverless-video-transcoder-pdx/videos/beach_1h_1080p.mp4 ./videos