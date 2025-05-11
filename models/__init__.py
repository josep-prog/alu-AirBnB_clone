# models/__init__.py
from models.engine.file_storage import FileStorage

# This needs to be after the import to avoid circular dependency
storage = FileStorage()
storage.reload()
