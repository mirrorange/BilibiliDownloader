import json
import os


def get_input(prompt, default=None, type=str):
    """
    提示用户输入并返回值。
    如果指定了默认值，则在用户输入为空时返回默认值。
    如果指定了类型，则将用户输入转换为指定类型。
    """
    while True:
        user_input = input(prompt)
        if not user_input:
            if default is not None:
                return default
            else:
                print("输入不能为空，请重新输入！")
        else:
            try:
                return type(user_input)
            except ValueError:
                print("输入格式不正确，请重新输入！")


if __name__ == "__main__":
    dir = get_input("下载保存目录: ", default="D:\\Download")
    sessdata = get_input("SESSDATA:")
    rpcserver = get_input("Aria2 RPC-Server:", default="http://localhost:6800/rpc")
    syncdownload = get_input("是否同步下载（如不同步下载，自动合并功能将失效）: ", default=True, type=bool)
    automerge = get_input("是否自动合并视频: ", default=True, type=bool)
    autodelete = get_input("合并后是否删除原文件: ", default=True, type=bool)
    ua = get_input(
        "Aria2浏览器UA: ",
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    )
    quality = get_input("默认下载清晰度代码（自动选择最高请填-1）: ", default=-1)
    backupurl = get_input("是否使用备用地址（如果输出异常请禁用）: ", default=False, type=bool)

    settings = {
        "dir": dir,
        "sessdata": sessdata,
        "rpcserver": rpcserver,
        "syncdownload": syncdownload,
        "automerge": automerge,
        "autodelete": autodelete,
        "ua": ua,
        "quality": quality,
        "backupurl": backupurl,
    }

    with open("settings.json", "w") as f:
        json.dump(settings, f)
else:
    default_settings = {
        "dir": "D:\\Download",
        "sessdata": "",
        "rpcserver": "http://localhost:6800/rpc",
        "syncdownload": True,
        "automerge": True,
        "autodelete": True,
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "quality": -1,
        "backupurl": False,
    }

    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            settings = json.load(f)
        for key in default_settings.keys():
            if key not in settings:
                settings[key] = default_settings[key]
    else:
        settings = default_settings
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    dir = settings["dir"]
    sessdata = settings["sessdata"]
    rpcserver = settings["rpcserver"]
    syncdownload = settings["syncdownload"]
    automerge = settings["automerge"]
    autodelete = settings["autodelete"]
    ua = settings["ua"]
    quality = settings["quality"]
    backupurl = settings["backupurl"]
