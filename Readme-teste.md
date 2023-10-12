# Meu Projeto Kafka

Este projeto demonstra o uso do Apache Kafka para enviar dados de uma API web para um tópico Kafka e, em seguida, consumir esses dados em tempo real.

## Requisitos

- Docker
- Python 3
- Bibliotecas Python listadas em `requirements.txt`

1. Configure o ambiente Kafka:
docker-compose up -d

2. Em um terminal, vá para o diretório app e inicie a API:
cd app
python3 api.py

3. Em outro terminal, vá para o diretório raiz do projeto e execute o script main.py:
python3 main.py

Isso iniciará a API na porta 5000.

# Uso
Acesse a API em http://127.0.0.1:5000/, onde você verá os produtos sendo enviados em tempo real.
