// 简化的用户管理系统测试脚本
// 测试核心功能而不需要MongoDB

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
async function runTests() {
  console.log('🧪 开始运行用户管理系统测试...\n');

  // 等待服务器启动
  console.log('等待服务器启动...');
  await new Promise(resolve => setTimeout(resolve, 2000));

  // 测试1：注册新用户
  await test('用户注册 - 成功注册新用户', async () => {
    const response = await request('POST', '/register', {
      username: 'testuser',
      email: 'test@example.com',
      password: 'password123'
    });
    
    if (response.status !== 201) {
      throw new Error(`期望状态码 201，实际 ${response.status}`);
    }
    if (response.data.message !== '注册成功') {
      throw new Error(`期望消息 "注册成功"，实际 "${response.data.message}"`);
    }
  });

  // 测试2：注册重复用户名
  await test('用户注册 - 重复用户名应失败', async () => {
    const response = await request('POST', '/register', {
      username: 'testuser',
      email: 'test2@example.com',
      password: 'password123'
    });
    
    if (response.status !== 400) {
      throw new Error(`期望状态码 400，实际 ${response.status}`);
    }
  });

  // 测试3：用户登录
  await test('用户登录 - 成功登录', async () => {
    const response = await request('POST', '/login', {
      username: 'testuser',
      password: 'password123'
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    if (!response.data.token) {
      throw new Error('期望返回 token，实际未返回');
    }
    if (!response.data.user) {
      throw new Error('期望返回 user 信息，实际未返回');
    }
    
    authToken = response.data.token;
  });

  // 测试4：错误密码登录
  await test('用户登录 - 错误密码应失败', async () => {
    const response = await request('POST', '/login', {
      username: 'testuser',
      password: 'wrongpassword'
    });
    
    if (response.status !== 400) {
      throw new Error(`期望状态码 400，实际 ${response.status}`);
    }
  });

  // 测试5：获取用户信息（需要认证）
  await test('用户信息 - 获取已登录用户信息', async () => {
    const response = await request('GET', '/profile', null, {
      'Authorization': `Bearer ${authToken}`
    });
    
    if (response.status !== 200) {
      throw new Error(`期望状态码 200，实际 ${response.status}`);
    }
    if (response.data.username !== 'testuser') {
      throw new Error(`期望用户名 "testuser"，实际 "${response.data.username}"`);
    }
  });

  // 测试6：无Token访问受保护资源
  await test('用户信息 - 无Token访问应失败', async () => {
    const response = await request('GET', '/profile');
    
    if (response.status !== 401) {
      throw new Error(`期望状态码 401，实际 ${response.status}`);
    }
  });

  // 测试7：无效Token访问
  await test('用户信息 - 无效Token应失败', async () => {
    const response = await request('GET', '/profile', null, {
      'Authorization': 'Bearer invalid_token'
    });
    
    if (response.status !== 403) {
      throw new Error(`期望状态码 403，实际 ${response.status}`);
    }
  });

  // 测试8：普通用户不能访问管理员接口
  await test('权限控制 - 普通用户不能访问管理员接口', async () => {
    const response = await request('GET', '/admin/users', null, {
      'Authorization': `Bearer ${authToken}`
    });
    
    if (response.status !== 403) {
      throw new Error(`期望状态码 403，实际 ${response.status}`);
    }
  });

  // 打印测试结果汇总
  console.log('\n📊 测试结果汇总:');
  const passed = testResults.filter(r => r.passed).length;
  const failed = testResults.filter(r => !r.passed).length;
  console.log(`通过: ${passed}/${testResults.length}`);
  console.log(`失败: ${failed}/${testResults.length}`);

  if (failed > 0) {
    console.log('\n失败的测试:');
    testResults.filter(r => !r.passed).forEach(r => {
      console.log(`  - ${r.description}: ${r.error}`);
    });
    process.exit(1);
  } else {
    console.log('\n✅ 所有测试通过！');
    process.exit(0);
  }
}

// 运行测试
runTests().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});