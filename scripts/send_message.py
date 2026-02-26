#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信发送图片消息工具
支持两种配置方式：
1. 环境变量 (GitHub Actions) - 优先级高
2. 配置文件 (本地运行) - 优先级低
"""

import json
import os
import sys
import time
import requests

# 默认配置路径
DEFAULT_CONFIG = "config.json"
DEFAULT_IMAGE = "assets/phone_learning.png"

def load_config():
    """加载配置 - 支持环境变量和配置文件"""
    
    # 优先使用环境变量 (GitHub Actions)
    corp_id = os.environ.get('CORP_ID')
    agent_id = os.environ.get('AGENT_ID')
    secret = os.environ.get('SECRET')
    image_path = os.environ.get('IMAGE_PATH', DEFAULT_IMAGE)
    
    # 如果环境变量存在，直接使用
    if corp_id and agent_id and secret:
        print("使用环境变量配置")
        return {
            'corp_id': corp_id,
            'agent_id': agent_id,
            'secret': secret,
            'image_path': image_path,
            'default_receiver': os.environ.get('DEFAULT_RECEIVER', '@all')
        }
    
    # 否则尝试读取配置文件
    print("环境变量未设置，尝试读取配置文件...")
    if not os.path.exists(DEFAULT_CONFIG):
        print(f"❌ 配置文件 {DEFAULT_CONFIG} 不存在!")
        print("请设置环境变量或复制 config.example.json 为 config.json")
        return None
    
    with open(DEFAULT_CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 合并环境变量覆盖配置文件
    if os.environ.get('CORP_ID'):
        config['corp_id'] = os.environ.get('CORP_ID')
    if os.environ.get('AGENT_ID'):
        config['agent_id'] = os.environ.get('AGENT_ID')
    if os.environ.get('SECRET'):
        config['secret'] = os.environ.get('SECRET')
    if os.environ.get('IMAGE_PATH'):
        config['image_path'] = os.environ.get('IMAGE_PATH')
    
    return config

def get_access_token(corp_id, secret):
    """获取企业微信access_token"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('errcode') == 0:
            return data.get('access_token')
        else:
            print(f"❌ 获取token失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def upload_media(access_token, file_path):
    """上传临时素材（图片）"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image"
    
    if not os.path.exists(file_path):
        print(f"❌ 图片文件不存在: {file_path}")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            files = {'media': (os.path.basename(file_path), f.read(), 'image/png')}
            response = requests.post(url, files=files, timeout=60)
        
        data = response.json()
        if data.get('errcode') == 0:
            print(f"✅ 图片上传成功!")
            return data.get('media_id')
        else:
            print(f"❌ 上传失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 上传异常: {e}")
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
    
    try:
        response = requests.post(url, json=message, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        return {"errcode": -1, "errmsg": str(e)}

def main():
    print("=" * 60)
    print("🚀 企业微信消息发送工具")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    if not config:
        sys.exit(1)
    
    corp_id = config.get('corp_id')
    agent_id = config.get('agent_id')
    secret = config.get('secret')
    image_path = config.get('image_path', DEFAULT_IMAGE)
    receiver = config.get('default_receiver', '@all')
    
    # 检查参数
    if not all([corp_id, agent_id, secret]):
        print("❌ 配置参数不完整")
        sys.exit(1)
    
    print(f"📋 AgentId: {agent_id}")
    print(f"📎 图片: {image_path}")
    print()
    
    # 1. 获取token
    print("[1/3] 获取access_token...")
    access_token = get_access_token(corp_id, secret)
    if not access_token:
        sys.exit(1)
    print("✅ 成功")
    
    # 2. 上传图片
    print("\n[2/3] 上传图片...")
    media_id = upload_media(access_token, image_path)
    if not media_id:
        sys.exit(1)
    
    # 3. 发送消息
    print("\n[3/3] 发送消息...")
    
    # 发送图片
    result = send_message(access_token, agent_id, "image", media_id, receiver)
    if result.get('errcode') == 0:
        print("✅ 图片发送成功!")
    else:
        print(f"❌ 图片发送失败: {result}")
        sys.exit(1)
    
    # 等待一下再发送文字
    time.sleep(1)
    
    # 文字内容
    text_content = """📱 数码百科学习资料已送达！

📖 本期内容：手机核心参数详解

• 处理器基础知识 (CPU/NPU/GPU)
• 屏幕显示技术 (刷新率/LTPO)
• 影像系统参数 (传感器/光圈)
• 续航与充电 (快充功率)
• 销售话术总结

请查看上方图片详情，欢迎学习交流！

📌 每天学习一点，轻松掌握手机数码知识！"""

    result = send_message(access_token, agent_id, "text", text_content, receiver)
    if result.get('errcode') == 0:
        print("✅ 文字说明发送成功!")
    else:
        print(f"⚠️ 文字说明发送失败: {result}")
    
    print("\n" + "=" * 60)
    print("🎉 发送完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
