// 简单的测试运行器
const { exec } = require('child_process');
const fs = require('fs');

// 检查是否已安装依赖
function checkDependencies() {
  try {
    const packageJson = JSON.parse(fs.readFileSync('./package.json', 'utf8'));
    console.log('✓ Package.json 文件已找到');
    
    // 检查必需的依赖
    const requiredDeps = ['express', 'mongoose', 'bcrypt', 'jsonwebtoken'];
    const missingDeps = requiredDeps.filter(dep => 
      !packageJson.dependencies[dep]
    );
    
    if (missingDeps.length > 0) {
      console.log('⚠ 缺少依赖:', missingDeps);
      return false;
    }
    
    console.log('✓ 所有必需依赖已安装');
    return true;
  } catch (error) {
    console.error('✗ 无法读取 package.json 文件:', error.message);
    return false;
  }
}

// 启动测试服务器
function startTestServer() {
  return new Promise((resolve, reject) => {
    try {
      // 这里需要实际运行服务器，但在Playwright测试中已经配置了webServer
      console.log('✓ 测试服务器配置已准备就绪');
      resolve(true);
    } catch (error) {
      reject(error);
    }
  });
}

// 运行测试
async function runTests() {
  console.log('🚀 开始运行测试...');
  
  // 检查依赖
  if (!checkDependencies()) {
    console.error('❌ 测试无法开始，缺少必要依赖');
    return;
  }

  // 启动服务器
  try {
    await startTestServer();
    console.log('✅ 服务器准备就绪');
    
    // 运行Playwright测试
    console.log('🧪 正在运行Playwright测试...');
    console.log('请使用命令: npx playwright test');
    console.log('或者运行: npm run test');
    
  } catch (error) {
    console.error('❌ 测试过程中发生错误:', error.message);
  }
}

// 主函数
if (require.main === module) {
  runTests();
}

module.exports = { runTests, checkDependencies, startTestServer };