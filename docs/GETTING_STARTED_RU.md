# PinCode: запуск для разработки

## 1. Быстрый просмотр интерфейса
Установи Node.js LTS. В корне репозитория выполни:

```powershell
npm install
npm run dev
```

Открой адрес, который покажет Vite (обычно `http://127.0.0.1:1420`). Для Monaco Editor сейчас требуется подключение к интернету.

## 2. Сборка приложения Windows
Для сборки Tauri нужны Node.js LTS, Rust stable и инструменты сборки Visual Studio C++ для Windows.

```powershell
npm install
npm run tauri -- dev
```

Чтобы собрать установщик:

```powershell
npm run tauri -- build
```

Установщики появятся в `src-tauri/target/release/bundle/`. Также GitHub Actions автоматически собирает установщики после изменений основных файлов; смотри вкладку **Actions** в репозитории.

## 3. Облачный API
Создай MongoDB Atlas database и скопируй connection string. Затем в Render создай Web Service из этого репозитория, выбери blueprint `render.yaml` и задай секретные переменные из `backend/.env.example`.

**Важно:** cloud API пока использует временный заголовок идентификатора, а не подтверждённую авторизацию. Не храни в нём личные проекты до подключения сессии Пинийской Федерации. Подробности: [SECURITY.md](SECURITY.md).
