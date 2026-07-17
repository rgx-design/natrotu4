/**
 * 游戏流程集成测试
 * 测试：注册 → 登录 → 游戏 → 积分 → 排行榜
 */

const http = require('http');

// API 基础地址
const API_BASE = 'http://localhost:3000';

// 颜色输出
const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[36m',
    reset: '\x1b[0m'
};

function log(type, msg) {
    const symbols = {
        pass: `${colors.green}✅`,
        fail: `${colors.red}❌`,
        info: `${colors.blue}ℹ️`,
        warn: `${colors.yellow}⚠️`
    };
    console.log(`${symbols[type] || '•'} ${colors.reset}${msg}`);
}

// 发送 HTTP 请求
function request(method, path, data = null, token = null) {
    return new Promise((resolve, reject) => {
        const url = new URL(path, API_BASE);
        const options = {
            hostname: url.hostname,
            port: url.port,
            path: url.pathname + url.search,
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (token) {
            options.headers['Authorization'] = `Bearer ${token}`;
        }

        const req = http.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    const json = body ? JSON.parse(body) : {};
                    resolve({ status: res.statusCode, data: json });
                } catch (e) {
                    resolve({ status: res.statusCode, data: body });
                }
            });
        });

        req.on('error', reject);
        req.setTimeout(5000, () => {
            req.destroy();
            reject(new Error('请求超时'));
        });

        if (data) {
            req.write(JSON.stringify(data));
        }
        req.end();
    });
}

