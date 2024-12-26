import pytest
from unittest.mock import patch
from main import clean_text, correct_text_with_yandex_speller, transcribe_file


# Тест для функции очистки текста
def test_clean_text():
    text = "  Это   тест   "
    cleaned = clean_text(text)
    assert cleaned == "Это тест", "Текст должен быть очищен от лишних пробелов"


# Тест для проверки орфографии
@patch('requests.get')  # Исправлено на прямое обращение к requests
def test_correct_text_with_yandex_speller(mock_get):
    # Имитация ответа от Яндекс.Спеллера
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'s': ['тест']}]

    original_text = "тестт"
    corrected_text = correct_text_with_yandex_speller(original_text)

    assert corrected_text == "тест", "Текст должен быть исправлен"


@patch('whisper.load_model') 
def test_transcribe_file(mock_load_model):
    mock_model = mock_load_model.return_value
    mock_model.transcribe.return_value = {'text': 'Это транскрибированный текст'}

    result = transcribe_file("test.mp3")
    assert result == "Это транскрибированный текст", "Функция должна возвращать правильный транскрибированный текст"


import os

from main import transcribe_file, clean_text, correct_text_with_yandex_speller

def test_integration_whisper_and_speller():
    """
    Интеграционный тест, который проверяет всю цепочку:
    1) Транскрибирование аудио через Whisper (реальная модель).
    2) Очистку текста.
    3) Исправление орфографии через реальное API Яндекс.Спеллера.
    И затем сравнивает результат с эталонным текстовым файлом.
    """

    test_file_path = "tests/data/test_audio.mp3"
    expected_file_path = "tests/data/expected_output.txt"

    # Проверяем, что оба файла существуют
    assert os.path.exists(test_file_path), (
        f"Тестовый аудиофайл не найден: {test_file_path}"
    )
    assert os.path.exists(expected_file_path), (
        f"Файл с ожидаемым результатом не найден: {expected_file_path}"
    )

    # 1) Транскрибируем аудио (Whisper)
    transcription = transcribe_file(test_file_path)
    assert transcription, "Транскрибированный текст пуст — возможно сбой в Whisper."

    # 2) Очищаем текст
    cleaned = clean_text(transcription)
    assert cleaned, "После очистки текст почему-то стал пустым."

    # 3) Исправляем орфографию через Яндекс.Спеллер
    corrected = correct_text_with_yandex_speller(cleaned)
    assert corrected, "После исправления орфографии текст оказался пустым."

    # 4) Считываем содержимое эталонного файла
    with open(expected_file_path, "r", encoding="utf-8") as f:
        expected_text = f.read().strip()

    # 5) Сравниваем с ожидаемым результатом
    # Можно убрать .strip() у corrected, если важны пробелы/переносы строк.
    assert corrected.strip() == expected_text, (
        "Итоговый текст не совпадает с ожидаемым результатом."
    )

    print("Интеграционный тест прошёл успешно и совпал с эталонным текстом!")





