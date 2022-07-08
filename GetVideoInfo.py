# 由 AID,BVID 获取视频信息
import requests
import Settings


def get_page_list(aid="", bvid="", sessdata=""):
    # 检查是否提供了AVID或BVID
    if not aid and not bvid:
        print("GetVideoInfo: 必须提供aid与bvid其中之一")
        return
    # 准备GET请求的信息
    cookies = {}
    params = {}
    if sessdata.strip():
        cookies = {"SESSDATA": sessdata}
    if aid:
        params = {"avid": aid}
    else:
        params = {"bvid": bvid}
    # 发出和解析请求
    try:
        r1 = requests.get("https://api.bilibili.com/x/web-interface/view", params=params, cookies=cookies)
        r1.raise_for_status()
        jsonobj1 = r1.json()
        r2 = requests.get("https://api.bilibili.com/x/player/pagelist", params=params, cookies=cookies)
        r2.raise_for_status()
        jsonobj2 = r2.json()
    except requests.exceptions.RequestException as e:
        print("GetVideoInfo: 请求错误:", e)
        return {"code": 1}
    # 处理请求结果
    if jsonobj2["code"] == 0 and jsonobj1["code"] == 0:
        results = []
        for data in jsonobj2["data"]:
            print(f"GetVideoInfo: 取得分P:{data['page']}，标题为:{data['part']}，CID:{data['cid']}")
            result = {"title": jsonobj1["data"]["title"], "subtitle": f"{data['page']}.{data['part']}",
                      "aid": aid, "bvid": bvid, "cid": data["cid"]}
            results.append(result)
        return {"code": 0, "results": results}
    else:
        if jsonobj1["code"] != 0:
            print(f"GetVideoInfo: 请求: {r1.url} 错误: {jsonobj1['message']}")
        if jsonobj2["code"] != 0:
            print(f"GetVideoInfo: 请求: {r2.url} 错误: {jsonobj2['message']}")
        return {"code": 1}


if __name__ == '__main__':
    if Settings.sessdata:
        sessdata = Settings.sessdata
    else:
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
    get_page_list(aid=aid, bvid=bvid, sessdata=sessdata)