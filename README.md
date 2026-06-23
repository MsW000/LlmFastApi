# J.A.R.V.I.S v1.0

> **Just A Rather Very Intelligent System** – ваш личный AI-ассистент с открытым исходным кодом, интегрированный в операционную систему. Управляйте компьютером голосом, чатом, автоматизируйте задачи и расширяйте возможности с помощью модульной архитектуры.

---

## **О проекте**

**Jarvis** — это полноценная AI-платформа, сочетающая мощь large language models (LLM) с глубокой интеграцией в ОС (Windows/Linux). Проект разработан для замены стандартных интерфейсов взаимодействия с компьютером: вместо мыши и клавиатуры — **голос, текст и автоматизация**.

🔹 **Статус**: `Alpha (Active Development)`  
🔹 **Лицензия**: `MIT`  
🔹 **Язык**: `Python 3.10+`  
🔹 **Фреймворки**: `FastAPI`, `PyQt6`, `Ollama`, `PostgreSQL`, `pgvector`

---

## **Возможности**


| Категория                   | Функционал                                                                      |
| --------------------------- | ------------------------------------------------------------------------------- |
| ** Голосовой интерфейс** | STT (Speech-to-Text), TTS (Text-to-Speech), поддержка диалогов                  |
| ** Чат-интерфейс**        | Мультимодальные диалоги, контекстная память, поддержка инструментов             |
| ** AI-ядро**              | Интеграция с Ollama (локальные модели), кастомизация промптов                   |
| ** Автоматизация**       | Запуск приложений, выполнение команд, управление окнами                         |
| ** Знания**               | RAG (Retrieval-Augmented Generation), поиск по документам                       |
| ** Память**               | Краткосрочная (контекст чата), долговременная (факты о пользователе), векторная |
| ** Расширяемость**        | Поддержка внешних API, веб-поиск, кастомные инструменты                         |
| ** Наблюдаемость**        | Логирование, история действий, отладка                                          |


---

## **Архитектура**

```
JARVIS CORE SYSTEM
│
├── 1. API LAYER (FastAPI)
│   ├── Auth (JWT)
│   ├── Users / Roles
│   ├── Chat API
│   ├── Agent API
│   ├── Tools API
│   └── System Control API
│
├── 2. AI CORE (LLM ENGINE)
│   ├── Ollama Client
│   ├── Prompt Manager
│   ├── Conversation Memory
│   ├── Context Builder
│   └── Response Formatter
│
├── 3. AGENT SYSTEM (BRAIN)
│   ├── Intent Parser
│   ├── Planner (step generation)
│   ├── Executor (tool runner)
│   ├── Tool Router
│   └── Safety Guard
│
├── 4. TOOLS SYSTEM (ACTION LAYER)
│   ├── System Tools
│   │   ├── Open App
│   │   ├── Run Command
│   │   ├── File System Ops
│   │   └── Window Control
│   │
│   ├── Knowledge Tools
│   │   ├── Chat History Search
│   │   ├── Notes / Memory DB
│   │   └── Document Search (RAG)
│   │
│   ├── Data Tools
│   │   ├── PostgreSQL Query Tool
│   │   └── Analytics Tool
│   │
│   └── External Tools
│       ├── Web Search
│       ├── API Caller
│       └── Future Extensions
│
├── 5. KNOWLEDGE SYSTEM (RAG)
│   ├── Document Ingestion
│   ├── Chunking Engine
│   ├── Embeddings (Ollama)
│   ├── pgvector Storage
│   └── Semantic Search
│
├── 6. MEMORY SYSTEM
│   ├── Short-term Memory (chat context)
│   ├── Long-term Memory (user facts)
│   ├── Vector Memory (semantic recall)
│   └── Session Storage
│
├── 7. SYSTEM INTEGRATION
│   ├── OS Bridge Layer (Windows/Linux)
│   ├── Process Manager
│   ├── Hotkeys / Events
│   └── Background Service
│
├── 8. QT6 CLIENT (Frontend)
│   ├── Chat UI
│   ├── Voice Input (STT)
│   ├── Voice Output (TTS)
│   ├── Animated Avatar (GIF/Live2D later)
│   └── System Tray App
│
└── 9. OBSERVABILITY
    ├── Logging
    ├── Action History
    ├── Error Tracking
    └── Debug Panel
```

