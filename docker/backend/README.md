## 环境

在当前目录下添加.env文件，内容为：

```bash
PORT=3000
DATABASE_PATH=./flowise
APIKEY_PATH=./flowise
SECRETKEY_PATH=./flowise
LOG_PATH=./flowise/logs

# NUMBER_OF_PROXIES= 1

# DATABASE_TYPE=postgres
# DATABASE_PORT=""
# DATABASE_HOST=""
# DATABASE_NAME="flowise"
# DATABASE_USER=""
# DATABASE_PASSWORD=""

# FLOWISE_USERNAME=user
# FLOWISE_PASSWORD=1234
# FLOWISE_SECRETKEY_OVERWRITE=myencryptionkey
# DEBUG=true
# LOG_LEVEL=debug (error | warn | info | verbose | debug)
# TOOL_FUNCTION_BUILTIN_DEP=crypto,fs
# TOOL_FUNCTION_EXTERNAL_DEP=moment,lodash

# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
# LANGCHAIN_API_KEY=your_api_key
# LANGCHAIN_PROJECT=your_project
```