# Reminder Free Epic Games

Você nunca mais vai perder um jogo grátis da Epic Games.

Este projeto foi criado com o objetivo de automatizar o monitoramento das promoções semanais da Epic Games Store e enviar notificações diretamente para um canal no Telegram.

## ✨ Motivação

A Epic Games disponibiliza jogos gratuitos toda semana, mas nem sempre lembramos de verificar.

A ideia foi criar um sistema totalmente automatizado, que:

- Consulta a API oficial da Epic Games
- Filtra apenas jogos realmente gratuitos no momento
- Traduz automaticamente a descrição para português
- Envia imagem, descrição e link direto para resgate
- Executa tudo na nuvem, sem depender de um computador ligado

## 🎮 Conceito

O projeto funciona como um radar automatizado.

Uma vez configurado, ele roda sozinho através do GitHub Actions, verificando semanalmente se existem jogos gratuitos ativos e enviando as informações diretamente para um canal no Telegram.

Sem intervenção manual.
Sem necessidade de servidor próprio.
Sem custos.

## 🛠️ Tecnologias Utilizadas

- Python 3.13
- Requests (requisições HTTP)
- API pública da Epic Games Store
- Telegram Bot API
- GitHub Actions (execução em nuvem)
- Google Translate (tradução automática)

## 🧠 O que este projeto demonstra

- Consumo de APIs públicas
- Manipulação e filtragem de JSON complexo
- Integração com APIs externas (Telegram)
- Automação em nuvem com CI/CD
- Uso seguro de Secrets no GitHub
- Estruturação de scripts Python voltados para automação

## 🚀 Como executar localmente

1. Clone o repositório
2. Instale as dependências:

pip install requests

3. Configure as variáveis de ambiente:

TELEGRAM_TOKEN
CHAT_ID

4. Execute:

python main.py

## ☁️ Execução automática

O projeto utiliza GitHub Actions para rodar automaticamente toda quinta-feira.

Isso significa que o bot continua funcionando mesmo com o computador desligado.

## 🔐 Segurança

Os tokens e IDs sensíveis não ficam expostos no código.
Eles são armazenados como GitHub Secrets.

## 📌 Estado atual do projeto

Atualmente o projeto encontra-se funcional e estável, enviando semanalmente:

- Nome do jogo
- Descrição traduzida
- Imagem oficial
- Link direto para a página da Epic Games

Melhorias futuras podem incluir:

- Sistema anti-repetição de jogos
- Log estruturado
- Histórico de promoções
- Deploy alternativo em servidor próprio

## 🤝 Feedback e contribuições

Sugestões, melhorias e ideias são sempre bem-vindas.

Este projeto também representa uma evolução prática no estudo de automação, Python e integração entre APIs.
