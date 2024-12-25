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


