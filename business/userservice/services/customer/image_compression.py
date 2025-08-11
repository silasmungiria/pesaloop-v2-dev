from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from PIL import Image
import io


class ImageCompressor:
    @staticmethod
    def compress(image, max_size=(1024, 1024), quality=85) -> bytes:
        """
        Compresses an uploaded image to reduce its size.

        Args:
            image (InMemoryUploadedFile | TemporaryUploadedFile): Uploaded image file.
            max_size (tuple): Maximum (width, height) for the thumbnail. Defaults to 1024x1024.
            quality (int): JPEG quality level (1–100). Defaults to 85.

        Returns:
            bytes: Compressed image content.
        """
        img = Image.open(image)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        byte_io = io.BytesIO()
        img.save(byte_io, format="JPEG", quality=quality)
        byte_io.seek(0)

        return byte_io.read()
