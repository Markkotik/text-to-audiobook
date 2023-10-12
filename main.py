import os
import textract
from gtts import gTTS


class AudioBookCreator:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        """Извлекает текст из файла, используя библиотеку textract."""
        text = textract.process(self.file_path, language='rus')
        return text.decode('utf-8')

    @staticmethod
    def split_text(text, max_len=5000):
        """Разбивает текст на части, каждая из которых не превышает max_len символов."""
        parts = []
        while text:
            if len(text) <= max_len:
                parts.append(text)
                break
            else:
                part = text[:max_len]
                last_period = part.rfind('.')
                if last_period == -1:
                    last_period = max_len
                parts.append(text[:last_period + 1])
                text = text[last_period + 1:]
        return parts

    def create_audio_book(self, output_file='audiobook.mp3', lang='ru'):
        """Преобразует текст из файла в аудиофайл."""
        text = self.extract_text()

        if not text.strip():
            raise ValueError("Документ не содержит текста.")

        parts = self.split_text(text)
        audio_files = []

        for i, part in enumerate(parts):
            tts = gTTS(text=part, lang=lang, slow=False)
            part_file = f"part_{i+1}.mp3"
            tts.save(part_file)
            audio_files.append(part_file)

        self.combine_audio_files(audio_files, output_file)

        for file in audio_files:
            os.remove(file)  # Удаляем части после объединения

        print(f"Аудиокнига сохранена как '{output_file}'.")

    @staticmethod
    def combine_audio_files(audio_files, output_file):
        """Объединяет несколько аудиофайлов в один."""
        import pydub

        combined = pydub.AudioSegment.empty()
        for file in audio_files:
            audio = pydub.AudioSegment.from_mp3(file)
            combined += audio

        combined.export(output_file, format='mp3')


if __name__ == "__main__":
    # Замените 'your_file_path' реальным путем к вашему файлу.
    creator = AudioBookCreator('zdarova priyatel.txt')

    # Вы можете изменить имя выходного файла и язык (по умолчанию 'ru' - русский)
    creator.create_audio_book(output_file="output_audiobook.mp3", lang="ru")
