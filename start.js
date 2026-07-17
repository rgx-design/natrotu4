// 快速启动脚本
// 一键启动积分系统服务器和前端界面

const { exec, spawn } = require('child_process');
const readline = require('readline');

console.log('='.repeat(60));
console.log('🎮 火影单词速记 - 积分系统启动器');
console.log('='.repeat(60));
console.log();

// 检查MongoDB是否运行
function checkMongoDB() {
  return new Promise((resolve) => {
    const mongo = exec('mongod --version', (error) => {
      if (error) {
        console.log('⚠️  MongoDB 未安装或未启动');
        console.log('   请先安装并启动 MongoDB');
        console.log('   下载地址: https://www.mongodb.com/try/download/community');
        console.log();
        resolve(false);
      } else {
        console.log('✅ MongoDB 已安装');
        resolve(true);
      }
    });
  });
}

// 启动服务器
function startServer() {
  return new Promise((resolve, reject) => {
    console.log('🚀 启动积分系统服务器...');
    
    const server = spawn('node', ['points-system.js'], {
      cwd: process.cwd(),
      stdio: 'pipe'
    });

    server.stdout.on('data', (data) => {
      const output = data.toString();
      console.log(output);
      
      if (output.includes('运行在端口')) {
        console.log();
        console.log('✅ 服务器启动成功！');
        console.log();
        resolve(server);
      }
    });

    server.stderr.on('data', (data) => {
      console.error(data.toString());
    });

    server.on('error', (error) => {
      console.error('❌ 服务器启动失败:', error.message);
      reject(error);
    });

    // 超时检测
    setTimeout(() => {
      console.log('⚠️  服务器启动超时...');
    }, 10000);
  });
}

// 打开浏览器
function openBrowser() {
  const os = require('os');
  const path = require('path');
  
  const htmlPath = path.join(process.cwd(), 'game-integration.html');
  const url = `file://${htmlPath}`;
  
  console.log('🌐 打开前端界面...');
  
  let command;
  switch (os.platform()) {
    case 'win32':
      command = `start "" "${url}"`;
      break;
    case 'darwin':
      command = `open "${url}"`;
      break;
    case 'linux':
      command = `xdg-open "${url}"`;
      break;
    default:
      command = `open "${url}"`;
  }
  
  exec(command, (error) => {
    if (error) {
      console.error('❌ 打开浏览器失败');
    } else {
      console.log('✅ 浏览器已打开');
    }
  });
}

// 显示帮助信息
function showHelp() {
  console.log();
  console.log('📖 使用说明:');
  console.log();
  console.log('1. 确保MongoDB正在运行');
  console.log('2. 服务器将自动启动在 http://localhost:3000');
  console.log('3. 前端界面将在浏览器中打开');
  console.log();
  console.log('📝 可用命令:');
  console.log('   npm start     - 启动服务器');
  console.log('   node test-standalone.js - 运行独立测试');
  console.log('   node test-integration.js - 运行集成测试');
  console.log();
  console.log('🔧 配置环境变量:');
  console.log('   JWT_SECRET    - JWT密钥');
  console.log('   PORT          - 服务器端口');
  console.log('   MONGODB_URI   - MongoDB连接字符串');
  console.log();
  console.log('='.repeat(60));
}

// 主函数
async function main() {
  try {
    showHelp();
    
    // 检查MongoDB
    const mongoReady = await checkMongoDB();
    
    if (!mongoReady) {
      console.log('⚠️  警告: MongoDB未运行，部分功能可能不可用');
      console.log('   可以先启动MongoDB，或者使用test-standalone.js进行测试');
      console.log();
      
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });
      
      await new Promise((resolve) => {
        rl.question('是否继续启动服务器？(y/n): ', (answer) => {
          rl.close();
          if (answer.toLowerCase() === 'y') {
            resolve();
          } else {
            console.log('已退出');
            process.exit(0);
          }
        });
      });
    }
    
    // 启动服务器
    const server = await startServer();
    
    // 打开浏览器
    openBrowser();
    
    console.log();
    console.log('🎉 系统已启动！');
    console.log('   API地址: http://localhost:3000');
    console.log('   前端界面: game-integration.html');
    console.log();
    console.log('按 Ctrl+C 停止服务器');
    console.log();
    
    // 优雅退出
    process.on('SIGINT', () => {
      console.log();
      console.log('🛑 正在停止服务器...');
      server.kill();
      process.exit(0);
    });
    
  } catch (error) {
    console.error('❌ 启动失败:', error.message);
    process.exit(1);
  }
}

// 导出函数供外部调用
module.exports = {
  startServer,
  openBrowser,
  checkMongoDB
};

// 如果直接运行此脚本
if (require.main === module) {
  main();
}