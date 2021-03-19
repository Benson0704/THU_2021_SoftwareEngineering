import os
import requests
from django.shortcuts import redirect

from oauthlib import oauth2

OAUTH = {
    "app_id": "ks692991395583662522",
    "app_secret": "SQQoA2MFqcdeRF_vbFttIw",  # 需要存储在服务器端，不能暴露
    "scope": "user_video_info",
    "response_type": "code",
    "auth_url": "https://open.kuaishou.com/oauth2/authorize",
    "token_url": "https://open.kuaishou.com/oauth2/access_token",
    "redirect_uri": "http://127.0.0.1:8000/logIn/oauth/callback"
}
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
session = {}


def oauth(response):
    """用户点击链接时，把用户定向到OAuth2的登陆界面"""
    client = oauth2.WebApplicationClient(OAUTH["app_id"])
    state = client.state_generator()
    auth_url = client.prepare_request_uri(OAUTH["auth_url"],
                                          OAUTH["redirect_uri"],
                                          OAUTH["scope"],
                                          state)
    session["oauth_state"] = state
    return redirect(auth_url)


def oauth_callback(response):
    """用户同意授权后，会被重定向回到这个URL"""
    print("Successfully authorize")
    code = response.GET.get("code")
    print(code)
    body = {"app_id": OAUTH["app_id"],
            "app_secret": OAUTH["app_secret"],
            "code": code,
            "grant_type": "authorization_code"
            }
    r = requests.post(OAUTH["token_url"], body)
    access_token = r.json().get("access_token")

    # 通过list接口得到用户的全部video_list信息
    url = "https://open.kuaishou.com/openapi/tsinghua/photo/list"
    params = {"access_token": access_token, "app_id": OAUTH["app_id"]}
    r = requests.get(url=url, params=params)
    data = r.json()
    session["video_list"] = data.get("video_list")

    # 通过info接口得到单个video信息
    photo_url = "https://open.kuaishou.com/openapi/tsinghua/photo/info"
    for video in session["video_list"]:
        params = {"access_token": access_token, "app_id": OAUTH["app_id"], "photo_id": video["photo_id"]}
        r = requests.get(photo_url, params=params)
        photo_data = r.json()

    # 通过count接口得到用户的视频数量统计信息
    count_url = "https://open.kuaishou.com/openapi/photo/count"
    r = requests.get(url=count_url, params=params)
    count_data = r.json()
    session["all_count"] = count_data["all_count"]
    session["private_count"] = count_data["private_count"]
    session["public_count"] = count_data["public_count"]
    session["friend_count"] = count_data["friend_count"]
    print(session)
    return redirect("/")  # 得到首页的接口后需要修改
