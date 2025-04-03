// 在浏览器控制台中运行此脚本，帮助排查登录问题

// 清除登录状态和本地存储
function clearLoginState() {
  console.log("=== 清除登录状态 ===");
  localStorage.removeItem('token');
  localStorage.removeItem('userInfo');
  localStorage.removeItem('userRole');
  console.log("已清除本地存储中的登录信息");
}

// 检查环境和网络
function checkEnvironment() {
  console.log("\n=== 环境检查 ===");
  
  // 检查API基础URL
  const envBaseUrl = process.env.VUE_APP_API_BASE_URL || "";
  console.log("API基础URL:", envBaseUrl);
  
  // 使用fetch API测试API连接
  console.log("测试API连接中...");
  return fetch(`${envBaseUrl}/api/user/login`, {
    method: 'OPTIONS'
  })
  .then(response => {
    console.log(`API连接测试结果: ${response.status} ${response.statusText}`);
    return true;
  })
  .catch(err => {
    console.error("API连接测试失败:", err);
    return false;
  });
}

// 手动执行登录
async function manualLogin(email, password) {
  console.log("\n=== 手动执行登录 ===");
  console.log(`使用账号 ${email} 登录...`);
  
  const baseUrl = process.env.VUE_APP_API_BASE_URL || "http://localhost:5000";
  const loginUrl = `${baseUrl}/api/user/login`;
  
  try {
    const response = await fetch(loginUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });
    
    console.log("登录请求状态:", response.status, response.statusText);
    
    if (response.ok) {
      const data = await response.json();
      console.log("登录成功:", data);
      
      // 存储登录信息
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('userInfo', JSON.stringify(data.user));
      localStorage.setItem('userRole', data.user.role);
      
      console.log("已保存登录状态");
      return true;
    } else {
      const error = await response.json();
      console.error("登录失败:", error);
      return false;
    }
  } catch (err) {
    console.error("登录请求异常:", err);
    return false;
  }
}

// 检查登录状态
function checkLoginState() {
  console.log("\n=== 检查登录状态 ===");
  
  const token = localStorage.getItem('token');
  const userInfo = localStorage.getItem('userInfo');
  const userRole = localStorage.getItem('userRole');
  
  console.log("Token存在:", Boolean(token));
  console.log("用户信息存在:", Boolean(userInfo));
  console.log("用户角色:", userRole);
  
  if (token && userInfo) {
    try {
      const user = JSON.parse(userInfo);
      console.log("用户ID:", user.id);
      console.log("用户名:", user.username);
      console.log("邮箱:", user.email);
      console.log("用户角色:", user.role);
      return true;
    } catch (e) {
      console.error("解析用户信息失败:", e);
      return false;
    }
  }
  
  return false;
}

// 执行全面检查
async function runFullCheck() {
  console.log("======= 登录问题诊断工具 =======");
  
  // 先清除登录状态
  clearLoginState();
  
  // 检查环境
  const envOk = await checkEnvironment();
  if (!envOk) {
    console.error("环境检查失败，请确保后端API正在运行");
    return;
  }
  
  // 测试管理员登录
  console.log("\n正在测试管理员账户登录...");
  const adminLoginOk = await manualLogin("admin2@example.com", "Admin123456");
  
  // 检查登录状态
  if (adminLoginOk) {
    checkLoginState();
    console.log("\n✅ 管理员登录成功，请刷新页面并尝试访问管理员功能");
  } else {
    console.error("\n❌ 管理员登录失败，请检查网络和服务器状态");
  }
}

// 运行诊断
runFullCheck(); 