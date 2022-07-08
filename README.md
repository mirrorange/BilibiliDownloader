# BilibiliDownloader
用于下载B站视频的一个 Python 脚本。调用B站官方API获取视频链接，通过 Aria2 进行下载，再调用 FFmpeg 进行视频的合并。
## 使用方法
- 运行 Settings.py 进行设置。
- 开启 Aria2 服务器。
- 运行 DownloadVideo.py 下载视频。