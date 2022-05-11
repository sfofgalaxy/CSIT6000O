from pydoc import cli
from transformers import pipeline
from minio_client import MINIO_CLIENT
import os

# 单例模式
class MODEL(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
            cls.clf = pipeline("sentiment-analysis")
        return cls._instance

    def __init__(self):
        pass

    def predict(self, url):
        client = MINIO_CLIENT()
        text = client.load_data_minio(url)
        ret = self.clf(text)[0]

        filename = url.split(".")[-2] + ".txt"
        file = open(filename, "w")
        file.write(str(ret))
        file.close()
        client.up_data_minio("sentiment", filename, filename)
        os.remove(filename)
