#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 定时任务安装脚本
用于在 Windows 计划任务中设置每日自动发送
"""

import os
import sys
import subprocess

# 配置
TASK_NAME = "WeChatDailySender"
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "send_message.py")
PYTHON_PATH = sys.executable
TRIGGER_TIME = "09:10"  # 每天运行时间

def create_task():
    """创建 Windows 计划任务"""
    
    # 检查脚本是否存在
    if not os.path.exists(SCRIPT_PATH):
        print(f"❌ 脚本不存在: {SCRIPT_PATH}")
        return False
    
    # 删除已存在的任务（如果存在）
    try:
        subprocess.run(
            ['schtasks', '/Delete', '/TN', TASK_NAME, '/F'],
            capture_output=True
        )
        print("已删除旧任务")
    except:
        pass
    
    # 创建新任务
    # 每天 9:10 运行
    cmd = [
        'schtasks', '/Create',
        '/TN', TASK_NAME,
        '/TR', f'"{PYTHON_PATH}" "{SCRIPT_PATH}"',
        '/SC', 'DAILY',
        '/ST', TRIGGER_TIME,
        '/F'  # 如果存在则强制覆盖
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 定时任务创建成功!")
            print(f"   任务名称: {TASK_NAME}")
            print(f"   运行时间: 每天 {TRIGGER_TIME}")
            print(f"   脚本路径: {SCRIPT_PATH}")
            return True
        else:
            print(f"❌ 创建失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 创建异常: {e}")
def delete_task():
    """删除计划        return False

任务"""
    try:
        result = subprocess.run(
            ['schtasks', '/Delete', '/TN', TASK_NAME, '/F'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 任务已删除")
            return True
        else:
            print(f"❌ 删除失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 删除异常: {e}")
        return False

def show_status():
    """查看任务状态"""
    try:
        result = subprocess.run(
            ['schtasks', '/Query', '/TN', TASK_NAME],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 任务状态:")
            print(result.stdout)
            return True
        else:
            print("❌ 任务不存在或查询失败")
            return False
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        return False

def main():
    print("=" * 60)
    print("Windows 定时任务管理工具")
    print("=" * 60)
    print()
    print("用法:")
    print("  python setup_task.py create   - 创建定时任务")
    print("  python setup_task.py delete   - 删除定时任务")
    print("  python setup_task.py status  - 查看任务状态")
    print("  python setup_task.py run      - 立即运行一次")
    print()
    
    if len(sys.argv) < 2:
        show_status()
        return
    
    action = sys.argv[1].lower()
    
    if action == "create":
        create_task()
    elif action == "delete":
        delete_task()
    elif action == "status":
        show_status()
    elif action == "run":
        print("正在运行脚本...")
        os.system(f'"{PYTHON_PATH}" "{SCRIPT_PATH}"')
    else:
        print(f"未知命令: {action}")

if __name__ == "__main__":
    main()
