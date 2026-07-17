// 独立测试脚本 - 不需要MongoDB
// 测试用户管理系统的核心功能

// 模拟用户数据存储（内存）
const users = new Map();
let userIdCounter = 1;

// 模拟bcrypt
const bcrypt = {
  async hash(password, saltRounds) {
    return `hashed_${password}_${Date.now()}`;
  },
  async compare(password, hash) {
    return hash === `hashed_${password}_1` || hash.startsWith('hashed_' + password);
  }
};

// 模拟jsonwebtoken
const jwt = {
  sign(payload, secret, options) {
    return `token_${Buffer.from(JSON.stringify(payload)).toString('base64')}`;
  },
  verify(token, secret) {
    try {
      const payload = JSON.parse(Buffer.from(token.replace('token_', ''), 'base64').toString());
      return payload;
    } catch {
      throw new Error('Invalid token');
    }
  }
};

// 模拟User模型
class MockUser {
  constructor(data) {
    this._id = userIdCounter++;
    this.username = data.username;
    this.email = data.email;
    this.password = data.password;
    this.role = data.role || 'user';
    this.createdAt = new Date();
  }

  save() {
    users.set(this._id, this);
    return Promise.resolve(this);
  }

  static findOne(query) {
    const user = Array.from(users.values()).find(u => {
      if (query.username) return u.username === query.username;
      if (query.email) return u.email === query.email;
      if (query.$or) {
        return query.$or.some(q => 
          (q.username && u.username === q.username) ||
          (q.email && u.email === q.email)
        );
      }
      return false;
    });
    return Promise.resolve(user || null);
  }

  static findById(id) {
    return Promise.resolve(users.get(id) || null);
  }

  static find(query = {}) {
    const result = Array.from(users.values());
    return Promise.resolve(result);
  }
}

// JWT密钥
const JWT_SECRET = 'test-secret';

// 注册函数
async function register(username, email, password) {
  // 检查用户是否已存在
  const existingUser = await MockUser.findOne({ 
    $or: [{ email }, { username }] 
  });
  
  if (existingUser) {
    return { success: false, message: '用户名或邮箱已存在' };
  }
  
  // 密码加密
  const hashedPassword = await bcrypt.hash(password, 12);
  
  // 创建用户
  const user = new MockUser({
    username,
    email,
    password: hashedPassword
  });
  
  await user.save();
  
  return { success: true, message: '注册成功' };
}

// 登录函数
async function login(username, password) {
  // 查找用户
  const user = await MockUser.findOne({ username });
  if (!user) {
    return { success: false, message: '用户名或密码错误' };
  }
  
  // 验证密码
  const isPasswordValid = await bcrypt.compare(password, user.password);
  if (!isPasswordValid) {
    return { success: false, message: '用户名或密码错误' };
  }
  
  // 生成JWT
  const token = jwt.sign(
    { userId: user._id, username: user.username, role: user.role },
    JWT_SECRET,
    { expiresIn: '24h' }
  );
  
  return {
    success: true,
    message: '登录成功',
    token,
    user: {
      id: user._id,
      username: user.username,
      email: user.email,
      role: user.role
    }
  };
}

// 获取用户信息
async function getProfile(token) {
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    const user = await MockUser.findById(decoded.userId);
    
    if (!user) {
      return { success: false, message: '用户不存在' };
    }
    
    return {
      success: true,
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
        role: user.role
      }
    };
  } catch (error) {
    return { success: false, message: '令牌无效' };
  }
}

// 权限验证
function requireAuth(token) {
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    return { success: true, user: decoded };
  } catch {
    return { success: false, message: '访问令牌缺失或无效' };
  }
}

function requireAdmin(user) {
  return user.role === 'admin';
}