---

## **Установка**

### **Требования**

- Python **3.10+**
- PostgreSQL **14+** (с расширением `pgvector`)
- Ollama (для локальных LLM)
- Qt6 (для GUI)

### 🚀 **Быстрый старт**

1. **Клонируйте репозиторий:**
  ```bash
   git clone https://github.com/your-username/jarvis.git
   cd jarvis
  ```
2. **Создайте виртуальное окружение:**
  ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
  ```
3. **Установите зависимости:**
  ```bash
   pip install -r requirements.txt
  ```
4. **Настройте базу данных:**
  ```bash
   # Создайте базу данных PostgreSQL
   createdb jarvis_db

   # Установите расширение pgvector
   psql -d jarvis_db -c "CREATE EXTENSION vector;"

   # Примените миграции
   alembic upgrade head
  ```
5. **Настройте переменные окружения:**
  &nbsp;
6. **Запустите сервер:**
  ```bash
   uvicorn jarvis.api.main:app --reload
  ```
7. **Запустите сервер:**
  ```bash
   uvicorn jarvis.api.main:app --reload
  ```
8. **Запустите клиент:**
  ```bash
   python jarvis/client/main.py
  ```

---

## **Быстрый запуск (Альтернативный способ)**

Для тех, кто хочет запустить проект **с минимальными усилиями** (бекенд + фронтенд):

### **Бэкенд (FastAPI + Docker)**

```bash
# 1. Поднимите контейнеры (PostgreSQL, Redis и т.д.)
docker-compose up -d

# 2. Запустите FastAPI сервер
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Фронтенд (Qt6 Client)**

```bash
# Перейдите в папку с клиентом
cd .\app\Front\  # Windows
# или
cd ./app/Front/   # Linux/Mac

# Запустите клиент
python .\widget.py  # Windows
# или
python ./widget.py  # Linux/Mac
```

> ⚠️ **Примечание**: В будущем будет добавлена поддержка запуска **одной командой** через Docker для максимального удобства.

---

## **Использование**

### **GUI (Qt6 Client)**

- **Чат**: Введите текст или используйте голосовой ввод (кнопка микрофона).
- **Голос**: Нажмите `Ctrl+Space` для активации голосового ввода (настраивается в `config.json`).
- **Инструменты**: Используйте команды вида:
  - `Открой Chrome` → запустит приложение
  - `Выполни: ls -la` → выполнит команду в терминале
  - `Поиск в интернете: погода в Минске` → вернёт результаты поиска
  - `Найди в документах: что такое RAG` → выполнит семантический поиск

### **API (FastAPI)**

Документация API доступна по адресу:

```
http://localhost:8000/docs
```

**Примеры запросов:**

```bash
# Авторизация
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Отправка сообщения
curl -X POST "http://localhost:8000/chat/message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Привет, Jarvis!"}'

# Выполнение инструмента
curl -X POST "http://localhost:8000/tools/run" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "open_app", "args": {"app": "notepad"}}'
```

---

## 🛠️ **Конфигурация**

Файл конфигурации: `config.json`

```json
{
  "ollama": {
    "host": "http://localhost:11434",
    "default_model": "llama3:8b",
    "timeout": 120
  },
  "tts": {
    "engine": "pyttsx3",
    "voice": "ru_RU",
    "rate": 150
  },
  "stt": {
    "engine": "whisper",
    "model": "base"
  },
  "hotkeys": {
    "voice_input": "Ctrl+Space",
    "toggle_window": "Ctrl+Alt+J"
  },
  "memory": {
    "short_term_window": 10,
    "long_term_enabled": true
  }
}
```

---

## 📂 **Структура проекта**

