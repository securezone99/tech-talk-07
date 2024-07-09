# AI-Assistants for Meetup Demo

### 1. Create a virtual environment

```shell
sudo apt-get install libpq-dev
sudo apt install python3.12-venv
sudo apt-get install python3.12-dev

python3.12 -m venv x_venv
source x_venv/bin/activate
cp .envExample .env
pip install -r meetup_assistants/requirements.txt
cd meetup_assistants/app
```

### Update all Keys in .env

### start locally

```shell
python -B -m uvicorn main:app --reload --log-level info
```

# Build and Push Image to Dockerhub (Free of Charge for one Private account)
```shell
sudo docker build -t xxx/xxx:1.1.1.1 .
sudo docker push xxx/xxx:1.1.1.1
```

