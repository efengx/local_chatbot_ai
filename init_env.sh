#!/bin/sh

# 安装 docker 20.10.24
# 方法一：使用ubuntu snap进行安装
# snap info docker                                                                                  # 查看docker
# sudo snap refresh                                                                                 # 刷新docker  
# sudo snap install docker                                                                          # 安装docker
# # docker 安装完成后，需要重启终端，否则会出现错误：permanently dropping privs did not work: File exists

# 方法二：使用apt-get进行安装
# 参考：https://docs.docker.com/engine/install/ubuntu/
# 移除可能冲突的包，会提示package not found
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
# 设置docker apt存储库
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
# 安装 docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin




# 安装 milvus v2.3.1 (分布式)
wget https://github.com/milvus-io/milvus/releases/download/v2.3.1/milvus-standalone-docker-compose.yml -O docker-compose.yml \
    && sudo docker compose up -d \
    && docker run -p 8000:3000 -e MILVUS_URL=192.168.0.107:19530 zilliz/attu:latest
# 安装 attu -e HOST_URL=http://39.104.228.125:8000
# 账号/密码：minioadmin/minioadmin
