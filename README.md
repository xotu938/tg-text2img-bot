# TG Text2Img Bot（一键部署）

这是一个可以直接 **Fork 使用和部署** 的 Telegram 机器人模版项目，用于：

- 从指定 Telegram 频道/群抓取文本与图片，保存到本地 SQLite 数据库与文件夹。  
- 将文字消息渲染为图片并发送到 Telegram。  
- 预留接口接入开源文生图模型（如 Stable Diffusion）把文字生成风格相似的图片。  
- 支持在 GitHub 托管代码，并用 GitHub Actions 定时抓取频道数据（可选）。[web:32][web:39][web:41]

> 本项目仅作技术演示，请务必遵守 Telegram 政策及所在地区法律，尊重版权与隐私。[web:24][web:27]

---

## 一、快速开始（给 Fork 用户）

### 1. Fork 本仓库

1. 打开本仓库页面，点击右上角 **Fork**。  
2. 等待 GitHub 创建你的副本仓库。

### 2. 创建 Telegram Bot 并获取 Bot Token

1. 在 Telegram 中搜索 `@BotFather` 并开始对话。  
2. 发送 `/newbot`，按提示设置机器人名称和用户名（必须以 `bot` 结尾）。  
3. BotFather 返回一串 `123456:ABC-DEF...`，这就是你的 **Bot Token**，请妥善保管。[web:37][web:46]

### 3. 获取 chat id / 频道 id（简易方法）

1. 把你的 Bot 拉进目标群/频道，并给它发一条消息。  
2. 在浏览器打开：  
   `https://api.telegram.org/bot<你的BotToken>/getUpdates`  
3. 在返回的 JSON 里找到 `message.chat.id`，这个就是对应会话的 **chat id**。[web:40][web:46]

---

## 二、项目结构说明

tg-text2img-bot/
├── main.py # 机器人主逻辑：监听消息、文字转图/文生图发回
├── collect_tg_data.py # 抓取频道图文，存 SQLite + 下载图片
├── db.py # 数据库封装
├── model_adapter.py # 文生图模型适配接口（需要你按实际环境对接）
├── config.example.env # 环境变量示例
├── requirements.txt # Python 依赖
├── fonts/
│ └── NotoSansCJK-Regular.otf # 建议准备一个支持中英文的字体
├── data/
│ ├── images/ # 抓取的图片（本地运行后自动生成）
│ └── tg_data.db # SQLite 数据库（本地运行后自动生成）
└── .github/
└── workflows/
└── bot.yml # GitHub Actions 工作流（可选：定时抓取频道数据）

text

---

## 三、本地部署步骤（推荐）

### 1. 克隆你自己的 Fork 仓库

git clone https://github.com/<你的GitHub用户名>/tg-text2img-bot.git
cd tg-text2img-bot

text

### 2. 创建并激活虚拟环境，安装依赖

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

text

### 3. 配置环境变量

复制示例配置：

cp config.example.env .env

text

编辑 `.env`，填入你自己的参数：

API_ID=你的_api_id
API_HASH=你的_api_hash
BOT_TOKEN=你的_bot_token

SOURCE_CHAT_USERNAME=@来源频道或群
TARGET_CHAT_USERNAME=@目标频道或群
TRIGGER_KEYWORD=#pic

text

说明：

- `API_ID` 与 `API_HASH`：在 https://my.telegram.org 创建应用后获得。[web:46]  
- `BOT_TOKEN`：在 `@BotFather` 创建机器人后获得。  
- `SOURCE_CHAT_USERNAME`：你要抓取图文的频道/群（`@xxx` 或数字 id）。  
- `TARGET_CHAT_USERNAME`：机器人发图的目标频道/群（为空则发回当前会话）。  
- `TRIGGER_KEYWORD`：文字转图片的触发关键字，例如 `#pic`。

### 4. 准备字体文件

确保 `fonts/NotoSansCJK-Regular.otf` 存在。  
你可以替换为任意支持中英文的字体文件，并在 `main.py` 中修改 `FONT_PATH`。

---

## 四、功能使用说明

### 1. 抓取频道文字与图片到本地数据库

python collect_tg_data.py

text

脚本会：

- 从 `SOURCE_CHAT_USERNAME` 指定的频道/群抓取最近若干条消息（默认 500 条，可在脚本中改 `limit`）。  
- 文本保存到 `data/tg_data.db` 中的 `messages` 表。  
- 图片下载到 `data/images/`，并在 `images` 表中记录 `file_path`、`caption`、时间等信息。

