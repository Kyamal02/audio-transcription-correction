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
    assert corrected.strip() == expected_text, (
        "Итоговый текст не совпадает с ожидаемым результатом."
    )

    print("Интеграционный тест прошёл успешно и совпал с эталонным текстом!")
