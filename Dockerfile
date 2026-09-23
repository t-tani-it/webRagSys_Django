# Dockerfile - APIイメージ定義（構成見本、起動対象外）.
#
# Why: 構成見本として残すため。
# What: 依存導入とrunserver起動を定義する。
# Assumption / Dependencies: Docker。
# I/O: 入力=ビルドコンテキスト、出力=イメージ。
# Caution: storage制約のため起動検証の対象外とする。
# Future Work: 本番用gunicorn化。
# Change Log: 初版作成.

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
