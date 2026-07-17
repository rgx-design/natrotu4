# 🔥 火影背单词 - 完整游戏项目

## 📁 项目概述

**火影背单词** 是一个基于火影忍者主题的背单词游戏，集成了完整的用户管理系统和积分系统。

## 🎮 游戏特色

- **火影忍者主题**：使用火影角色作为头像和主题背景
- **多种词库**：动词词库、小学词汇、四级词汇
- **积分系统**：答对得积分，连续答对有额外奖励
- **排行榜**：实时显示总积分榜和今日积分榜
- **用户系统**：注册、登录、个人进度追踪

## 🚀 快速启动

### 方式1：使用启动脚本

```bash
cd "F:\2fen\.qclaw\workspace-ua58rsb93veqtxl7\{workspace_root_dir}\natrotu4"
node start.js
```

### 方式2：手动启动

```bash
# 1. 确保 MongoDB 正在运行
mongod

# 2. 启动服务器
cd "F:\2fen\.qclaw\workspace-ua58rsb93veqtxl7\{workspace_root_dir}\natrotu4"
node points-system.js

# 3. 打开浏览器访问
# 首页：http://localhost:3000 (或直接打开 index.html)
# 游戏页：http://localhost:3000/app/natrotu6.html
```

## 📂 项目结构

```
natrotu4/
│
├── 📄 入口文件
│   ├── index.html              # 首页（登录注册、排行榜）
│   └── app/
│       └── natrotu6.html       # 游戏主页面
│
├── ⚙️ 后端
│   ├── points-system.js        # 积分系统后端API
│   ├── server.js               # 基础服务器
│   └── package.json            # npm依赖配置
│
├── 📚 资源文件
│   ├── assets/
│   │   └── img/
│   │       └── naruto_team.png # 火影忍者图片
│   ├── auth/
│   │   └── logo/               # 火影头像 (1.png - 10.png)
│   └── words/
│       ├── verbs.json          # 动词词库
│       ├── primary.json        # 小学词库
│       └── cet4.json           # 四级词库
│
└── 🧪 测试文件
    ├── test-standalone.js      # 单元测试
    ├── test-integration.js     # 集成测试
    └── start.js                # 启动脚本
```

## 💰 积分规则

| 动作 | 积分 |
|------|------|
| 注册 | +100 |
| 每日登录 | +10 |
| 答对1题 | +5 |
| 连续答对3题 | +10 额外 |
| 连续答对5题 | +25 额外 |
| 连续答对10题 | +50 额外 |
| 答错1题 | -2 |

## 🎮 游戏规则

1. **选择词库**：动词、小学、四级
2. **选择数量**：5、10、15、20题
3. **开始游戏**：看中文释义，输入英文单词
4. **获得积分**：答对得分，连续答对有额外奖励
5. **攀登阶梯**：答对越多，忍者爬得越高

## 🏆 段位系统

| 积分 | 段位 |
|------|------|
| 0-999 | 下忍 |
| 1000-2999 | 中忍 |
| 3000-5999 | 上忍 |
| 6000-9999 | 精英上忍 |
| 10000+ | 影 |

## 🔧 API 接口

### 用户管理
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `GET /profile` - 获取用户信息

### 游戏
- `POST /game/complete` - 完成游戏并更新积分

### 排行榜
- `GET /leaderboard?type=total` - 总积分榜
- `GET /leaderboard?type=daily` - 今日积分榜

## 📱 访问地址

| 页面 | 地址 |
|------|------|
| 首页 | `index.html` |
| 游戏页 | `app/natrotu6.html` |
| API | http://localhost:3000 |

## 🔐 默认测试账号

注册后即可使用，无需预置账号。

## 📊 技术栈

- **前端**: HTML5 + CSS3 + JavaScript
- **后端**: Node.js + Express
- **数据库**: MongoDB
- **认证**: JWT Token
- **密码加密**: bcrypt

## 🎯 功能列表

- ✅ 用户注册和登录
- ✅ JWT Token认证
- ✅ 密码加密存储
- ✅ 游戏积分系统
- ✅ 排行榜系统
- ✅ 段位系统
- ✅ 多种词库
- ✅ 连续答对奖励
- ✅ 实时进度追踪

## 🛠️ 配置

### 环境变量

```bash
export JWT_SECRET=your-secret-key
export PORT=3000
export MONGODB_URI=mongodb://localhost:27017/natrotu4
```

## 📞 支持

如有问题，请检查：
1. MongoDB 是否运行
2. 端口 3000 是否被占用
3. 网络连接是否正常

---

**享受火影背单词的乐趣！🔥🎮**