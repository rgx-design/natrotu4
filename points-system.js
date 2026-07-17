// 积分管理系统 - 扩展server.js
const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(express.json());
app.use(cors());

// 连接MongoDB
mongoose.connect('mongodb://localhost:27017/natrotu4', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
});

// ==================== 用户模型 ====================
const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user'
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const User = mongoose.model('User', userSchema);

// ==================== 用户进度模型（积分系统） ====================
const userProgressSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    unique: true
  },
  username: {
    type: String,
    required: true
  },
  // 积分相关
  totalPoints: {
    type: Number,
    default: 0
  },
  dailyPoints: {
    type: Number,
    default: 0
  },
  streakDays: {
    type: Number,
    default: 0
  },
  lastLoginDate: {
    type: Date,
    default: Date.now
  },
  lastGameDate: {
    type: String,
    default: ''
  },
  todayStudyWords: {
    type: Number,
    default: 0
  },
  todayStudyTime: {
    type: Number,
    default: 0
  },
  // 游戏统计
  gamesPlayed: {
    type: Number,
    default: 0
  },
  totalCorrect: {
    type: Number,
    default: 0
  },
  totalWrong: {
    type: Number,
    default: 0
  },
  // 学习数据
  learnedWords: {
    type: Map,
    of: {
      correctCount: Number,
      wrongCount: Number,
      lastReview: Date
    },
    default: {}
  },
  wrongWords: {
    type: Array,
    default: []
  },
  customWordbooks: {
    type: Array,
    default: []
  },
  avatar: {
    type: Number,
    default: 1
  }
});

const UserProgress = mongoose.model('UserProgress', userProgressSchema);

// JWT密钥
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

// ==================== 积分规则配置 ====================
const POINTS_RULES = {
  // 每日登录
  DAILY_LOGIN: 10,
  // 连续登录奖励
  STREAK_BONUS: 5, // 每天额外奖励
  // 每正确回答一题
  CORRECT_ANSWER: 5,
  // 每错误回答一题
  WRONG_ANSWER: -2,
  // 完成一轮游戏
  GAME_COMPLETE: 20,
  // 首次游戏
  FIRST_GAME: 50,
  // 每日目标达成
  DAILY_GOAL: 30,
  // 连续答对3题
  STREAK_CORRECT_3: 10,
  // 连续答对5题
  STREAK_CORRECT_5: 25,
  // 连续答对10题
  STREAK_CORRECT_10: 50
};

// ==================== 用户注册路由 ====================
app.post('/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    
    // 检查用户是否已存在
    const existingUser = await User.findOne({ $or: [{ email }, { username }] });
    if (existingUser) {
      return res.status(400).json({ message: '用户名或邮箱已存在' });
    }
    
    // 密码加密
    const hashedPassword = await bcrypt.hash(password, 12);
    
    // 创建用户
    const user = new User({
      username,
      email,
      password: hashedPassword
    });
    
    await user.save();
    
    // 创建用户进度记录
    const userProgress = new UserProgress({
      userId: user._id,
      username: user.username,
      totalPoints: 100, // 新用户初始积分
      dailyPoints: 0,
      lastLoginDate: new Date()
    });
    
    await userProgress.save();
    
    res.status(201).json({ 
      message: '注册成功',
      initialPoints: 100
    });
  } catch (error) {
    console.error('注册错误:', error);
    res.status(500).json({ message: '服务器内部错误' });
  }
});

// ==================== 用户登录路由 ====================
app.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // 查找用户
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(400).json({ message: '用户名或密码错误' });
    }
    
    // 验证密码
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(400).json({ message: '用户名或密码错误' });
    }
    
    // 更新登录信息
    const userProgress = await UserProgress.findOne({ userId: user._id });
    const today = new Date().toISOString().split('T')[0];
    const lastLogin = userProgress.lastLoginDate ? userProgress.lastLoginDate.toISOString().split('T')[0] : null;
    
    // 检查是否连续登录
    if (lastLogin === today) {
      // 今天已经登录，不重复奖励
    } else {
      // 新的一天，发放登录积分
      userProgress.dailyPoints = POINTS_RULES.DAILY_LOGIN;
      userProgress.totalPoints += POINTS_RULES.DAILY_LOGIN;
      
      // 检查连续登录
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = yesterday.toISOString().split('T')[0];
      
      if (lastLogin === yesterdayStr) {
        // 连续登录
        userProgress.streakDays += 1;
        userProgress.totalPoints += POINTS_RULES.STREAK_BONUS * userProgress.streakDays;
      } else {
        // 中断连续登录
        userProgress.streakDays = 1;
      }
      
      userProgress.lastLoginDate = new Date();
    }
    
    await userProgress.save();
    
    // 生成JWT
    const token = jwt.sign(
      { userId: user._id, username: user.username, role: user.role },
      JWT_SECRET,
      { expiresIn: '24h' }
    );
    
    res.json({
      message: '登录成功',
      token,
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
        role: user.role
      },
      progress: {
        totalPoints: userProgress.totalPoints,
        dailyPoints: userProgress.dailyPoints,
        streakDays: userProgress.streakDays
      }
    });
  } catch (error) {
    console.error('登录错误:', error);
    res.status(500).json({ message: '服务器内部错误' });
  }
});

// ==================== JWT验证中间件 ====================
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ message: '访问令牌缺失' });
  }
  
  jwt.verify(token, JWT_SECRET, async (err, user) => {
    if (err) {
      return res.status(403).json({ message: '令牌无效' });
    }
    req.user = user;
    next();
  });
};

