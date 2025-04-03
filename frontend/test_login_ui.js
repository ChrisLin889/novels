// 此脚本可以在浏览器控制台中运行，检查登录页面的输入字段
console.log("===== 测试登录页面表单 =====");

// 检查登录表单是否存在
const loginForm = document.querySelector("form");
if (!loginForm) {
  console.error("未找到登录表单");
  return;
}

// 检查输入字段
const accountInput = document.querySelector("input[v-model='loginForm.account']");
if (!accountInput) {
  console.error("未找到账户输入框");
} else {
  console.log("✓ 账户输入框存在");
  console.log("账户输入框类型:", accountInput.type);
  console.log("账户输入框占位符:", accountInput.placeholder);
}

const passwordInput = document.querySelector("input[v-model='loginForm.password']");
if (!passwordInput) {
  console.error("未找到密码输入框");
} else {
  console.log("✓ 密码输入框存在");
  console.log("密码输入框类型:", passwordInput.type);
}

// 检查登录按钮
const loginButton = document.querySelector("button[type='submit']");
if (!loginButton) {
  console.error("未找到登录按钮");
} else {
  console.log("✓ 登录按钮存在");
  console.log("登录按钮文本:", loginButton.textContent.trim());
}

console.log("\n===== 登录测试指南 =====");
console.log("请使用以下账户信息测试登录:");
console.log("1. 管理员账户:");
console.log("   - 邮箱: admin2@example.com");
console.log("   - 密码: Admin123456");
console.log("2. 普通用户账户:");
console.log("   - 邮箱: lsm1248845597@163.com");
console.log("   - 密码: Ok123456789");
console.log("\n注意: 必须使用邮箱登录，不能使用用户名。"); 