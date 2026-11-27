from fastapi import UploadFile, HTTPException, status


class MediaValidator:

    MAX_FILES = 5

    MAX_FILE_SIZE = 5 * 1024 * 1024

    ALLOWED_SIGNATURES = {
        "image/jpeg": ([b"\xff\xd8\xff"], ".jpg"),
        "image/png": ([b"\x89PNG\r\n\x1a\n"], ".png"),
        "image/webp": ([b"RIFF"], ".webp"),
        "application/pdf": ([b"%PDF-"], ".pdf"),
    }

    @classmethod
    def validate_file(cls, file: UploadFile) -> dict:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is required"
            )

        # Get file size
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{file.filename} is empty",
            )

        if size > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail=f"File size it too large",
            )

        # Read actual file signature
        signature = file.file.read(12)
        file.file.seek(0)

        detected_type = None
        extension = None

        for mime, (signatures, ext) in cls.ALLOWED_SIGNATURES.items():
            if any(signature.startswith(s) for s in signatures):
                detected_type = mime
                extension = ext
                break

        if detected_type is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file content: {file.filename}",
            )

        return {
            "file": file,
            "mime_type": detected_type,
            "extension": extension,
            "size": size,
        }

    @classmethod
    def validate_files(cls, files: list[UploadFile]) -> list[dict]:

        if not files:
            raise HTTPException(status_code=400, detail="At least one file is required")

        if len(files) > cls.MAX_FILES:
            raise HTTPException(
                status_code=400, detail=f"Maximum {cls.MAX_FILES} files allowed"
            )

        validated = []

        for file in files:
            get_validated = cls.validate_file(file=file)

            validated.append(get_validated)

        return validated
