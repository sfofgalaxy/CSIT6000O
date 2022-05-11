from flask import Flask, request, jsonify
from conversion import convert
from sentiment import MODEL

PORT = 60000

app = Flask(__name__)


@app.route("/")  # 代表首页
def index():  # 视图函数
    return


@app.route("/conversion", methods=["POST"])  # 支持get、post请求
def conversion():  # conversion
    url = request.form.get("url")  # args取get方式参数
    convert(url)
    return jsonify({"message": "success"})


@app.route("/sentiment", methods=["POST"])  # 支持get、post请求
def sentiment():  # sentiment
    url = request.form.get("url")  # args取get方式参数
    model = MODEL()
    model.predict(url)
    return jsonify({"message": "success"})


if __name__ == "__main__":
    # 0.0.0.0代表任何能代表这台机器的地址都可以访问
    app.run(host="0.0.0.0", port=PORT)