// ==================== 获取用户信息路由 ====================
app.get('/profile', authenticateToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId).select('-password');
    if (!user) {
      return res.status(404).json({ message: '用户不存在' });
    }
    
    const progress = await UserProgress.findOne({ userId: req.user.userId });
    
    res.json({
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
        role: user.role
      },
      progress: progress ? {
        totalPoints: progress.totalPoints,
        dailyPoints: progress.dailyPoints,
        streakDays: progress.streakDays,
        gamesPlayed: progress.gamesPlayed,
        totalCorrect: progress.totalCorrect,
        totalWrong: progress.totalWrong,
        avatar: progress.avatar
      } : null
    });
  } catch (error) {
    console.error('获取用户信息错误:', error);
    res.status(500).json({ message: '服务器内部错误' });
  }
});

// ==================== 游戏积分接口 ====================

// 完成游戏后更新积分
app.post('/game/complete', authenticateToken, async (req, res) => {
  try {
    const { correct, wrong, streak } = req.body;
    
    const userProgress = await UserProgress.findOne({ userId: req.user.userId });
    if (!userProgress) {
      return res.status(404).json({ message: '用户进度不存在' });
    }
    
    let pointsEarned = 0;
    
    // 基础积分：答对题目
    pointsEarned += correct * POINTS_RULES.CORRECT_ANSWER;
    
    // 扣分：答错题目
    pointsEarned += wrong * POINTS_RULES.WRONG_ANSWER;
    
    // 完成游戏奖励
    pointsEarned += POINTS_RULES.GAME_COMPLETE;
    
    // 首次游戏额外奖励
    if (userProgress.gamesPlayed === 0) {
      pointsEarned += POINTS_RULES.FIRST_GAME;
    }
    
    // 连续答对奖励
    if (streak >= 10) {
      pointsEarned += POINTS_RULES.STREAK_CORRECT_10;
    } else if (streak >= 5) {
      pointsEarned += POINTS_RULES.STREAK_CORRECT_5;
    } else if (streak >= 3) {
      pointsEarned += POINTS_RULES.STREAK_CORRECT_3;
    }
    
    // 更新用户进度
    userProgress.totalPoints += pointsEarned;
    userProgress.dailyPoints += pointsEarned;
    userProgress.gamesPlayed += 1;
    userProgress.totalCorrect += correct;
    userProgress.totalWrong += wrong;
    userProgress.lastGameDate = new Date().toISOString().split('T')[0];
    
    await userProgress.save();
    
    res.json({
      message: '游戏完成',
      pointsEarned,
      totalPoints: userProgress.totalPoints,
      dailyPoints: userProgress.dailyPoints,
      gamesPlayed: userProgress.gamesPlayed
    });
  } catch (error) {
    console.error('游戏完成错误:', error);
    res.status(500).json({ message: '服务器内部错误' });
  }
});

// 获取积分排行榜
app.get('/leaderboard', async (req, res) => {
  try {
    const { type = 'total', limit = 10 } = req.query;
    
    let sortField = type === 'daily' ? 'dailyPoints' : 'totalPoints';
    
    const leaders = await UserProgress.find()
      .sort({ [sortField]: -1 })
      .limit(parseInt(limit));
    
    const leaderboard = leaders.map((user, index) => ({
      rank: index + 1,
      username: user.username,
      points: type === 'daily' ? user.dailyPoints : user.totalPoints,
      avatar: user.avatar,
      streakDays: user.streakDays
    }));
    
    res.json(leaderboard);
  } catch (error) {
    console.error('获取排行榜错误:', error);
    res.status(500).json({ message: '服务器内部错误' });
  }
});

// 获取用户积分详情
app.get('/points/:username', authenticateToken, async (req, res) => {
  try {
    const userProgress = await UserProgress.findOne({ userId: req.user.userId });
    
    if (!userProgress) {
      return res.status(404).json({ message: '用户进度不存在' });
    }
    
    res.json({
      username: userProgress.username,
      totalPoints: userProgress.totalPoints,
      dailyPoints: userProgress.dailyPoints,
      streakDays: userProgress.streakDays,
      gamesPlayed: userProgress.gamesPlayed,
      totalCorrect: userProgress.totalCorrect,
      totalWrong: userProgress.totalWrong,
      accuracy: userProgress.totalCorrect + userProgress.totalWrong > 0
        ? ((userProgress.totalCorrect / (userProgress.totalCorrect + userProgress.totalWrong)) * 100).toFixed(1) + '%'
        : '0%'
    });
  } catch (error) {
    console.error('获取积分详情错误:', error);
    res.status(500).json({ message: '服务器内部错误' });
  }
});

// 管理员路由（仅管理员可访问）
const requireAdmin = (req, res, next) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ message: '需要管理员权限' });
  }
  next();
};

app.get('/admin/users', authenticateToken, requireAdmin, async (req, res) => {
  try {
    const users = await User.find().select('-password');
    const allProgress = await UserProgress.find();
    
    const usersWithProgress = users.map(user => {
      const progress = allProgress.find(p => p.userId.toString() === user._id.toString());
      return {
        ...user.toObject(),
        progress: progress ? {
          totalPoints: progress.totalPoints,
          dailyPoints: progress.dailyPoints,
          gamesPlayed: progress.gamesPlayed
        } : null
      };
    });
    
    res.json(usersWithProgress);
  } catch (error) {
    console.error('获取用户列表错误:', error);
    res.status(500).json({ message: '服务器内部错误' });
  }
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
  console.log('积分规则配置:');
  console.log(POINTS_RULES);
});

module.exports = app;