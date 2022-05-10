from markdown import markdown
from minio_client import MINIO_CLIENT
import os

def convert(url):
    client = MINIO_CLIENT()
    data = client.load_data_minio(url)
    ret = markdown(data)

    filename = url.split('.')[-2]+'.html'
    file = open(filename,'w')
    file.write(str(ret))
    file.close()
    client.up_data_minio('html', filename, filename)
    os.remove(filename)