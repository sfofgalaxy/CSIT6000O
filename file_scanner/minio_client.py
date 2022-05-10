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

    def list_files(self):
        found = self.client.bucket_exists(INPUT_BUCKET)
        if not found:
            self.client.make_bucket(INPUT_BUCKET)
        objects = self.client.list_objects(INPUT_BUCKET, prefix=None, recursive=True)
        return [str(obj.object_name.encode('utf-8'), "utf-8") for obj in objects]
