import os
import uuid
from abc import ABC, abstractmethod
from typing import BinaryIO

from django.conf import settings


class ImageUploadStrategy(ABC):
    """
    Strategy interface for uploading pet images.
    """

    @abstractmethod
    def upload(self, file_name: str, file_content: BinaryIO) -> str:
        pass


class LocalFileSystemImageStorageStrategy(ImageUploadStrategy):
    """
    Concrete strategy that saves the image to the local file system.
    """

    def upload(self, file_name: str, file_content: BinaryIO) -> str:
        upload_dir = os.path.join(settings.MEDIA_ROOT, "publications")
        os.makedirs(upload_dir, exist_ok=True)

        # Prevent file name collisions
        ext = os.path.splitext(file_name)[1]
        unique_name = f"{uuid.uuid4()}{ext}"

        file_path = os.path.join(upload_dir, unique_name)
        with open(file_path, "wb") as f:
            f.write(file_content.read())

        return f"{settings.MEDIA_URL}publications/{unique_name}"
