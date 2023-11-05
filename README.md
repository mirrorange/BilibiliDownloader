# BilibiliDownloader

用于下载B站视频的一个 Python 脚本。调用B站官方API获取视频链接，通过 Aria2 进行下载，再调用 FFmpeg 进行视频的合并。

A script for downloading Bilibili videos. It calls the official API of Bilibili to get the video link, downloads it through Aria2, and then calls FFmpeg to merge the video.

## 使用方法 Usage

### 1. 安装 Python Install Python

[Python](https://www.python.org/downloads/)

### 2. 安装并运行 Aria2 Install and run Aria2

[Aria2](https://aria2.github.io/)

启动 Aria2 时，需要开启 RPC，具体方法请参考 Aria2 的官方文档。

When starting Aria2, you need to turn on RPC. For details, please refer to the official documentation of Aria2.

### 3. 安装 FFmpeg Install FFmpeg

[FFmpeg](https://ffmpeg.org/download.html)

安装 FFmpeg 时，需要将 FFmpeg 添加到环境变量中或者将 FFmpeg.exe 放到项目目录下。

When installing FFmpeg, you need to add FFmpeg to the environment variable or put FFmpeg.exe in the project directory.

### 4. 运行下载脚本 Run the download script

```bash
python download.py
```

按照提示输入视频 ID（BVID，AID，MDID，SSID，EPID），即可开始下载。

Enter the video ID (BVID, AID, MDID, SSID, EPID) as prompted to start downloading.

## 声明 Statement

本项目仅供学习交流使用，请勿用于商业用途。若因使用本项目导致任何损失，本人概不负责。

This project is for learning and communication only, please do not use it for commercial purposes. I am not responsible for any loss caused by the use of this project.