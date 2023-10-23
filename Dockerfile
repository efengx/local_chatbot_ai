FROM huggingface/transformers-pytorch-cpu

# 
WORKDIR /code

# 将当前目录copy到容器中的/code/目录下
COPY ./ /code/

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
CMD ["uvicorn", "app.main_restapi:app", "--host", "0.0.0.0", "--port", "80"]
