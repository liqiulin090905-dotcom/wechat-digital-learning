# 企业微信数码知识每日推送工具

> 自动化的手机数码知识学习文件生成与企业微信推送工具

## 项目简介

这是一个用于生成手机数码相关学习内容并自动推送到企业微信的工具。支持生成精美的学习长图，包含处理器、屏幕、影像、续航等核心知识的详细讲解。

## 功能特性

- 📱 **学习内容生成**：自动生成专业的手机数码知识长图
- 📤 **企业微信推送**：一键推送到企业微信应用
- 📖 **每日更新**：持续输出数码知识学习内容
- 🎯 **销售话术**：附带实用的销售推荐话术

## 项目结构

```
wechat-digital-learning/
├── src/
│   └── phone_learning.html    # 学习文件HTML模板
├── assets/
│   └── phone_learning.png    # 生成的学习图片
├── scripts/
│   ├── send_final.py         # 最终发送脚本
│   ├── check_wechat_permissions.py  # 权限检查工具
│   └── send_to_wechat.py     # 基础发送脚本
├── requirements.txt          # Python依赖
├── README.md                 # 项目说明
└── config.example.json       # 配置文件示例
```

## 快速开始

### 环境要求

- Python 3.8+
- 企业微信账号（需要管理员权限）

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yourusername/wechat-digital-learning.git
cd wechat-digital-learning
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置企业微信

复制 `config.example.json` 为 `config.json` 并填入您的配置：

```json
{
    "corp_id": "your_corp_id",
    "agent_id": "your_agent_id",
    "secret": "your_secret"
}
```

### 使用方法

#### 1. 生成学习图片

修改 `src/phone_learning.html` 中的内容，然后使用浏览器截图或工具生成PNG图片。

#### 2. 推送到企业微信

```bash
python scripts/send_final.py
```

或指定图片路径：

```bash
python scripts/send_final.py --image path/to/image.png
```

## 学习内容模板

学习文件包含以下模块：

### 1. 处理器 (SoC) 基础知识
- CPU 性能核心
- NPU AI 引擎
- GPU 图形处理
- 基带芯片

### 2. 屏幕显示技术
- 刷新率 (60Hz/120Hz/144Hz)
- 分辨率 (1080P/2K/4K)
- LTPO 智能调频
- 护眼调光

### 3. 影像系统
- 传感器尺寸
- 像素数量
- 光圈大小
- 光学防抖

### 4. 续航与充电
- 电池容量
- 有线/无线快充
- 反向充电

### 5. 销售话术
- 产品推荐话术
- 核心卖点总结

## 配置说明

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| corp_id | 企业ID | 企业微信后台获取 |
| agent_id | 应用ID | 应用管理页面 |
| secret | 应用Secret | 应用管理页面 |

## 常见问题

### Q: 发送失败，提示 "not allow operate another agent"
A: 请检查 AgentId 是否正确，确保使用应用专属的 Secret。

### Q: 图片上传失败
A: 检查网络连接，确保企业微信API可访问。

### Q: 如何修改学习内容？
A: 直接编辑 `src/phone_learning.html` 文件，使用浏览器打开后截图生成新图片。

## 技术栈

- **Python 3.8+** - 后端脚本
- **HTML/CSS** - 学习内容模板
- **企业微信API** - 消息推送

## 许可证

MIT License

## 作者

Matrix Agent

## 更新日志

### v1.0.0 (2026-02-26)
- 初始版本
- 支持学习图片生成
- 支持企业微信推送
- 包含权限检查工具
