import minio

MINIO_CONF = {
    'endpoint': 'minio1:9000',
    'access_key': 'hkust',
    'secret_key': 'csit6000o',
    'secure': False
}
INPUT_BUCKET = 'markdown'

# 单例模式
class MINIO_CLIENT(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
            cls.client = minio.Minio(**MINIO_CONF)
        return cls._instance

    def __init__(self):
        pass

    def up_data_minio(self, bucket: str, up_object_name, filepath):
        found = self.client.bucket_exists(bucket)
        if not found:
            self.client.make_bucket(bucket)
        self.client.fput_object(bucket, up_object_name, filepath)

    def load_data_minio(self, load_object):
        if not self.client.bucket_exists(INPUT_BUCKET):
            return None
        data = self.client.get_object(INPUT_BUCKET, load_object)
        return str(data.data, "utf-8")