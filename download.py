from xmlrpc.client import ServerProxy
import time
import video_info
import bangumi_info
import download_info
import settings
import process
import os
from os import path


def prepare_file_name(filename):
    """删除文件名里不该有的东西"""
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename


def aria2_download_status(gid):
    """获取下载状态"""
    if gid == 0:
        return "complete"
    s = ServerProxy(settings.rpcserver)
    return s.aria2.tellStatus(gid, ["status"])["status"]


def aria2_wait(gid):
    """等待下载完成"""
    s = ServerProxy(settings.rpcserver)
    while True:
        time.sleep(1)
        status = s.aria2.tellStatus(gid, ["status", "downloadSpeed", "completedLength", "totalLength", "files"])
        if status["status"] in ["active", "waiting", "paused"]:
            print(f"DownloadVideo: 下载状态: {status['status']}，速度: {status['downloadSpeed']} byte/s，{status['completedLength']}/{status['totalLength']}")
        elif status["status"] == "complete":
            print(f"DownloadVideo: 下载完成: {status['files'][0]['path']}")
            return True
        elif status["status"] in ["error", "removed"]:
            print("DownloadVideo: 下载失败。")
            return False


def check_file(filepath):
    """检查文件，返回True为需要下载，False为跳过下载"""
    if path.exists(filepath + ".mkv"):
        return False
    else:
        return True


def aria2_check_file(filepath):
    """检查文件，返回True为需要下载，False为跳过下载"""
    if path.exists(filepath):
        if path.exists(filepath + ".aria2"):
            os.remove(filepath)
            os.remove(filepath + ".aria2")
            return True
        else:
            return False
    else:
        return True


def aria2_download(url, sync=True, out="", dir=settings.dir):
    """通过Aria2下载文件"""
    s = ServerProxy(settings.rpcserver)
    ua = settings.ua
    ref = "https://www.bilibili.com/"
    if out.strip() != "":
        if not aria2_check_file(path.join(dir, out)):
            print("DownloadVideo: 文件已存在，跳过下载")
            return 0
        options = {"dir": dir, "out": out, "referer": ref, "user-agent": ua, "allow-overwrite": True}
    else:
        options = {"dir": dir, "referer": ref, "user-agent": ua, "allow-overwrite": True}
    gid = s.aria2.addUri(url, options)
    if sync:
        if not aria2_wait(gid):
            time.sleep(2)
            gid = aria2_download(url, sync, out, dir)
    return gid


def download_by_list(video_list, sessdata, quality=-1):
    """通过AVID或BVID，CID列表下载"""
    gid_list = []
    fail_list = []
    code = 1  # 代码 0: 全部成功；1: 全部失败；2: 部分失败
    for video in video_list:
        if len(video_list) == 1:
            file_name = prepare_file_name(video["title"])
            folder_name = settings.dir
        else:
            file_name = prepare_file_name(video["subtitle"])
            folder_name = path.join(settings.dir, prepare_file_name(video["title"]))
        if not check_file(path.join(folder_name, file_name)):
            print("DownloadVideo: 下载已完成，跳过下载")
            continue
        url_obj = download_info.get_download_url(cid=video["cid"], aid=video["aid"], bvid=video["bvid"], quality=quality, sessdata=sessdata)
        if url_obj["code"] == 0:
            video_gid = aria2_download(url=url_obj["videoUrl"], out=file_name + "_video.m4s", dir=folder_name)
            audio_gid = aria2_download(url=url_obj["audioUrl"], out=file_name + "_audio.m4s", dir=folder_name)
            if settings.syncdownload and settings.automerge:
                if aria2_download_status(video_gid) == "complete" and aria2_download_status(audio_gid) == "complete":
                    process.auto_merge(path.join(folder_name, file_name) + "_video.m4s")
            gid_list.append({"code": url_obj["code"], "videoGid": video_gid, "audioGid": audio_gid})
            if code == 1:
                code = 0
        else:
            fail_list.append({"code": url_obj["code"], "item": video})
            if code == 0:
                code = 2
    print(f"DownloadVideo: 下载处理完成，成功: {len(gid_list)}，失败: {len(fail_list)}")
    return {"code": code, "gidList": gid_list, "failList": fail_list}


def download_range(download_list):
    rstr = input("DownloadVideo:请输入下载范围（留空下载全部）: ")
    if len(rstr.split("-")) == 2:
        results = download_list[int(rstr.split("-")[0]) - 1:int(rstr.split("-")[1])]
    else:
        try:
            i = int(rstr)
            results = download_list[i - 1]
        except:
            results = download_list
    return results


def download_by_aid(aid, sessdata, quality=-1):
    """通过AVID下载"""
    data = video_info.get_page_list(aid=aid, sessdata=sessdata)
    download_list = download_range(data["results"])
    return download_by_list(video_list=download_list, quality=quality, sessdata=sessdata)


def download_by_bvid(bvid, sessdata, quality=-1):
    """通过BVID下载"""
    data = video_info.get_page_list(bvid=bvid, sessdata=sessdata)
    download_list = download_range(data["results"])
    return download_by_list(video_list=download_list, quality=quality, sessdata=sessdata)


def download_by_mdid(mdid, sessdata, quality=-1):
    """通过MDID下载"""
    data = bangumi_info.get_media_info(mdid=mdid, sessdata=sessdata)
    download_list = download_range(data["results"])
    return download_by_list(video_list=download_list, quality=quality, sessdata=sessdata)


def download_by_ssid(ssid, sessdata, quality=-1):
    """通过SSID下载"""
    data = bangumi_info.get_bangumi_info(ssid=ssid, sessdata=sessdata)
    download_list = download_range(data["results"])
    return download_by_list(video_list=download_list, quality=quality, sessdata=sessdata)


def download_by_epid(epid, sessdata, quality=-1):
    """通过EPID下载"""
    data = bangumi_info.get_bangumi_info(epid=epid, sessdata=sessdata)
    download_list = download_range(data["results"])
    return download_by_list(video_list=download_list, quality=quality, sessdata=sessdata)


if __name__ == '__main__':
    if settings.sessdata != "":
        sessdata = settings.sessdata
    else:
        sessdata = input("请输入SESSDATA: ")
    if settings.quality != 0:
        quality = settings.quality
    else:
        qstr = input("请输入清晰度代码（不填将自动选择最高画质）: ")
        if qstr.strip() == "":
            quality = -1
        else:
            quality = int(qstr)
    id = input("请输入各种ID（支持BVID，AID，MDID，SSID，EPID）: ")
    if id.startswith("av") or id.startswith("AV"):
        aid = id[2:]
        download_by_aid(aid=aid, quality=quality, sessdata=sessdata)
    elif id.startswith("bv") or id.startswith("BV"):
        bvid = id
        download_by_bvid(bvid=bvid, quality=quality, sessdata=sessdata)
    elif id.startswith("md") or id.startswith("MD"):
        mdid = id[2:]
        download_by_mdid(mdid=mdid, quality=quality, sessdata=sessdata)
    elif id.startswith("ss") or id.startswith("SS"):
        ssid = id[2:]
        download_by_ssid(ssid=ssid, quality=quality, sessdata=sessdata)
    elif id.startswith("ep") or id.startswith("EP"):
        epid = id[2:]
        download_by_epid(epid=epid, quality=quality, sessdata=sessdata)
    else:
        print("无法识别你的输入！")