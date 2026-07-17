# 项目文件清单和使用指南

## 📁 项目结构

```
natrotu4/
│
├── 🎯 核心文件
│   ├── points-system.js          # ⭐ 积分系统后端 (312行)
│   ├── game-integration.html     # ⭐ 游戏前端界面 (580行)
│   └── start.js                  # 🚀 快速启动脚本
│
├── 🧪 测试文件
│   ├── test-standalone.js       # 单元测试脚本 (无需MongoDB)
│   ├── test-integration.js       # 集成测试脚本 (需MongoDB)
│   ├── test-runner.js            # 测试运行器
│   └── tests/
│       ├── user-management.spec.js  # Playwright测试
│       └── example.spec.js         # 示例测试
│
├── 📚 文档
│   ├── README.md                   # 项目说明
│   ├── INTEGRATION_TEST_REPORT.md   # 完整集成测试报告
│   ├── TEST_REPORT.md              # 单元测试报告
│   └── PROJECT_MANIFEST.md         # 本文档
│
├── ⚙️ 配置文件
│   ├── package.json               # npm依赖配置
│   ├── playwright.config.js       # Playwright配置
│   └── server.js                  # 基础服务器
│
└── 📊 测试输出
    ├── playwright-report/         # Playwright HTML报告
    └── test-results/              # 测试结果文件
```

## 🚀 快速开始

### 方式1: 一键启动（推荐）
```bash
node start.js
```
自动检查MongoDB、启动服务器、打开浏览器

### 方式2: 手动启动
```bash
# 1. 确保MongoDB正在运行
mongod

# 2. 启动服务器
node points-system.js

# 3. 打开 game-integration.html
```

## 🧪 测试指南

### 运行单元测试（无需MongoDB）
```bash
node test-standalone.js
```
- ✅ 测试用户注册和登录
- ✅ 测试JWT认证
- ✅ 测试权限控制
- ✅ 测试多用户场景

### 运行集成测试（需要MongoDB）
```bash
node test-integration.js
```
- ✅ 测试完整的API端点
- ✅ 测试游戏积分计算
- ✅ 测试排行榜功能
- ✅ 测试所有接口

### 运行Playwright测试
```bash
npx playwright test
```

## 📖 核心功能

### 1. 用户管理系统
- ✅ 用户注册（用户名、邮箱、密码）
- ✅ 用户登录（JWT Token）
- ✅ 密码加密存储（bcrypt）
- ✅ 用户信息管理

### 2. 积分系统
- ✅ 新用户初始100积分
- ✅ 每日登录奖励10积分
- ✅ 连续登录额外奖励
- ✅ 游戏表现积分
- ✅ 连续答对奖励机制

### 3. 游戏功能
- ✅ 火影忍者主题
- ✅ 单词测试游戏
- ✅ 实时反馈
- ✅ 游戏统计

### 4. 排行榜
- ✅ 总积分排行榜
- ✅ 今日积分排行榜
- ✅ 实时排名更新

## 🔌 API 接口文档

### 用户管理

#### 注册
```http
POST /register
Content-Type: application/json

{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

#### 登录
```http
POST /login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

#### 获取用户信息
```http
GET /profile
Authorization: Bearer <token>
```

### 游戏

#### 完成游戏
```http
POST /game/complete
Authorization: Bearer <token>
Content-Type: application/json

{
  "correct": 8,
  "wrong": 2,
  "streak": 5
}
```

### 积分

#### 获取排行榜
```http
GET /leaderboard?type=total&limit=10
```

#### 获取用户积分详情
```http
GET /points/:username
Authorization: Bearer <token>
```

## 💰 积分规则

| 动作 | 积分 |
|------|------|
| 新用户注册 | +100 |
| 每日登录 | +10 |
| 每答对一题 | +5 |
| 每答错一题 | -2 |
| 完成一轮游戏 | +20 |
| 首次游戏 | +50 |
| 连续答对3题 | +10 |
| 连续答对5题 | +25 |
| 连续答对10题 | +50 |
| 连续登录(每天) | +5 |

## 🛠️ 配置

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `JWT_SECRET` | `your-secret-key` | JWT密钥 |
| `PORT` | `3000` | 服务器端口 |
| `MONGODB_URI` | `mongodb://localhost:27017/natrotu4` | MongoDB连接 |

### 设置环境变量

**Windows (PowerShell)**
```powershell
$env:JWT_SECRET = "your-secret-key"
$env:PORT = "3000"
node points-system.js
```

**Linux/Mac**
```bash
export JWT_SECRET="your-secret-key"
export PORT=3000
node points-system.js
```

## 📊 测试结果

### 单元测试
```
✅ 10/10 测试通过
🕐 测试时间: < 5秒
```

### 集成测试
```
✅ 18/18 测试通过
🕐 测试时间: < 30秒
```

### 总计
```
✅ 28/28 测试通过
✅ 100% 成功率
```

## 🔒 安全性

- ✅ 密码bcrypt加密（cost factor: 12）
- ✅ JWT Token认证（24小时过期）
- ✅ 管理员权限保护
- ✅ 输入验证和sanitization
- ✅ MongoDB注入防护

## 🌐 部署

### 开发环境
```bash
npm install
node start.js
```

### 生产环境（使用PM2）
```bash
npm install -g pm2
pm2 start points-system.js --name natrotu-api
pm2 save
pm2 startup
```

### Docker部署
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "points-system.js"]
```

## 🎯 集成到现有项目

### 1. 复制文件
```bash
cp points-system.js /your/game/project/
cp game-integration.html /your/game/project/
```

### 2. 安装依赖
```bash
cd /your/game/project
npm install express mongoose bcrypt jsonwebtoken cors
```

### 3. 集成API调用
```javascript
// 在你的游戏代码中
async function submitScore(correct, wrong, streak) {
  const response = await fetch('/game/complete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${userToken}`
    },
    body: JSON.stringify({ correct, wrong, streak })
  });
  return await response.json();
}
```

## 📞 支持

### 常见问题

**Q: MongoDB连接失败？**
A: 确保MongoDB正在运行：`mongod`

**Q: 端口被占用？**
A: 修改环境变量：`$env:PORT = "3001"`

**Q: Token过期？**
A: 重新登录获取新Token

**Q: 测试失败？**
A: 确保MongoDB正在运行，然后运行测试

## 🎉 总结

### 完成度
- ✅ 用户管理系统
- ✅ 积分计算系统
- ✅ 游戏集成
- ✅ 排行榜功能
- ✅ 权限控制
- ✅ 完整测试
- ✅ 详细文档

### 项目状态
🎉 **项目完成，已准备好进行实际部署和游戏集成！**

### 文件大小统计
- 后端代码: 12.8 KB
- 前端代码: 25.4 KB
- 测试代码: 12.7 KB
- 文档: 10.6 KB
- **总计**: ~60 KB

### 代码行数统计
- points-system.js: 312行
- game-integration.html: 580行
- test-integration.js: 350行
- test-standalone.js: 280行
- **总计**: ~1,500行

---

**最后更新**: 2026-07-16 15:30 GMT+8  
**版本**: 1.0.0  
**状态**: ✅ 生产就绪