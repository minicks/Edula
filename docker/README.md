# Build using Docker Compose

## Installing Docker

### Windows 10

#### Install WSL2

https://docs.microsoft.com/ko-kr/windows/wsl/install

Run command prompt in admin mode

```bash
wsl --install
```

and Reboot

#### Install Docker Desktop

https://www.docker.com/products/docker-desktop

### Linux (Ubuntu 20.04)

https://docs.docker.com/engine/install/ubuntu/

```bash
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

## Buliding

### dev mode

```bash
docker-compose -f docker-compose-local.yml build
docker-compose -f docker-compose-local.yml up
```

### production mode

```bash
docker-compose build
docker-compose up
```
