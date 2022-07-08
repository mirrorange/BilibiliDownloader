# 对下载的内容进行合并处理
import os
from os import path
import Settings


def merge_video(video, audio, output):
    """将视频和音频合并成一个文件"""
    # 使用ffmpeg命令将视频和音频合并成一个文件
    command = f'ffmpeg -i "{video}" -i "{audio}" -map 0:v -map 1:a -c copy "{output}"'
    if os.system(command) == 0:
        # 如果合并成功，打印提示信息并返回True
        print("Process: 文件合并完成: ", output)
        return True
    else:
        # 如果合并失败，打印提示信息并返回False
        print("Process: 文件合并失败: ", command)
        return False


def auto_merge(filepath, delete=Settings.autodelete):
    """自动合并视频和音频文件"""
    # 判断是否为视频文件
    if filepath.endswith("_video.m4s"):
        # 判断对应的音频文件是否存在
        if path.exists(filepath[0:-10] + "_audio.m4s"):
            # 调用merge_video函数将视频和音频合并成一个mkv文件
            flag = merge_video(
                filepath, filepath[0:-10] + "_audio.m4s", filepath[0:-10] + ".mkv"
            )
            # 如果需要删除原始文件，并且合并成功，则删除视频和音频文件
            if delete and flag:
                os.remove(filepath)
                os.remove(filepath[0:-10] + "_audio.m4s")


def auto_merge_all(directory):
    """自动合并指定文件夹下的所有视频和音频文件"""
    for i in os.listdir(directory):
        filepath = path.join(directory, i)
        if path.isfile(filepath):
            auto_merge(filepath)


if __name__ == "__main__":
    # 获取用户输入的文件夹路径，并自动合并其中的所有视频和音频文件
    directory = input("请输入文件所在文件夹: ")
    auto_merge_all(directory)
