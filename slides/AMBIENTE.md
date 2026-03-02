# Ambiente Usado No Curso

# VS Code
Site: `https://code.visualstudio.com/download`

# Python 
- Version: 3.13.x
```bash
# Nesse laboratorio instalando usando o uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# teste
uv --version
# instala python
uv python install 3.13
``` 
# Node Js
- Version: 22 lts
```bash
# Nesse laboratorio instalei usando nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
# Resetar bashrc
source ~/.bashrc
# instalar node 
nvm install 22
``` 
# Nats Cli
- Version 0.3.1
```bash
# baixar
curl -LO https://github.com/nats-io/natscli/releases/download/v0.3.1/nats-0.3.1-amd64.deb 
# descompactar
sudo dpkg -i nats-0.3.1-amd64.deb 
# instalar
sudo apt-get -f install
# Validar
nats --version

```
https://github.com/nats-io/natscli/releases/tag/v0.3.1
# Docker

```bash
# instalar dependencias
sudo apt update
sudo apt install ca-certificates curl gnupg 

# adicionar chave gpg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# adicionar repositorio oficial
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# instalar engines
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# teste rapido
sudo docker run hello-world

# configurar grupo de permissao
sudo usermod -aG docker $USER
newgrp docker

# validar versoes
docker --version
docker compose version
``` 
