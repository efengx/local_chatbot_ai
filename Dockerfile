FROM python:3.9

# 
WORKDIR /code

# 将当前目录copy到容器中的/code/目录下
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# 
CMD ["uvicorn", "main_restapi:app", "--host", "0.0.0.0", "--port", "80"]