# 由 AID，BVID，CID 获取某一视频的下载地址
import requests
import Settings

def get_quality(cid, aid="", bvid="", sessdata=""):
    # 检查是否提供了AVID或BVID
    if not aid and not bvid:
        print("GetQuality: 必须提供aid与bvid其中之一")
        return
    # 准备GET请求的信息
    cookies = {}
    params = {}
    if sessdata.strip():
        cookies = {"SESSDATA": sessdata}
    if aid:
        params = {"avid": aid, "cid": cid, "fnval": 16}
    else:
        params = {"bvid": bvid, "cid": cid, "fnval": 16}
    # 发出和解析请求
    try:
        r = requests.get("https://api.bilibili.com/x/player/playurl", params=params, cookies=cookies)
        r.raise_for_status()
        jsonobj = r.json()
    except requests.exceptions.HTTPError as err:
        print("GetQuality: 请求: ", r.url, " 错误: ", err)
        return {"code": 1}
    if jsonobj["code"] == 0:
        quality_num = jsonobj["data"]["accept_quality"][0]
        print("GetQuality: 取得最高清晰度: ", quality_num)
        return {"code": jsonobj["code"], "quality_num": quality_num}
    else:
        print("GetQuality: 请求: ", r.url, " 错误: ", jsonobj["message"])
        return {"code": jsonobj["code"]}

def get_download_url(cid, quality=-1, aid="", bvid="", sessdata=""):
    # 检查是否提供了AVID或BVID
    if not aid and not bvid:
        print("GetDownloadUrl: 必须提供aid与bvid其中之一")
        return
    # 自动取得最高清晰度
    if quality == -1:
        quality_info = get_quality(cid=cid, aid=aid, bvid=bvid, sessdata=sessdata)
        if quality_info["code"] == 0:
            quality = quality_info["quality_num"]
        else:
            return {"code": quality_info["code"]}
    # 准备GET请求的信息
    cookies = {}
    params = {}
    if sessdata.strip():
        cookies = {"SESSDATA": sessdata}
    if aid:
        params = {"avid": aid, "cid": cid, "fnval": 16, "qn": quality}
    else:
        params = {"bvid": bvid, "cid": cid, "fnval": 16, "qn": quality}
    # 发出和解析请求
    try:
        r = requests.get("https://api.bilibili.com/x/player/playurl", params=params, cookies=cookies)
        r.raise_for_status()
        jsonobj = r.json()
    except requests.exceptions.HTTPError as err:
        print("GetDownloadUrl: 请求: ", r.url, " 错误: ", err)
        return {"code": 1}
    if jsonobj["code"] == 0:
        video_url = [jsonobj["data"]["dash"]["video"][0]["baseUrl"]]
        audio_url = [jsonobj["data"]["dash"]["audio"][0]["baseUrl"]]
        if Settings.backupurl:
            video_url += jsonobj["data"]["dash"]["video"][0]["backupUrl"]
            audio_url += jsonobj["data"]["dash"]["audio"][0]["backupUrl"]
        quality_num = jsonobj["data"]["dash"]["video"][0]["id"]
        print("GetDownloadUrl: 取得视频清晰度代码: ", quality_num)
        print("GetDownloadUrl: 取得视频下载地址: ", video_url)
        print("GetDownloadUrl: 取得音频下载地址: ", audio_url)
        return {"code": jsonobj["code"], "quality_num": quality_num, "video_url": video_url, "audio_url": audio_url, "jsonobj": jsonobj}
    else:
        print("GetDownloadUrl: 请求: ", r.url, " 错误: ", jsonobj["message"])
        return {"code": jsonobj["code"]}

if __name__ == '__main__':
    sessdata = input("请输入SESSDATA: ")
    id = input("请输入BVID或AID: ")
    aid = ""
    bvid = ""
    if id.startswith("av") or id.startswith("AV"):
        aid = id[2:]
    elif id.startswith("bv") or id.startswith("BV"):
        bvid = id
    else:
        print("无法识别你的输入！")
        exit()
    cid = input("请输入CID: ")
    qstr = input("请输入清晰度代码: ")
    if not qstr.strip():
        quality = -1
    else:
        quality = int(qstr)
    get_download_url(cid=cid, aid=aid, bvid=bvid, sessdata=sessdata, quality=quality)