# Teste de estágio - Reis Softwares

<p align="center">
  <a href="#-tecnologia-escolhida">Tecnologia escolhida</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-tecnologias-utilizadas">Tecnologias Utilizadas</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-setup-do-projeto-e-como-executar">Setup do projeto e como executar</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#como-testar">Como testar</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#decisões-técnicas">Decisões técnicas</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#melhorias-futuras">Melhorias futuras</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#vídeo-funcional-da-aplicação">Vídeo funcional da aplicação</a>
</p>

## 💻 Tecnologia escolhida

Optei por utilizar Python com FastAPI neste desafio técnico. Python é a stack que eu mais domino em programação, e
pensando no desafio e o proposto utilizei FastAPI pois é simples, versátil e de rápida aplicação sem perca de qualidade.
Fora essas questões, ele facilita muito a criação de endpoints, a validação automática de dados com Pydantic.

## 🚀 Tecnologias Utilizadas

Essas são as tecnologias que utilizei para construir o projeto:

- Python - Linguagem usada
- FastAPI - Framework para desenvolver a API
- Swagger - Documentação da API
- SQLAlchemy - ORM para manipulação de banco
- Pydantic - Validação de dados
- Alembic - Criar e gerenciar migration
- Python-Jose - Gerenciador de autenticação JWT
- Pwdlib - Biblioteca para gerar Hash de senhas (argon2)
- Docker - Criado o container onde o banco de dados e o backend está hospedado
- Postgres - Modelo do banco de dados

## 💻 Setup do projeto e como executar

1. Baixe este repositório e com seu terminal entre no diretório

```
git clone SSH( git@github.com:pedrohenriquelimasilva/reis_software.git ) or HTTP( https://github.com/pedrohenriquelimasilva/reis_software.git )
```

2. Entre na pasta que foi clonada

```
cd folder
```

3. Verifique se o python 3.12 ou acima estão em sua máquina

```
python --version
```

3. Se não estiver, instale o python

```
https://www.python.org/downloads/
```

4. Instale o pipx e o poetry e instâncie o poetry nos path pelo terminal

```
pip install pipx

pipx install poetry

pipx ensurepath
```

5. Vá até o local onde o repositório clonado está, instale as dependências e inicie o ambiente

```
cd folder

poetry install

poetry env activate
```

6. Vá até ao arquivo .env e coloque suas variaveis de ambiente (exemplo tá no .env.example)

7. Crie seus containers com o Docker

```
docker-compose up --build
```

8. Após criar o container, crie as tabelas no banco

```
alembic upgrade head
```

9. Inicie a aplicação

```
task run
```

## Como testar

Apos executar os passo de setup e execução, basta entrar na URL e ter acesso a todas as rotas

<a  href="http://localhost:8000/docs">
http://localhost:8000/docs
</a>

## Decisões técnicas

Visão padrões de projetos limpos e de fácil manutenção, utilizei POO junto a Strategy para elaboração de todo o código. Penso, sinceramente, que um código que outro programador não consegue entender, é um código que não serve para aplicação (com exceção de plataformas legadas kkk). Tendo em vista esse ponto e perante meu convívio e domínio da tecnologia, essa é a escolha mais sensata para a proposta do teste

## Melhorias futuras

Tem algumas possíveis melhorias que logo, logo vou aplicar nessa aplicação

1. Rota para filtragem com base em intervalos de data de finalização.

2. Penso em colocar um serviço de alerta por email para notificar o usuário que a task tá pendente ou que tá chegando perto de sua data final.

3. Layout front-end para ter um interatividade com o usuário.

## Vídeo funcional da aplicação

Vídeo com toda a execução e teste da aplicação

[![Assista ao vídeo](https://img.youtube.com/vi/3E4n0s-O2K8/0.jpg)](https://youtu.be/3E4n0s-O2K8)
