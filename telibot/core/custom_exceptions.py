class TooLongException(Exception):
    def __init__(self, duration, max_duration: int = 6):
        self.duration = duration
        self.max_duration = max_duration
        super().__init__(f"A duração do audio: {duration} excede o máximo pertimido de: {max_duration} segundos.")


class NotAudioException(Exception):
    def __init__(self, content_type: str):
        self.content_type = content_type
        super().__init__(f"Arquivo não é um áudio. Tipo: {content_type}")


class FileSizeException(Exception):
    def __init__(self, size: int, max_size: int):
        self.size = size
        self.max_size = max_size
        super().__init__(f"O arquivo tem tamanho: {size} bytes, excede o máximo permitido de: {max_size} bytes.")
