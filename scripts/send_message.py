#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信发送图片消息工具 - 简洁版
支持从配置文件读取配置
"""

import json
import os
import sys
import requests

# 默认配置路径
DEFAULT_CONFIG = "config.json"
DEFAULT_IMAGE = "assets/phone_learning.png"

def load_config():
    """加载配置文件"""
    if not os.path.exists(DEFAULT_CONFIG):
        print(f"❌ 配置文件 {DEFAULT_CONFIG} 不存在!")
        print("请复制 config.example.json 为 config.json 并填入配置")
        return None
    
    with open(DEFAULT_CONFIG, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_access_token(corp_id, secret):
    """获取企业微信access_token"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
    
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if data.get('errcode') == 0:
        return data.get('access_token')
    else:
        print(f"❌ 获取token失败: {data}")
        return None

def upload_media(access_token, file_path):
    """上传临时素材（图片）"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image"
    
    if not os.path.exists(file_path):
        print(f"❌ 图片文件不存在: {file_path}")
        return None
    
    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f.read(), 'image/png')}
        response = requests.post(url, files=files, timeout=60)
    
    data = response.json()
    if data.get('errcode') == 0:
        return data.get('media_id')
    else:
        print(f"❌ 上传失败: {data}")
        return None

def send_message(access_token, agent_id, msg_type, content, to_user="@all"):
    """发送消息"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    
    message = {
        "touser": to_user,
        "msgtype": msg_type,
        "agentid": agent_id
    }
    
    if msg_type == "text":
        message["text"] = {"content": content}
    elif msg_type == "image":
        message["image"] = {"media_id": content}
    
    response = requests.post(url, json=message, timeout=10)
    return response.json()

def main():
    print("=" * 50)
    print("🚀 企业微信消息发送工具")
    print("=" * 50)
    
    # 加载配置
    config = load_config()
    if not config:
        return
    
    corp_id = config.get('corp_id')
    agent_id = config.get('agent_id')
    secret = config.get('secret')
    image_path = config.get('image_path', DEFAULT_IMAGE)
    receiver = config.get('default_receiver', '@all')
    
    # 检查参数
    if not all([corp_id, agent_id, secret]):
        print("❌ 配置参数不完整，请检查 config.json")
        return
    
    print(f"📋 AgentId: {agent_id}")
    print(f"📎 图片: {image_path}")
    print()
    
    # 1. 获取token
    print("[1/3] 获取access_token...")
    access_token = get_access_token(corp_id, secret)
    if not access_token:
        return
    print("✅ 成功")
    
    # 2. 上传图片
    print("\n[2/3] 上传图片...")
    media_id = upload_media(access_token, image_path)
    if not media_id:
        return
    print("✅ 成功")
    
    # 3. 发送消息
    print("\n[3/3] 发送消息...")
    
    # 发送图片
    result = send_message(access_token, agent_id, "image", media_id, receiver)
    if result.get('errcode') == 0:
        print("✅ 图片发送成功!")
    else:
        print(f"❌ 图片发送失败: {result}")
        return
    
    # 发送文字
    import time
    time.sleep(1)
    
    text_content = """📱 数码百科学习资料已送达！

本期内容：手机核心参数详解
• 处理器基础知识
• 屏幕显示技术  
• 影像系统参数
• 续航与充电
• 销售话术总结

请查看上方图片详情，欢迎学习交流！"""
    
    result = send_message(access_token, agent_id, "text", text_content, receiver)
    if result.get('errcode') == 0:
        print("✅ 文字说明发送成功!")
    else:
        print(f"⚠️ 文字说明发送失败: {result}")
    
    print("\n" + "=" * 50)
    print("🎉 发送完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
