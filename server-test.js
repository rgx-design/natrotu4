/**
 * 简化版测试服务器 - 使用内存存储
 * 无需 MongoDB 即可运行
 */

const http = require('http');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

// 项目根目录（兼容本地与 Vercel serverless 路径）
const ROOT_DIR = (() => {
    const candidates = [process.cwd(), __dirname, path.join(__dirname, '..')];
    for (const c of candidates) {
        if (fs.existsSync(path.join(c, 'index.html'))) return c;
    }
    return process.cwd();
})();

// ==================== 内存数据存储 ====================
const users = new Map();
const tokens = new Map();
let userIdCounter = 1;

// 积分规则
const POINTS_RULES = {
    DAILY_LOGIN: 10,
    STREAK_BONUS: 5,
    CORRECT_ANSWER: 5,
    WRONG_ANSWER: -2,
    GAME_COMPLETE: 20,
    FIRST_GAME: 50,
    DAILY_GOAL: 30,
    STREAK_CORRECT_3: 10,
    STREAK_CORRECT_5: 25,
    STREAK_CORRECT_10: 50
};

// 初始积分
const INITIAL_POINTS = 100;

// 密码哈希
function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

// 生成 Token
function generateToken() {
    return crypto.randomBytes(32).toString('hex');
}

// ==================== HTTP 服务器 ====================
// 导出 requestHandler 供 Vercel serverless 使用
async function requestHandler(req, res) {
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    const url = new URL(req.url, `http://localhost:${PORT}`);
    const pathname = url.pathname;

    let body = '';
    req.on('data', chunk => body += chunk);

    await new Promise(resolve => req.on('end', resolve));

    let data = {};
    try {
        if (body) data = JSON.parse(body);
    } catch (e) {}

    // Token 验证
    const authHeader = req.headers.authorization;
    let currentUser = null;
    if (authHeader && authHeader.startsWith('Bearer ')) {
        const token = authHeader.slice(7);
        const tokenData = tokens.get(token);
        if (tokenData && tokenData.expires > Date.now()) {
            currentUser = tokenData.user;
        }
    }

    // ==================== 路由 ====================
    
    // 注册
    if (pathname === '/register' && req.method === 'POST') {
        const { username, email, password } = data;

        if (!username || !email || !password) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: '请填写完整信息' }));
            return;
        }

        // 检查用户名重复
        for (const u of users.values()) {
            if (u.username === username) {
                res.writeHead(409, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ message: '用户名已存在' }));
                return;
            }
        }

        // 创建用户
        const user = {
            id: userIdCounter++,
            username,
            email,
            passwordHash: hashPassword(password),
            avatar: 1,
            createdAt: new Date().toISOString()
        };

        // 初始化进度（包含错词本和已学单词）
        user.progress = {
            totalPoints: INITIAL_POINTS,
            dailyPoints: 0,
            streakDays: 1,
            gamesPlayed: 0,
            totalCorrect: 0,
            totalWrong: 0,
            accuracy: 0,
            lastPlayDate: null,
            learnedWords: {},
            wrongWords: [],
            hardModeCorrect: 0
        };

        users.set(user.id, user);

        // 生成 Token
        const token = generateToken();
        tokens.set(token, {
            user: { id: user.id, username: user.username, email: user.email, avatar: user.avatar },
            expires: Date.now() + 7 * 24 * 60 * 60 * 1000
        });

        console.log(`✅ 注册成功: ${username}`);

        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            message: '注册成功',
            token,
            user: { id: user.id, username: user.username, email: user.email, avatar: user.avatar },
            initialPoints: INITIAL_POINTS
        }));
        return;
    }

    // 登录
    if (pathname === '/login' && req.method === 'POST') {
        const { username, password } = data;

        let foundUser = null;
        for (const u of users.values()) {
            if (u.username === username) {
                foundUser = u;
                break;
            }
        }

        if (!foundUser || foundUser.passwordHash !== hashPassword(password)) {
            res.writeHead(401, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: '用户名或密码错误' }));
            return;
        }

        // 生成 Token
        const token = generateToken();
        tokens.set(token, {
            user: { id: foundUser.id, username: foundUser.username, email: foundUser.email, avatar: foundUser.avatar },
            expires: Date.now() + 7 * 24 * 60 * 60 * 1000
        });

        console.log(`✅ 登录成功: ${username}`);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            message: '登录成功',
            token,
            user: { id: foundUser.id, username: foundUser.username, email: foundUser.email, avatar: foundUser.avatar },
            progress: foundUser.progress
        }));
        return;
    }

    // 获取资料
    if (pathname === '/profile' && req.method === 'GET') {
        if (!currentUser) {
            res.writeHead(401, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: '请先登录' }));
            return;
        }

        const user = users.get(currentUser.id);
        if (!user) {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: '用户不存在' }));
            return;
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            user: { id: user.id, username: user.username, email: user.email, avatar: user.avatar },
            progress: user.progress
        }));
        return;
    }

    // 完成游戏
    if (pathname === '/game/complete' && req.method === 'POST') {
        if (!currentUser) {
            res.writeHead(401, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: '请先登录' }));
            return;
        }

        const { correct, wrong, streak } = data;
        const user = users.get(currentUser.id);

        // 计算积分
        const basePoints = correct * POINTS_RULES.CORRECT_ANSWER;
        const wrongDeduct = wrong * POINTS_RULES.WRONG_ANSWER;
        
        // 连续奖励
        let streakBonus = 0;
        if (streak >= 10) streakBonus = POINTS_RULES.STREAK_CORRECT_10;
        else if (streak >= 5) streakBonus = POINTS_RULES.STREAK_CORRECT_5;
        else if (streak >= 3) streakBonus = POINTS_RULES.STREAK_CORRECT_3;

        const gamePoints = POINTS_RULES.GAME_COMPLETE + basePoints + wrongDeduct + streakBonus;
        const actualPoints = Math.max(0, gamePoints);

        // 更新进度（前端发的是累计值，直接覆盖不做累加避免重复计数）
        user.progress.totalPoints += actualPoints;
        user.progress.dailyPoints += actualPoints;
        user.progress.gamesPlayed++;
        user.progress.totalCorrect = correct;  // 前端发的是累计值，直接覆盖
        user.progress.totalWrong = wrong;      // 前端发的是累计值，直接覆盖
        user.progress.accuracy = Math.round((user.progress.totalCorrect / (user.progress.totalCorrect + user.progress.totalWrong)) * 100) || 0;
        user.progress.lastPlayDate = new Date().toISOString();

        // 保存完整学习数据（错词本 + 已学单词 + hardModeCorrect）
        if (data.learnedWords) {
            user.progress.learnedWords = data.learnedWords;
        }
        // 合并错词本：新旧数据合并，避免覆盖丢失
        if (data.wrongWords !== undefined) {
            const existingMap = new Map(user.progress.wrongWords.map(w => [w.word, w]));
            for (const incoming of data.wrongWords) {
                if (existingMap.has(incoming.word)) {
                    // 累加错误次数
                    existingMap.get(incoming.word).wrongCount += incoming.wrongCount;
                } else {
                    // 新增错词
                    existingMap.set(incoming.word, { ...incoming });
                }
            }
            user.progress.wrongWords = Array.from(existingMap.values());
        }
        if (typeof data.hardModeCorrect === 'number') {
            user.progress.hardModeCorrect = data.hardModeCorrect;
        }

        console.log(`🎮 游戏完成: ${user.username} +${actualPoints}分 (正确${correct}, 困难模式正确${data.hardModeCorrect || 0}, 错误${wrong}, 连击${streak})`);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            message: '游戏完成',
            pointsEarned: actualPoints,
            totalPoints: user.progress.totalPoints,
            dailyPoints: user.progress.dailyPoints,
            streakDays: user.progress.streakDays,
            gamesPlayed: user.progress.gamesPlayed,
            totalCorrect: user.progress.totalCorrect,
            totalWrong: user.progress.totalWrong,
            accuracy: user.progress.accuracy,
            hardModeCorrect: user.progress.hardModeCorrect
        }));
        return;
    }

    // 排行榜
    if (pathname.startsWith('/leaderboard') && req.method === 'GET') {
        const type = url.searchParams.get('type') || 'total';
        const limit = parseInt(url.searchParams.get('limit')) || 10;

        // 排序
        const sorted = Array.from(users.values())
            .sort((a, b) => b.progress.totalPoints - a.progress.totalPoints)
            .slice(0, limit)
            .map((u, i) => ({
                rank: i + 1,
                username: u.username,
                avatar: u.avatar,
                points: u.progress.totalPoints,
                dailyPoints: u.progress.dailyPoints,
                wrongWords: u.progress.wrongWords ? u.progress.wrongWords.length : 0,
                totalWrong: u.progress.totalWrong || 0,
                accuracy: u.progress.accuracy || 0
            }));

        console.log(`📊 排行榜查询 (${type}): ${sorted.length} 名用户`);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ leaderboard: sorted }));
        return;
    }

    // 静态文件服务
    if (req.method === 'GET') {
        let filePath = pathname === '/' ? '/index.html' : decodeURIComponent(pathname);
        filePath = path.join(ROOT_DIR, filePath);

        // 安全检查
        if (!filePath.startsWith(ROOT_DIR)) {
            res.writeHead(403);
            res.end('Forbidden');
            return;
        }

        try {
            const content = fs.readFileSync(filePath);
            const ext = path.extname(filePath);
            const contentTypes = {
                '.html': 'text/html; charset=utf-8',
                '.js': 'application/javascript',
                '.css': 'text/css',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.mp3': 'audio/mpeg',
                '.json': 'application/json',
                '.svg': 'image/svg+xml'
            };
            res.writeHead(200, { 'Content-Type': contentTypes[ext] || 'text/plain' });
            res.end(content);
        } catch (e) {
            res.writeHead(404);
            res.end('Not Found');
        }
        return;
    }

    res.writeHead(404);
    res.end('Not Found');
}

// 本地运行时才监听端口（Vercel serverless 不需要）
if (require.main === module) {
    const PORT = process.env.PORT || 3000;
    const server = http.createServer(requestHandler);
    server.listen(PORT, () => {
        console.log('\n' + '='.repeat(50));
        console.log('🔥 火影背单词 - 测试服务器');
        console.log('='.repeat(50));
        console.log(`\n服务器运行在: http://localhost:${PORT}`);
        console.log('\n功能:');
        console.log('  • POST /register  - 用户注册');
        console.log('  • POST /login     - 用户登录');
        console.log('  • GET  /profile   - 获取资料');
        console.log('  • POST /game/complete - 完成游戏');
        console.log('  • GET  /leaderboard - 排行榜');
        console.log('\n内存存储，无需 MongoDB\n');
    });
}

module.exports = requestHandler;