# 基于镜像基础
FROM python:3-alpine
# 设置代码文件夹工作目录 '/'
WORKDIR /
# 复制当前代码文件到容器中的'/'路径
ADD . /
# 安装所需的包
RUN pip install -r requirements.txt
# Run app.py when the container launches
CMD ["python", "workflow_opener.py"]