// 生成随机用户名
function randomUser() {
    return `testuser_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
}

// 测试报告
const report = {
    passed: 0,
    failed: 0,
    tests: []
};

function addTest(name, passed, details = '') {
    if (passed) {
        report.passed++;
        log('pass', name);
    } else {
        report.failed++;
        log('fail', `${name}${details ? ': ' + details : ''}`);
    }
    report.tests.push({ name, passed, details });
}

// ==================== 测试流程 ====================

async function runTests() {
    console.log('\n' + '='.repeat(50));
    console.log('🔥 火影背单词 - 游戏流程集成测试');
    console.log('='.repeat(50) + '\n');

    let authToken = null;
    let testUser = null;

    // ==================== 1. 用户注册 ====================
    log('info', '【测试 1】用户注册');
    console.log('-'.repeat(40));

    try {
        testUser = {
            username: randomUser(),
            email: `${Date.now()}@test.com`,
            password: 'test123456'
        };

        const regRes = await request('POST', '/register', testUser);
        
        if (regRes.status === 201 || regRes.status === 200) {
            addTest('注册成功', true);
            if (regRes.data.token) {
                authToken = regRes.data.token;
                addTest('获得 Token', true);
            } else {
                addTest('获得 Token', false, '未返回 token');
            }
            
            // 检查初始积分
            if (regRes.data.initialPoints === 100) {
                addTest('初始积分 100', true);
            } else {
                addTest('初始积分 100', false, `实际: ${regRes.data.initialPoints}`);
            }
        } else {
            addTest('注册成功', false, `状态码: ${regRes.status}`);
        }
    } catch (e) {
        addTest('注册成功', false, e.message);
    }

    // ==================== 2. 重复注册检测 ====================
    log('info', '\n【测试 2】重复注册检测');
    console.log('-'.repeat(40));

    try {
        const dupRes = await request('POST', '/register', testUser);
        
        if (dupRes.status === 400 || dupRes.status === 409) {
            addTest('重复注册被拒绝', true);
        } else {
            addTest('重复注册被拒绝', false, `状态码: ${dupRes.status}`);
        }
    } catch (e) {
        addTest('重复注册被拒绝', false, e.message);
    }

    // ==================== 3. 用户登录 ====================
    log('info', '\n【测试 3】用户登录');
    console.log('-'.repeat(40));

    try {
        const loginRes = await request('POST', '/login', {
            username: testUser.username,
            password: testUser.password
        });

        if (loginRes.status === 200) {
            addTest('登录成功', true);
            if (loginRes.data.token) {
                authToken = loginRes.data.token;
                addTest('获得登录 Token', true);
            }
            if (loginRes.data.user) {
                addTest('返回用户信息', true);
            }
        } else {
            addTest('登录成功', false, `状态码: ${loginRes.status}`);
        }
    } catch (e) {
        addTest('登录成功', false, e.message);
    }

    // ==================== 4. 错误密码登录 ====================
    log('info', '\n【测试 4】错误密码登录');
    console.log('-'.repeat(40));

    try {
        const wrongRes = await request('POST', '/login', {
            username: testUser.username,
            password: 'wrongpassword'
        });

        if (wrongRes.status === 401 || wrongRes.status === 400) {
            addTest('错误密码被拒绝', true);
        } else {
            addTest('错误密码被拒绝', false, `状态码: ${wrongRes.status}`);
        }
    } catch (e) {
        addTest('错误密码被拒绝', false, e.message);
    }

    // ==================== 5. 获取用户资料 ====================
    log('info', '\n【测试 5】获取用户资料');
    console.log('-'.repeat(40));

    try {
        const profileRes = await request('GET', '/profile', null, authToken);

        if (profileRes.status === 200) {
            addTest('获取资料成功', true);
            if (profileRes.data.user) {
                addTest('返回用户数据', true);
            }
            if (profileRes.data.progress) {
                addTest('返回进度数据', true);
            }
        } else {
            addTest('获取资料成功', false, `状态码: ${profileRes.status}`);
        }
    } catch (e) {
        addTest('获取资料成功', false, e.message);
    }

    // ==================== 6. 完成游戏 ====================
    log('info', '\n【测试 6】完成游戏并获得积分');
    console.log('-'.repeat(40));

    try {
        const gameRes = await request('POST', '/game/complete', {
            correct: 8,
            wrong: 2,
            streak: 5
        }, authToken);

        if (gameRes.status === 200) {
            addTest('游戏完成提交成功', true);
            if (gameRes.data.pointsEarned > 0) {
                addTest(`获得积分: ${gameRes.data.pointsEarned}`, true);
            } else {
                addTest('获得积分', false, '积分为 0');
            }
            if (gameRes.data.totalPoints) {
                addTest(`总积分: ${gameRes.data.totalPoints}`, true);
            }
        } else {
            addTest('游戏完成提交成功', false, `状态码: ${gameRes.status}`);
        }
    } catch (e) {
        addTest('游戏完成提交成功', false, e.message);
    }

    // ==================== 7. 排行榜 ====================
    log('info', '\n【测试 7】排行榜功能');
    console.log('-'.repeat(40));

    try {
        const leaderRes = await request('GET', '/leaderboard?type=total&limit=10');

        if (leaderRes.status === 200) {
            addTest('获取总榜成功', true);
            if (Array.isArray(leaderRes.data) && leaderRes.data.length > 0) {
                addTest(`排行榜有 ${leaderRes.data.length} 名用户`, true);
                
                // 检查测试用户是否在榜上
                const myRank = leaderRes.data.find(u => u.username === testUser.username);
                if (myRank) {
                    addTest(`测试用户排名第 ${myRank.rank}`, true);
                }
            }
        } else {
            addTest('获取总榜成功', false, `状态码: ${leaderRes.status}`);
        }
    } catch (e) {
        addTest('获取总榜成功', false, e.message);
    }

    // ==================== 8. 无效 Token ====================
    log('info', '\n【测试 8】无效 Token 认证');
    console.log('-'.repeat(40));

    try {
        const invalidRes = await request('GET', '/profile', null, 'invalid_token');

        if (invalidRes.status === 401 || invalidRes.status === 403) {
            addTest('无效 Token 被拒绝', true);
        } else {
            addTest('无效 Token 被拒绝', false, `状态码: ${invalidRes.status}`);
        }
    } catch (e) {
        addTest('无效 Token 被拒绝', false, e.message);
    }

    // ==================== 测试报告 ====================
    console.log('\n' + '='.repeat(50));
    console.log('📊 测试报告');
    console.log('='.repeat(50));
    console.log(`\n${colors.green}✅ 通过: ${report.passed}${colors.reset}`);
    console.log(`${colors.red}❌ 失败: ${report.failed}${colors.reset}`);
    console.log(`总计: ${report.passed + report.failed} 项测试\n`);

    if (report.failed > 0) {
        console.log(`${colors.red}失败的测试:${colors.reset}`);
        report.tests.filter(t => !t.passed).forEach(t => {
            console.log(`  • ${t.name}: ${t.details}`);
        });
    }

    console.log('\n' + '='.repeat(50));
    
    // 返回退出码
    process.exit(report.failed > 0 ? 1 : 0);
}

// 运行测试
runTests().catch(err => {
    console.error(`${colors.red}测试执行失败:${colors.reset}`, err.message);
    process.exit(1);
});