// 全站只用这一段脚本切换主题，页面布局交给 CSS。
const themeButton = document.querySelector(".theme-button");

// 记住用户上次选择的主题，刷新后自动恢复
const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    themeButton.textContent = "☀️";
}

// 按钮图标之外也提供文字名称，方便屏幕阅读器识别。
themeButton.setAttribute("aria-label",
    savedTheme === "dark" ? "Switch to light mode" : "Switch to dark mode");

// 监听按钮的点击事件
themeButton.addEventListener("click", function () {

    // 给 body 添加或移除 dark-mode 类
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        // 当前是黑夜模式，按钮显示太阳
        themeButton.textContent = "☀️";
        themeButton.setAttribute("aria-label", "Switch to light mode");
        localStorage.setItem("theme", "dark");
    } else {
        // 当前是白天模式，按钮显示月亮
        themeButton.textContent = "🌙";
        themeButton.setAttribute("aria-label", "Switch to dark mode");
        localStorage.setItem("theme", "light");
    }
});

// 笔记中的代码块可直接复制；不支持 Clipboard API 时使用兼容方案。
document.querySelectorAll(".code-copy-button").forEach(function (button) {
    button.addEventListener("click", async function () {
        const code = button.closest(".record-code-block").querySelector("code").textContent;

        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(code);
            } else {
                const textArea = document.createElement("textarea");
                textArea.value = code;
                textArea.setAttribute("readonly", "");
                textArea.style.position = "fixed";
                textArea.style.opacity = "0";
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand("copy");
                textArea.remove();
            }

            button.textContent = "Copied";
            window.setTimeout(function () {
                button.textContent = "Copy";
            }, 1600);
        } catch (error) {
            button.textContent = "Copy failed";
            window.setTimeout(function () {
                button.textContent = "Copy";
            }, 1600);
        }
    });
});
