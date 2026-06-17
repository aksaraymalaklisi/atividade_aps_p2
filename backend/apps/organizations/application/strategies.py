from abc import ABC, abstractmethod
from typing import BinaryIO


class DocumentUploadStrategy(ABC):
    """
    Strategy interface for uploading organization verification documents.
    """

    @abstractmethod
    def upload(self, file_name: str, file_content: BinaryIO) -> str:
        """
        Uploads the file and returns the public URL or path.
        """
        pass


class LocalFileSystemStorageStrategy(DocumentUploadStrategy):
    """
    Concrete strategy that saves the document to the local file system.
    """

    def upload(self, file_name: str, file_content: BinaryIO) -> str:
        # Em um cenário real, você salvaria no disco.
        # Aqui, vamos simular retornando uma URL local.
        import os

        from django.conf import settings

        # Certifique-se de que o diretório MEDIA_ROOT exista
        upload_dir = os.path.join(settings.MEDIA_ROOT, "organizations")
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(file_content.read())

        return f"{settings.MEDIA_URL}organizations/{file_name}"


class MockStorageStrategy(DocumentUploadStrategy):
    """
    Concrete strategy used for testing. Does not write to disk.
    """

    def upload(self, file_name: str, file_content: BinaryIO) -> str:
        return f"http://mock-storage.com/documents/{file_name}"
