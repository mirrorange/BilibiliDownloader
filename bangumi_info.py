# 由 MDID,SSID,EPID 获取视频信息
import requests
import settings


def get_media_info(mdid, sessdata=""):
    """由 MDID 获取视频信息"""
    if not mdid:
        print("GetMediaInfo: 必须提供mdid")
        return
    cookies = {"SESSDATA": sessdata} if sessdata else {}
    params = {"media_id": mdid}
    try:
        r = requests.get("https://api.bilibili.com/pgc/review/user",
                         params=params, cookies=cookies)
        r.raise_for_status()
        jsonobj = r.json()
    except requests.exceptions.HTTPError as err:
        print(f"GetMediaInfo: 请求: {r.url} 错误: {err}")
        return {"code": 1, "results": []}
    if jsonobj["code"] == 0:
        title = jsonobj["result"]["media"]["title"]
        ssid = jsonobj["result"]["media"]["season_id"]
        print(f"GetMediaInfo: 取得剧集: {title} SSID: {ssid}")
        return get_bangumi_info(ssid=ssid, sessdata=sessdata)
    else:
        print(f"GetMediaInfo: 请求: {r.url} 错误: {jsonobj['message']}")
        return {"code": jsonobj["code"], "results": []}

def get_bangumi_info(ssid="", epid="", sessdata=""):
    """由 SSID,EPID 获取视频信息"""
    if not ssid and not epid:
        print("GetBangumiInfo: 必须提供ssid与epid其中之一")
        return
    cookies = {"SESSDATA": sessdata} if sessdata else {}
    params = {"season_id": ssid} if ssid else {"ep_id": epid}
    try:
        r = requests.get("https://api.bilibili.com/pgc/view/web/season",
                     params=params, cookies=cookies)
        r.raise_for_status()
        jsonobj = r.json()
    except requests.exceptions.HTTPError as err:
        print(f"GetBangumiInfo: 请求: {r.url} 错误: {err}")
        return {"code": 1, "results": []}
    results = []
    if jsonobj["code"] == 0:
        for data in jsonobj["result"]["episodes"]:
            title = data["title"]
            long_title = data["long_title"]
            aid = data["aid"]
            bvid = data["bvid"]
            cid = data["cid"]
            print(
                f"GetBangumiInfo: 取得视频: {title}，标题为: {long_title}，AID: {aid}，BVID: {bvid}，CID: {cid}")
            result = {"title": jsonobj["result"]["title"],
                      "subtitle": f"{title}.{long_title}", "aid": aid, "bvid": bvid, "cid": cid}
            results.append(result)
        return {"code": jsonobj["code"], "results": results}
    else:
        print(f"GetBangumiInfo: 请求: {r.url} 错误: {jsonobj['message']}")
        return {"code": jsonobj["code"], "results": []}


if __name__ == '__main__':
    sessdata = settings.sessdata or input("请输入SESSDATA: ")
    id = input("请输入SSID或EPID或MDID: ")
    if id.startswith("ss") or id.startswith("SS"):
        ssid = id[2:]
        get_bangumi_info(ssid=ssid, sessdata=sessdata)
    elif id.startswith("ep") or id.startswith("EP"):
        epid = id[2:]
        get_bangumi_info(epid=epid, sessdata=sessdata)
    elif id.startswith("md") or id.startswith("MD"):
        mdid = id[2:]
        get_media_info(mdid=mdid, sessdata=sessdata)
    else:
        print("无法识别你的输入！")
