# serverless-video-transcoder

Serverless视频转码：通过Step Functions, Lambda和EFS实现分布式视频转码。适用于按需快速视频转码。Serverless架构，无需管理计算集群。 

![](./images/serverless-video-transcoder.png)

## 测试结果

1. [测试文件](https://serverless-video-transcoder-bjs.s3.cn-north-1.amazonaws.com.cn/videos/beach_1h_1080p.mp4) 1小时 1080p mp4 (h264, aac) 转码为720p mp4（h264, aac): 3分50秒
2. [测试文件](https://serverless-video-transcoder-bjs.s3.cn-north-1.amazonaws.com.cn/videos/topgun_8m_1080p.mp4) 8分钟 1080p mp4 (h264, aac) 转码为720p mp4 (h264, aac): 1分10秒
3. [测试文件](https://serverless-video-transcoder-bjs.s3.cn-north-1.amazonaws.com.cn/videos/topgun_8m_2160p60.mp4) 8分钟 2160p mp4 (h264, aac) 转码为720p mp4 (h264, aac): 2分23秒



## 部署方式

使用Quickstart/templates目录下的CloudFormation模版，可以快速完成部署。这个模版会新建带有两个公有子网的VPC, S3和DynamoDB Endpoints, S3存储桶，DyanomDB表，EFS文件系统, Lambda函数和Step Functions状态机。

|           Region            |                     Launch Stack in VPC                      |
| :-------------------------: | :----------------------------------------------------------: |
| **北京** (cn-north-1)   | [![cloudformation-launch-stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.amazonaws.cn/cloudformation/home?region=cn-north-1#/stacks/new?stackName=serverless-video-transcoder&templateURL=https://serverless-video-transcoder-cn-north-1.s3.cn-north-1.amazonaws.com.cn/templates/template.yaml) |
| **宁夏** (cn-northwest-1) | [![cloudformation-launch-stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.amazonaws.cn/cloudformation/home?region=cn-northwest-1#/stacks/new?stackName=serverless-video-transcoder&templateURL=https://aws-quickstart-cn.s3.cn-northwest-1.amazonaws.com.cn/serverless-video-transcoder/template.yaml) |
| **N. Virginia** (us-east-1) | [![cloudformation-launch-stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=serverless-video-transcoder&templateURL=https://serverless-video-transcoder.s3.amazonaws.com/templates/template.yaml) |
| **Tokyo** (ap-northeast-1) | [![cloudformation-launch-stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=serverless-video-transcoder&templateURL=https://serverless-video-transcoder-ap-northeast-1.s3-ap-northeast-1.amazonaws.com/templates/template.yaml) |



## 使用方法

部署完成后，在视频S3桶中input/目录下上传mp4文件。系统自动触发lambda函数和Step Funcntions进行转码，输出文件在同一S3桶的output目录下。