```
jarvis/
├── api/                  # FastAPI сервер
│   ├── main.py           # Точка входа
│   ├── auth/             # Авторизация (JWT)
│   ├── chat/             # Чат API
│   ├── agents/           # Агенты и планировщики
│   ├── tools/            # Инструменты
│   └── system/           # Управление системой
│
├── core/                 # AI ядро
│   ├── llm/              # Работа с LLM (Ollama)
│   ├── memory/           # Система памяти
│   ├── rag/              # RAG (Retrieval-Augmented Generation)
│   └── context/          # Контекст и промпты
│
├── agents/               # Агентская система
│   ├── parser.py         # Парсер интентов
│   ├── planner.py        # Планировщик действий
│   ├── executor.py       # Исполнитель
│   └── safety.py         # Безопасность
│
├── tools/                # Инструменты
│   ├── system/           # Системные инструменты
│   ├── knowledge/        # Инструменты знаний
│   ├── data/             # Работа с данными
│   └── external/         # Внешние инструменты
│
├── client/               # Qt6 клиент
│   ├── ui/               # Интерфейс
│   ├── voice/            # Голосовой ввод/вывод
│   └── tray.py           # Системный трей
│
├── os_integration/       # Интеграция с ОС
│   ├── windows.py        # Windows-специфично
│   ├── linux.py          # Linux-специфично
│   └── bridge.py         # Унифицированный интерфейс
│
├── models/               # Модели базы данных
│   ├── user.py
│   ├── chat.py
│   ├── memory.py
│   └── documents.py
│
├── utils/                # Утилиты
│   ├── logger.py
│   ├── config.py
│   └── helpers.py
│
├── migrations/           # Миграции Alembic
├── tests/                # Тесты
├── requirements.txt
├── config.json
└── README.md
```

---

## **Расширение функционала**

### **Добавление нового инструмента**

1. Создайте файл в `jarvis/tools/[category]/`:
  ```python
   # jarvis/tools/system/my_tool.py
   from jarvis.core.tools.base import Tool

   class MyTool(Tool):
       name = "my_tool"
       description = "Описание инструмента"

       async def execute(self, **kwargs):
           # Ваша логика
           return {"result": "Успех!"}
  ```
2. Зарегистрируйте инструмент в `jarvis/tools/__init__.py`:
  ```python
   from .system.my_tool import MyTool

   TOOLS = {
       "my_tool": MyTool,
       # ... остальные инструменты
   }
  ```
3. Обновите контекст агента (опционально).

### **Добавление новой модели памяти**

1. Реализуйте класс в `jarvis/core/memory/`:
  ```python
   from jarvis.core.memory.base import MemoryBackend

   class MyMemory(MemoryBackend):
       async def store(self, key, value):
           # Сохранение
           pass

       async def retrieve(self, key):
           # Извлечение
           pass
  ```
2. Обновите конфигурацию в `config.json`.

---

## **Демонстрация работы**

> **GIF с демонстрацией интерфейса и функционала**  
> *(Замените на ваш GIF: `![Jarvis Demo](path/to/your/demo.gif)`)*

---

## 🤝 **Вклад в проект**

Приветствуются:

- ✅ **Баг-репорты** (открывайте issue)
- ✅ **Пулл-реквесты** (с описанием изменений)
- ✅ **Новые инструменты** (с документацией)
- ✅ **Улучшения документации**

### **Как внести вклад:**

1. Форкните репозиторий.
2. Создайте ветку (`git checkout -b feature/your-feature`).
3. Закоммитьте изменения (`git commit -m "Добавлен новый инструмент X"`).
4. Отправьте пулл-реквест.

---

## 📜 **Лицензия**

Этот проект распространяется под лицензией **MIT**. Подробности смотрите в файле [LICENSE](LICENSE).

---

## 🙏 **Благодарности**

- [Ollama](https://ollama.ai) – за локальные LLM
- [FastAPI](https://fastapi.tiangolo.com) – за удобный API
- [PyQt6](https://www.qt.io/qt-for-python) – за GUI
- [pgvector](https://github.com/pgvector/pgvector) – за векторный поиск
- Всем, кто вносит вклад в open-source сообщество!

---

## 📬 **Контакты**

- **Telegram**: [@ms_W_0001]([https://t.me/your_telegram](https://t.me/whoammi_01001000))
- **Email**: [inakentius@gmail.com](inakentius@gmail.com)
- **GitHub**: [github.com/MsW000/]([https://github.com/your-username/jarvis](https://github.com/MsW000))

---

> **"I am Jarvis. I am here to assist you."** 🤖
