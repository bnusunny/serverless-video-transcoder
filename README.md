# serverless-video-transcoding

Serverless视频转码：通过Step Functions, Lambda和EFS实现分布式视频转码。可以低成本快速提高转码速度。

初步测试结果：

1. 1小时 1080p mp4 (h264, aac) 转码为720p mp4（h264, aac): 3分50秒
2. 8分钟 1080p mp4 (h264, aac) 转码为720p mp4 (h264, aac): 1分10秒
3. 8分钟 2160p mp4 (h264, aac) 转码为720p mp4 (h264, aac): 2分23秒

Lambda成本约为: ¥0.026/分钟。例如60分钟的1080p视频转码到720p的Lambda成本为¥1.6。

目前这个项目只是demo，不建议在生成环境使用。 

部署方式：
1. 使用现有vpc，选择两个子网，记录子网ID，也可以新建VPC。
2. 在VPC中新建EFS file system和accesspoint，记录file system ID和access point ID。
3. sam build
3. sam deploy --guided 输入对应的参数

部署完成后，在视频S3桶中input/目录下上传mp4文件。系统自动触发lambda函数和Step Funcntions进行转码，输出文件在同一S3桶的output目录下。