> 注意：不要把真实 `data/` 目录提交到公开仓库，避免泄露频道数据。

### 2. 启动 Telegram 机器人

python main.py

text

机器人默认行为：

- 在 `SOURCE_CHAT_USERNAME` 指向的会话监听新消息：  
  - 若消息文本中包含 `TRIGGER_KEYWORD`（如 `#pic`），会把该文本渲染为图片并发送到 `TARGET_CHAT_USERNAME`（未配置则发回当前会话）。  
- 支持命令：  

  - `/t2i 文本描述`  
    - 调用 `model_adapter.py` 中配置的文生图模型，根据描述生成图片再发送。  
    - 初始版本中此功能为占位，需你自己在 `model_adapter.py` 中接入 Stable Diffusion 等模型。[web:38][web:50]

---

## 五、接入开源文生图模型（可选，但推荐）

本项目为“文字转图片（排版）”开箱可用，“文字生风格图”提供统一接口，方便你后续接入各种开源模型，例如：

- Stable Diffusion v1.5 / v2.1 / SDXL（本地 GPU 或自建推理服务）。[web:38][web:41]  
- 其他兼容 Diffusers 的开源模型。

步骤建议：

1. 在服务器或本地安装 `torch` + `diffusers` 等依赖。  
2. 在 `model_adapter.py` 的 `Text2ImageModel.generate()` 中：  
   - 加载你选定的模型权重；  
   - 根据传入 `prompt` 生成图片；  
   - 输出 PNG 至 `BytesIO` 返回。  
3. 通过命令 `/t2i 一张蓝色科幻城市夜景` 测试效果。

> 提醒：如果你打算使用从 Telegram 频道抓取的图片来训练 LoRA 或微调模型，请事先确认你拥有足够的版权与授权。

---

## 六、GitHub Actions：定时抓取频道数据（可选）

本仓库包含 GitHub Actions 示例工作流 `.github/workflows/bot.yml`，用于在云端定时执行 `collect_tg_data.py`，例如每 6 小时更新一次本地数据库副本。[web:31]

> 说明：  
> - GitHub Actions 不适合作为长期在线 Telegram Bot 宿主。  
> - 推荐：Bot 长期运行放在你自己的 VPS，本工作流只承担“数据抓取 / CI 检查”职责。[web:31]

### 启用步骤

1. 在你的 Fork 仓库中，打开：`Settings → Secrets and variables → Actions`。  
2. 新建以下 Secrets：  

   - `API_ID`  
   - `API_HASH`  
   - `BOT_TOKEN`  
   - `SOURCE_CHAT_USERNAME`  
   - `TARGET_CHAT_USERNAME`（可选）  
   - `TRIGGER_KEYWORD`（可选）

3. 确认 `bot.yml` 已存在且未被注释掉。  
4. 之后每次 push 到 `main` 或到达定时执行时间，Actions 会自动：  
   - 安装依赖；  
   - 生成 `.env`；  
   - 运行一次 `collect_tg_data.py`。

---

## 七、部署到自己的服务器（VPS / 本机常驻）

以 Debian/Ubuntu 为例：

sudo apt update
sudo apt install -y python3 python3-venv git

git clone https://github.com/<你的GitHub用户名>/tg-text2img-bot.git
cd tg-text2img-bot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp config.example.env .env

编辑 .env，写入你的配置
python main.py

text

建议使用 `tmux`、`screen` 或 `systemd` 让机器人常驻运行。

---

## 八、法律与隐私提示（务必阅读）

- Telegram 频道和用户消息通常受著作权保护。请在抓取、存储、再利用或用于模型训练前，确认你有合法权限（包括但不限于频道所有者或内容作者授权）。[web:24]  
- 不要在公开仓库中提交任何真实用户数据、频道图片或 `tg_data.db` 文件。  
- 模型训练和生成过程可能涉及对原始内容风格的重用，请避免侵犯他人作品权益。  
- 本项目及 README 提供的信息不构成法律意见，具体合规情况因地区与用途而异，如有疑问请咨询专业律师。[web:27]  

**使用本项目即表示你理解并接受：项目作者对因使用本项目产生的任何版权、隐私或合规风险不承担责任，所有风险由使用者自行承担。**
