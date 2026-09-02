import os
import tempfile
import unittest
from unittest.mock import patch

from src.s3 import s3_crud


class DummyUploadedFile:
    def __init__(self, filename):
        self.filename = filename
        self.saved_path = None
        self._data = b"test-data"

    def save(self, destination):
        self.saved_path = destination
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb") as f:
            f.write(self._data)

    def seek(self, offset):
        return None


class S3UploadSecureFilenameTest(unittest.TestCase):
    def test_upload_sanitizes_user_supplied_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bucket_name = "uploads"
            storage_path = os.path.join(tmpdir, bucket_name)
            uploaded = DummyUploadedFile("../../../../tmp/evil.txt")

            with patch.object(s3_crud, "STORAGE_MODE", "local"), patch.object(s3_crud, "LOCAL_STORAGE_PATH", tmpdir):
                ops = s3_crud.S3_OPERATIONS(bucket_name)
                result = ops.Upload(uploaded, uploaded, False)

            self.assertEqual(result, "OK")
            expected_path = os.path.join(storage_path, "evil.txt")
            self.assertTrue(os.path.exists(expected_path))
            self.assertFalse(os.path.exists(os.path.join(tmpdir, "evil.txt")))


if __name__ == "__main__":
    unittest.main()
