# 无服务器转码动手实验

通过这次实验，您将部署serverless-video-transcoder，运行多个测试，实际体验无服务器转码的便捷和速度。

![](../images/serverless-video-transcoder.png)

## 实验环境

实验需要使用AWS账号和管理员用户。 您可以使用自己的AWS账号，或是使用AWS提供的实验账号。

### Cloud9实例

在AWS Console中选择“俄勒冈州”区域，在服务菜单中选择“Cloud9”。
![](img/1.png)
在Cloud9 Console中选择“Create environment”, 输入name，例如“workshop"，点击“Next Step”。
![](img/3.png)

在configuration页面，instance type选择m5.large, Platform选择Amazon Linux 2, 点击“Next Step”
![](img/4.png)

确认参数设置正确，点击“Create Enviroment”, 开始创建cloud9实例。等待一会儿，cloud9实例创建完成后，可以看到下面的界面。 
![](img/5.png)

### 下载项目代码

打开一个新的Terminal. 
![](img/6.png)

下载代码

```
git clone https://github.com/bnusunny/serverless-video-transcoder.git

cd serverless-video-transcoder/
```

### 部署项目

通过sam部署项目

```
sam build
```
![](img/7.png)

```
sam deploy --guided
```

修改下面的参数，其他参数保留默认值。
"stack name"输入 serverless-video-transcoder
"AWS Region"输入 us-west-2
"VideosBucketName"输入 svt-<random>

![](img/8.png)

几分钟后，部署完成。


### 扩展EBS空间

Cloud9实例初始EBS卷容量较小，为10GB。运行下面的脚本，把EBS卷容量扩展为100GB。

```
quickstart/scripts/resize.sh 100

```


### 下载测试视频



## 测试1：1080P 8分钟视频转码为720p


## 测试2: 1080p 1小时视频转码为720p










