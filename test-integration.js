// 完整的积分系统集成测试
// 测试用户注册、登录、游戏、积分获取等全部功能

const http = require('http');

// 测试配置
const BASE_URL = 'http://localhost:3000';
let authToken = null;
let testResults = [];

// 辅助函数：发送HTTP请求
function request(method, path, data = null, headers = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          resolve({
            status: res.statusCode,
            data: body ? JSON.parse(body) : null
          });
        } catch (e) {
          resolve({
            status: res.statusCode,
            data: body
          });
        }
      });
    });

    req.on('error', reject);
    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

// 测试用例
async function test(description, fn) {
  try {
    await fn();
    testResults.push({ description, passed: true });
    console.log(`✓ ${description}`);
  } catch (error) {
    testResults.push({ description, passed: false, error: error.message });
    console.log(`✗ ${description}: ${error.message}`);
  }
}

// 测试套件
async function runIntegrationTests() {
  console.log('🧪 开始运行完整积分系统集成测试...\n');

  // 等待服务器启动
  console.log('等待服务器启动...');
  await new Promise(resolve => setTimeout(resolve, 2000));

  // ==================== 用户管理测试 ====================
  console.log('\n📝 用户管理功能测试\n');

  // 测试1：注册新用户
  await test('用户注册 - 成功注册新用户', async () => {
    const response = await request('POST', '/register', {
      username: 'gamer001',
      email: 'gamer001@example.com',
      password: 'password123'
    });
    
    if (response.status !== 201) {
      throw new Error(`期望状态码 201，实际 ${response.status}`);
    }
    if (response.data.message !== '注册成功') {
      throw new Error(`期望消息 "注册成功"，实际 "${response.data.message}"`);
    }
    if (typeof response.data.initialPoints !== 'number') {
      throw new Error('期望返回初始积分');
    }
    console.log(`    初始积分: ${response.data.initialPoints}`);
  });

  // 测试2：注册重复用户名
  await test('用户注册 - 重复用户名应失败', async () => {
    const response = await request('POST', '/register', {
      username: 'gamer001',
      email: 'gamer002@example.com',
      password: 'password123'
    });
    
    if (response.status !== 400) {
      throw new Error(`期望状态码 400，实际 ${response.status}`);
    }
  });

  // 测试3：用户登录
  await test('用户登录 - 成功登录并获取初始积分', async () => {
    const response = await request('POST', '/login', {
      username: 'gamer001',
      password: 'password123'
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    if (!response.data.token) {
      throw new Error('期望返回 token');
    }
    if (!response.data.progress) {
      throw new Error('期望返回用户进度信息');
    }
    
    authToken = response.data.token;
    console.log(`    登录积分: ${response.data.progress.totalPoints}`);
    console.log(`    连续登录: ${response.data.progress.streakDays} 天`);
  });

  // 测试4：错误密码登录
  await test('用户登录 - 错误密码应失败', async () => {
    const response = await request('POST', '/login', {
      username: 'gamer001',
      password: 'wrongpassword'
    });
    
    if (response.status !== 400) {
      throw new Error(`期望状态码 400，实际 ${response.status}`);
    }
  });

  // 测试5：获取用户信息
  await test('用户信息 - 获取完整用户信息和进度', async () => {
    const response = await request('GET', '/profile', null, {
      'Authorization': `Bearer ${authToken}`
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    if (!response.data.user || !response.data.progress) {
      throw new Error('期望返回用户信息和进度');
    }
    console.log(`    用户: ${response.data.user.username}`);
    console.log(`    总积分: ${response.data.progress.totalPoints}`);
    console.log(`    游戏次数: ${response.data.progress.gamesPlayed}`);
  });

  // ==================== 游戏功能测试 ====================
  console.log('\n🎮 游戏功能测试\n');

  // 测试6：完成游戏并获取积分
  await test('游戏完成 - 完成游戏获得积分', async () => {
    const response = await request('POST', '/game/complete', {
      correct: 8,
      wrong: 2,
      streak: 5
    }, {
      'Authorization': `Bearer ${authToken}`
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    if (typeof response.data.pointsEarned !== 'number') {
      throw new Error('期望返回积分');
    }
    console.log(`    本次获得积分: ${response.data.pointsEarned}`);
    console.log(`    总积分: ${response.data.totalPoints}`);
    console.log(`    游戏次数: ${response.data.gamesPlayed}`);
  });

  // 测试7：再次完成游戏
  await test('游戏完成 - 多次游戏积分累加', async () => {
    const response = await request('POST', '/game/complete', {
      correct: 10,
      wrong: 0,
      streak: 10
    }, {
      'Authorization': `Bearer ${authToken}`
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    const previousPoints = 110; // 初始100 + 第一次游戏10
    if (response.data.totalPoints <= previousPoints) {
      throw new Error('积分应该累加');
    }
    console.log(`    本次获得积分: ${response.data.pointsEarned}`);
    console.log(`    总积分: ${response.data.totalPoints}`);
  });

  // 测试8：无Token玩游戏应失败
  await test('游戏完成 - 无Token应失败', async () => {
    const response = await request('POST', '/game/complete', {
      correct: 5,
      wrong: 5,
      streak: 0
    });
    
    if (response.status !== 401) {
      throw new Error(`期望状态码 401，实际 ${response.status}`);
    }
  });

  // ==================== 积分系统测试 ====================
  console.log('\n💰 积分系统测试\n');

  // 测试9：获取积分详情
  await test('积分详情 - 获取用户积分统计', async () => {
    const response = await request('GET', '/points/gamer001', null, {
      'Authorization': `Bearer ${authToken}`
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    console.log(`    总积分: ${response.data.totalPoints}`);
    console.log(`    答对总数: ${response.data.totalCorrect}`);
    console.log(`    答错总数: ${response.data.totalWrong}`);
    console.log(`    准确率: ${response.data.accuracy}`);
  });

  // 测试10：获取总积分排行榜
  await test('排行榜 - 获取总积分排行榜', async () => {
    const response = await request('GET', '/leaderboard?type=total&limit=10');
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    if (!Array.isArray(response.data)) {
      throw new Error('期望返回数组');
    }
    console.log(`    排行榜用户数: ${response.data.length}`);
    if (response.data.length > 0) {
      console.log(`    第1名: ${response.data[0].username} - ${response.data[0].points} 积分`);
    }
  });

  // 测试11：获取今日积分排行榜
  await test('排行榜 - 获取今日积分排行榜', async () => {
    const response = await request('GET', '/leaderboard?type=daily&limit=10');
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    if (!Array.isArray(response.data)) {
      throw new Error('期望返回数组');
    }
    console.log(`    今日排行榜用户数: ${response.data.length}`);
  });

  // ==================== 权限控制测试 ====================
  console.log('\n🔐 权限控制测试\n');

  // 测试12：普通用户不能访问管理员接口
  await test('权限控制 - 普通用户不能访问管理员接口', async () => {
    const response = await request('GET', '/admin/users', null, {
      'Authorization': `Bearer ${authToken}`
    });
    
    if (response.status !== 403) {
      throw new Error(`期望状态码 403，实际 ${response.status}`);
    }
  });

  // 测试13：无效Token访问受保护资源
  await test('权限控制 - 无效Token应被拒绝', async () => {
    const response = await request('GET', '/profile', null, {
      'Authorization': 'Bearer invalid_token'
    });
    
    if (response.status !== 403) {
      throw new Error(`期望状态码 403，实际 ${response.status}`);
    }
  });

  // 测试14：无Token访问受保护资源
  await test('权限控制 - 无Token应被拒绝', async () => {
    const response = await request('GET', '/profile');
    
    if (response.status !== 401) {
      throw new Error(`期望状态码 401，实际 ${response.status}`);
    }
  });

  // ==================== 多用户测试 ====================
  console.log('\n👥 多用户测试\n');

  // 测试15：注册第二个用户
  await test('多用户 - 注册第二个用户', async () => {
    const response = await request('POST', '/register', {
      username: 'gamer002',
      email: 'gamer002@example.com',
      password: 'password456'
    });
    
    if (response.status !== 201) {
      throw new Error(`期望状态码 201，实际 ${response.status}`);
    }
  });

  // 测试16：第二个用户登录
  let token2 = null;
  await test('多用户 - 第二个用户登录', async () => {
    const response = await request('POST', '/login', {
      username: 'gamer002',
      password: 'password456'
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    token2 = response.data.token;
    console.log(`    gamer002 登录成功`);
  });

  // 测试17：第二个用户玩游戏
  await test('多用户 - 第二个用户完成游戏', async () => {
    const response = await request('POST', '/game/complete', {
      correct: 5,
      wrong: 5,
      streak: 3
    }, {
      'Authorization': `Bearer ${token2}`
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    console.log(`    gamer002 获得积分: ${response.data.pointsEarned}`);
  });

  // 测试18：排行榜显示多个用户
  await test('多用户 - 排行榜显示多个用户', async () => {
    const response = await request('GET', '/leaderboard?type=total');
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    if (response.data.length < 2) {
      throw new Error('排行榜应该有至少2个用户');
    }
    console.log(`    排行榜共 ${response.data.length} 个用户`);
  });

  // 打印测试结果汇总
  console.log('\n' + '='.repeat(60));
  console.log('📊 测试结果汇总:');
  const passed = testResults.filter(r => r.passed).length;
  const failed = testResults.filter(r => !r.passed).length;
  console.log(`✓ 通过: ${passed}/${testResults.length}`);
  console.log(`✗ 失败: ${failed}/${testResults.length}`);
  console.log('='.repeat(60));

  if (failed > 0) {
    console.log('\n❌ 失败的测试:');
    testResults.filter(r => !r.passed).forEach(r => {
      console.log(`  - ${r.description}: ${r.error}`);
    });
    process.exit(1);
  } else {
    console.log('\n✅ 所有测试通过！积分系统完整功能验证成功。');
    console.log('\n🎉 系统已准备好进行以下操作:');
    console.log('   • 用户管理和认证');
    console.log('   • 游戏积分系统');
    console.log('   • 排行榜功能');
    console.log('   • 权限控制');
    console.log('   • 多用户支持');
    process.exit(0);
  }
}

// 运行测试
runIntegrationTests().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});