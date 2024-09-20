import streamlit as st
import whisper
import requests
import re


# Функция для загрузки модели Whisper
def load_whisper_model():
    return whisper.load_model("small")


# Функция для обработки аудио или видео файла и транскрибирования текста
def transcribe_file(file_path):
    whisper_model = load_whisper_model()
    result = whisper_model.transcribe(file_path, language='ru')
    transcription = result['text']
    return transcription


# Функция для проверки орфографии с помощью Яндекс.Спеллера
def correct_text_with_yandex_speller(text):
    url = 'https://speller.yandex.net/services/spellservice.json/checkText'
    words = text.split()  # Разделяем текст на слова
    corrected_words = []

    # Проверяем каждое слово
    for word in words:
        params = {'text': word}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            corrections = response.json()
            corrected_word = word  # По умолчанию слово не исправляется
            if corrections:
                corrected_word = corrections[0]['s'][0]  # Берем первое исправление
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)  # Если ошибка, добавляем оригинальное слово

    return ' '.join(corrected_words)  # Собираем исправленный текст обратно в строку


# Удаление лишних пробелов и переносов строк
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Заменить множественные пробелы на один
    return text.strip()  # Удалить пробелы в начале и в конце


# Интерфейс Streamlit
st.title("Whisper и Яндекс.Спеллер интеграция")

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите аудио или видео файл", type=["mp3", "mp4", "wav"])

if uploaded_file is not None:
    # Сохранение файла
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Транскрипция файла
    st.text("Транскрибирование файла...")
    transcription = transcribe_file(uploaded_file.name)

    # Очистка текста
    cleaned_transcription = clean_text(transcription)

    # Проверка орфографии
    st.text("Исправление орфографии...")
    corrected_transcription = correct_text_with_yandex_speller(cleaned_transcription)

    # Вывод результатов
    st.subheader("Транскрибированный и исправленный текст:")
    st.text(corrected_transcription)

    # Скачивание исправленного текста
    st.download_button("Скачать текст", corrected_transcription, file_name="transcription_corrected.txt")