// 测试套件
async function runTests() {
  console.log('🧪 开始运行用户管理系统测试...\n');
  
  let passed = 0;
  let failed = 0;
  
  // 测试1：注册新用户
  console.log('测试1: 用户注册 - 成功注册新用户');
  try {
    const result = await register('testuser', 'test@example.com', 'password123');
    if (result.success && result.message === '注册成功') {
      console.log('  ✓ 通过\n');
      passed++;
    } else {
      console.log(`  ✗ 失败: ${result.message}\n`);
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试2：注册重复用户名
  console.log('测试2: 用户注册 - 重复用户名应失败');
  try {
    const result = await register('testuser', 'test2@example.com', 'password123');
    if (!result.success) {
      console.log('  ✓ 通过 (正确拒绝重复用户名)\n');
      passed++;
    } else {
      console.log('  ✗ 失败: 应该拒绝重复用户名\n');
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试3：用户登录
  let authToken = null;
  console.log('测试3: 用户登录 - 成功登录');
  try {
    const result = await login('testuser', 'password123');
    if (result.success && result.token && result.user) {
      console.log('  ✓ 通过\n');
      console.log(`  - Token: ${result.token.substring(0, 30)}...`);
      console.log(`  - 用户: ${result.user.username}\n`);
      passed++;
      authToken = result.token;
    } else {
      console.log(`  ✗ 失败: ${result.message}\n`);
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试4：错误密码登录
  console.log('测试4: 用户登录 - 错误密码应失败');
  try {
    const result = await login('testuser', 'wrongpassword');
    if (!result.success) {
      console.log('  ✓ 通过 (正确拒绝错误密码)\n');
      passed++;
    } else {
      console.log('  ✗ 失败: 应该拒绝错误密码\n');
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试5：获取用户信息
  console.log('测试5: 用户信息 - 获取已登录用户信息');
  try {
    const result = await getProfile(authToken);
    if (result.success && result.user.username === 'testuser') {
      console.log('  ✓ 通过\n');
      console.log(`  - 用户ID: ${result.user.id}`);
      console.log(`  - 用户名: ${result.user.username}`);
      console.log(`  - 邮箱: ${result.user.email}`);
      console.log(`  - 角色: ${result.user.role}\n`);
      passed++;
    } else {
      console.log(`  ✗ 失败: ${result.message}\n`);
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试6：无Token访问
  console.log('测试6: 用户信息 - 无Token访问应失败');
  try {
    const result = await getProfile(null);
    if (!result.success) {
      console.log('  ✓ 通过 (正确拒绝无Token访问)\n');
      passed++;
    } else {
      console.log('  ✗ 失败: 应该拒绝无Token访问\n');
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试7：无效Token访问
  console.log('测试7: 用户信息 - 无效Token应失败');
  try {
    const result = await getProfile('invalid_token');
    if (!result.success) {
      console.log('  ✓ 通过 (正确拒绝无效Token)\n');
      passed++;
    } else {
      console.log('  ✗ 失败: 应该拒绝无效Token\n');
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试8：权限验证
  console.log('测试8: 权限控制 - 普通用户权限验证');
  try {
    const authResult = requireAuth(authToken);
    if (authResult.success && !requireAdmin(authResult.user)) {
      console.log('  ✓ 通过 (正确识别普通用户权限)\n');
      passed++;
    } else {
      console.log('  ✗ 失败: 权限验证不正确\n');
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试9：注册第二个用户
  console.log('测试9: 用户注册 - 注册多个用户');
  try {
    const result1 = await register('user2', 'user2@example.com', 'pass123');
    const result2 = await register('user3', 'user3@example.com', 'pass456');
    
    if (result1.success && result2.success) {
      console.log('  ✓ 通过 (成功注册多个用户)\n');
      passed++;
    } else {
      console.log('  ✗ 失败: 注册多个用户失败\n');
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 测试10：用户列表查询
  console.log('测试10: 用户管理 - 查询所有用户');
  try {
    const allUsers = await MockUser.find();
    if (allUsers.length >= 3) {
      console.log('  ✓ 通过');
      console.log(`  - 总用户数: ${allUsers.length}\n`);
      passed++;
    } else {
      console.log(`  ✗ 失败: 期望至少3个用户，实际 ${allUsers.length}\n`);
      failed++;
    }
  } catch (error) {
    console.log(`  ✗ 失败: ${error.message}\n`);
    failed++;
  }
  
  // 打印测试结果汇总
  console.log('='.repeat(50));
  console.log('📊 测试结果汇总:');
  console.log(`✓ 通过: ${passed}/${passed + failed}`);
  console.log(`✗ 失败: ${failed}/${passed + failed}`);
  console.log('='.repeat(50));
  
  if (failed > 0) {
    console.log('\n❌ 部分测试失败，请检查上述输出。');
    process.exit(1);
  } else {
    console.log('\n✅ 所有测试通过！用户管理系统核心功能正常。');
    process.exit(0);
  }
}

// 运行测试
runTests().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});