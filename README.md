# Система расшифровки и коррекции аудио и видео

Данный проект представляет собой приложение для автоматической расшифровки и коррекции аудио и видеофайлов на основе модели OpenAI Whisper. Пользовательский интерфейс создан с использованием фреймворка Streamlit.

Cсылка: https://audio-transcription-correction-cayencxpbneepkl2gqxzyi.streamlit.app/
## Возможности

- **Автоматическая расшифровка:** преобразование аудио и видеофайлов в текст.
- **Коррекция:** исправление ошибок в полученных транскрипциях с помощью Яндекс.Спеллера.
- **Поддержка различных форматов:** работает с файлами форматов MP3, MP4, WAV и других.

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Kyamal02/audio-transcription-correction.git
   cd audio-transcription-correction
2. Создайте и активируйте виртуальное окружение:

   - **Для Linux/macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - **Для Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. Запустите приложение:
   ```bash
   streamlit run app.py
