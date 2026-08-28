// 找到页面中的主题切换按钮
const themeButton = document.querySelector(".theme-button");

// 记住用户上次选择的主题，刷新后自动恢复
const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    themeButton.textContent = "☀️";
}

// 监听按钮的点击事件
themeButton.addEventListener("click", function () {

    // 给 body 添加或移除 dark-mode 类
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        // 当前是黑夜模式，按钮显示太阳
        themeButton.textContent = "☀️";
        localStorage.setItem("theme", "dark");
    } else {
        // 当前是白天模式，按钮显示月亮
        themeButton.textContent = "🌙";
        localStorage.setItem("theme", "light");
    }
});
