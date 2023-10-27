FROM python:3.9

# 
WORKDIR /code

# 将当前目录copy到容器中的/code/目录下
COPY ./docker/frontend/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# 
CMD ["streamlit", "run", "main_web.py", "--server.port", "80"]
