import os
import pytest
import difflib
from main import transcribe_file, clean_text, correct_text_with_yandex_speller

def test_integration_whisper_and_speller():
    """
    Интеграционный тест, который проверяет всю цепочку:
    1) Транскрибирование аудио через Whisper (реальная модель).
    2) Очистку текста.
    3) Исправление орфографии через реальное API Яндекс.Спеллера.
    И затем сравнивает результат с эталонным текстовым файлом.
    """

    test_file_path = os.path.join("tests", "data", "test_audio.mp3")
    expected_file_path = os.path.join("tests", "data", "expected_output.txt")

    # Проверяем текущую рабочую директорию
    print("Текущая рабочая директория:", os.getcwd())
    print("Содержимое текущей директории:", os.listdir("."))
    print("Содержимое папки tests/data:", os.listdir("tests/data"))

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
    print("Транскрибированный текст:", transcription)

    # 2) Очищаем текст
    cleaned = clean_text(transcription)
    assert cleaned, "После очистки текст почему-то стал пустым."
    print("Очищенный текст:", cleaned)

    # 3) Исправляем орфографию через Яндекс.Спеллер
    corrected = correct_text_with_yandex_speller(cleaned)
    assert corrected, "После исправления орфографии текст оказался пустым."
    print("Исправленный текст:", corrected)

    # 4) Считываем содержимое эталонного файла
    with open(expected_file_path, "r", encoding="utf-8") as f:
        expected_text = f.read().strip()
    print("Ожидаемый текст:", expected_text)

    # 5) Сравниваем с ожидаемым результатом используя коэффициент похожести
    similarity = difflib.SequenceMatcher(None, corrected.strip(), expected_text).ratio()
    print(f"Коэффициент похожести: {similarity:.2f}")

    # Устанавливаем порог похожести
    assert similarity > 0.9, (
        f"Итоговый текст не совпадает с ожидаемым результатом. Коэффициент похожести: {similarity:.2f}"
    )

    print("Интеграционный тест прошёл успешно и совпал с эталонным текстом!")
