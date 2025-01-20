<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Регистрация и Вход</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 400px;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1, h2 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        input {
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px;
            background-color: #4CAF50;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .link {
            text-align: center;
            margin-top: 10px;
        }
        .link a {
            color: #007BFF;
            text-decoration: none;
        }
        .link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>

<div class="container" id="auth-container">
    <h1>Вход</h1>
    <form id="login-form" onsubmit="return false;">
        <input type="email" id="login-email" placeholder="Имейл" required>
        <div>
            <input type="password" id="login-password" placeholder="Парола" required>
            <input type="checkbox" id="show-password-login" onclick="togglePassword('login-password')"> Показване
        </div>
        <button type="button" onclick="login()">Вход</button>
    </form>
    <div class="link">
        <a href="#" onclick="showForgotPassword()">Забравена парола?</a>
    </div>
    <div class="link">
        <a href="#" onclick="showRegistration()">Нямате акаунт? Регистрирайте се</a>
    </div>
</div>

<div class="container" id="register-container" style="display: none;">
    <h2>Регистрация</h2>
    <form id="register-form" onsubmit="return false;">
        <input type="email" id="register-email" placeholder="Имейл" required>
        <div>
            <input type="password" id="register-password" placeholder="Парола" required>
            <input type="checkbox" id="show-password-register" onclick="togglePassword('register-password')"> Показване
        </div>
        <button type="button" onclick="register()">Регистрация</button>
    </form>
    <div class="link">
        <a href="#" onclick="showLogin()">Вече имате акаунт? Влезте</a>
    </div>
</div>

<div class="container" id="forgot-password-container" style="display: none;">
    <h2>Забравена парола</h2>
    <form id="forgot-password-form" onsubmit="return false;">
        <input type="email" id="forgot-email" placeholder="Имейл" required>
        <button type="button" onclick="resetPassword()">Промяна на парола</button>
    </form>
    <div class="link">
        <a href="#" onclick="showLogin()">Върнете се към вход</a>
    </div>
</div>

<div class="container" id="verification-container" style="display: none;">
    <h2>Въведете код за двустепенна автентикация</h2>
    <form id="verification-form" onsubmit="return false;">
        <input type="text" id="verification-code" placeholder="Въведете кода" required>
        <button type="button" onclick="verifyCode()">Потвърди код</button>
    </form>
</div>

<div class="container" id="manager-container" style="display: none;">
    <h2>Мениджър</h2>
    <p>Добре дошли в акаунта си!</p>
    <input type="file" id="file-input" accept=".docx,.pdf,.txt">
    <button onclick="uploadFile()">Качи файл</button>
    <div id="download-link-container" style="display: none; margin-top: 20px;">
        <a id="download-link" href="#" download>Изтегли качения файл</a>
    </div>
    <div class="link">
        <a href="#" onclick="logout()">Изход</a>
    </div>
</div>

<script>
    // Данни за симулация
    const users = {};
    const verificationCodes = {}; // Кодове за двустепенна автентикация
    let loggedInUser = null;
    let uploadedFile = null;

    // Показване на паролата
    function togglePassword(inputId) {
        const passwordField = document.getElementById(inputId);
        passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
    }

    // Превключване между секциите
    function showLogin() {
        document.getElementById('auth-container').style.display = 'block';
        document.getElementById('register-container').style.display = 'none';
        document.getElementById('forgot-password-container').style.display = 'none';
        document.getElementById('verification-container').style.display = 'none';
        document.getElementById('manager-container').style.display = 'none';

        // Автоматично попълване на имейл, ако е запазен в localStorage
        const savedEmail = localStorage.getItem('email');
        
        if (savedEmail) {
            document.getElementById('login-email').value = savedEmail;
        }
    }

    function showRegistration() {
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('register-container').style.display = 'block';
        document.getElementById('forgot-password-container').style.display = 'none';
        document.getElementById('verification-container').style.display = 'none';
        document.getElementById('manager-container').style.display = 'none';
    }

    function showForgotPassword() {
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('register-container').style.display = 'none';
        document.getElementById('forgot-password-container').style.display = 'block';
        document.getElementById('verification-container').style.display = 'none';
        document.getElementById('manager-container').style.display = 'none';
    }

    function showVerification() {
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('verification-container').style.display = 'block';
        document.getElementById('manager-container').style.display = 'none';
    }

    function showManager() {
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('register-container').style.display = 'none';
        document.getElementById('forgot-password-container').style.display = 'none';
        document.getElementById('verification-container').style.display = 'none';
        document.getElementById('manager-container').style.display = 'block';
    }

    // Регистрация
    function register() {
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;

        if (!/^[a-zA-Z0-9]+$/.test(password)) {
            alert('Паролата трябва да съдържа само английски букви и числа.');
            return;
        }

        if (users[email]) {
            alert('Този имейл вече е регистриран.');
            return;
        }

        users[email] = password;
        alert('Регистрацията е успешна! Моля, потвърдете вашия акаунт чрез 2FA.');

        loggedInUser = email;

        // Запазване на имейла в localStorage
        localStorage.setItem('email', email);

        // Генериране на случайния 2FA код
        const verificationCode = Math.floor(100000 + Math.random() * 900000); // 6 цифри
        verificationCodes[email] = verificationCode;

        alert(`Вашият 2FA код е: ${verificationCode}`);  // В реален проект ще изпращате имейл тук

        // Преминаване към екрана за въвеждане на код
        showVerification();
    }

    // Вход
    function login() {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        if (users[email] && users[email] === password) {
            loggedInUser = email;

            // Генериране на случайния 2FA код
            const verificationCode = Math.floor(100000 + Math.random() * 900000); // 6 цифри
            verificationCodes[email] = verificationCode;

            alert(`Вашият 2FA код е: ${verificationCode}`);  // В реален проект ще изпращате имейл тук

            // Преминаване към екрана за въвеждане на код
            showVerification();
        } else {
            alert('Грешен имейл или парола.');
        }
    }

    // Потвърждение на 2FA код
    function verifyCode() {
        const enteredCode = document.getElementById('verification-code').value;
        const expectedCode = verificationCodes[loggedInUser];

        if (enteredCode === expectedCode.toString()) {
            alert('Входът е успешен!');
            showManager();
        } else {
            alert('Невалиден код!');
        }
    }

    // Забравена парола
    function resetPassword() {
        const email = document.getElementById('forgot-email').value;

        if (!users[email]) {
            alert('Имейлът не е регистриран.');
            return;
        }

        const newPassword = prompt('Моля, въведете нова парола:');
        if (newPassword) {
            users[email] = newPassword;
            alert('Паролата е променена успешно!');
            showLogin();
        }
    }

    // Качване на файл
    function uploadFile() {
        const fileInput = document.getElementById('file-input');
        const file = fileInput.files[0];

        if (!file) {
            alert('Моля, изберете файл за качване.');
            return;
        }

        uploadedFile = file;
        const downloadLink = document.getElementById('download-link');
        downloadLink.href = URL.createObjectURL(file);
        downloadLink.download = file.name;

        document.getElementById('download-link-container').style.display = 'block';
        alert('Файлът беше качен успешно и е готов за изтегляне!');
    }

    // Изход
    function logout() {
        loggedInUser = null;
        localStorage.removeItem('email');
        alert('Излязохте успешно.');
        showLogin();
    }

    // Инициализация
    showLogin();
</script>

</body>
</html>
