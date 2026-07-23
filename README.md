# 🔎 JobFinder — Vagas de Tecnologia no Brasil

<p align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

</p>

<p align="center">

<a href="https://job-finder-seven-rust.vercel.app/" target="_blank">
<img src="https://img.shields.io/badge/🌐%20Acessar%20JobFinder-22C55E?style=for-the-badge" />
</a>

<a href="https://www.linkedin.com/in/rodrigo-mayer-alves-a9255675" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>

</p>

---

# 📖 Sobre o projeto

JobFinder é uma plataforma de busca de vagas de tecnologia no Brasil. O sistema coleta anúncios de múltiplas fontes (Adzuna, Remotive, Findwork) e os organiza em um banco de dados unificado, permitindo buscas com filtros por tecnologia, modalidade, nível, localização e faixa salarial.

O projeto foi desenvolvido para praticar desenvolvimento full stack com Python assíncrono, FastAPI, React moderno e deploy em múltiplos ambientes.

---

# ✨ Funcionalidades

- Busca de vagas com filtros avançados
- Filtros por tecnologia, cidade, estado, modalidade, nível e tipo de contrato
- Sincronização automática com APIs de vagas (Adzuna, Remotive)
- Listagem paginada com ordenação
- Interface responsiva e moderna
- Documentação OpenAPI/Swagger integrada

---

# 🚀 Tecnologias utilizadas

## Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 (assíncrono)
- Pydantic v2
- APScheduler
- HTTPX
- SQLite / PostgreSQL
- Loguru

## Frontend

- React 19
- TypeScript 6
- Vite 8
- Tailwind CSS 4
- TanStack React Query
- Axios
- React Router 7

## Ferramentas

- Git & GitHub
- VS Code
- Docker

## Deploy

- Backend: PythonAnywhere
- Frontend: Vercel

---

# 📁 Estrutura do projeto

```text
JobFinder/
│
├── backend/
│   ├── app/
│   │   ├── api/          # Rotas e schemas da API
│   │   ├── core/         # Config, database, logging
│   │   ├── data/         # Dados auxiliares (cidades brasileiras)
│   │   ├── domain/       # Enums e regras de negócio
│   │   ├── models/       # Modelos SQLAlchemy
│   │   ├── repositories/ # Camada de acesso a dados
│   │   ├── scheduler/    # Sincronização agendada
│   │   ├── schemas/      # Schemas Pydantic
│   │   ├── scrapers/     # Integração com APIs externas
│   │   ├── services/     # Lógica de negócio
│   │   └── main.py       # Entry point FastAPI
│   ├── wsgi.py           # Adaptador ASGI -> WSGI
│   ├── render.yaml
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/   # Componentes reutilizáveis
│   │   ├── pages/        # Páginas da aplicação
│   │   ├── hooks/        # Custom hooks (TanStack Query)
│   │   ├── services/     # Chamadas à API
│   │   ├── types/        # Tipos TypeScript
│   │   └── context/
│   ├── vercel.json       # Proxy /api -> PythonAnywhere
│   └── vite.config.ts
│
├── docker-compose.yml
└── README.md
```

---

# 💻 Como executar

## Backend

Clone o repositório

```bash
git clone https://github.com/RodrigoMA21/JobFinder.git
cd JobFinder/backend
```

Crie e ative o virtualenv

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Copie e configure o arquivo .env

```bash
cp .env.example .env
```

Inicie o servidor

```bash
uvicorn app.main:app --reload
```

Acesse a documentação em http://localhost:8000/docs

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse em http://localhost:5173

---

# 📦 Build para produção

```bash
cd frontend
npm run build
```

O build será gerado na pasta `dist/`.

---

# 🔮 Próximas melhorias

- [ ] Autenticação de usuários
- [ ] Salvamento de vagas favoritas
- [ ] Alertas de novas vagas por e-mail
- [ ] Integração com LinkedIn e Indeed
- [ ] Modo escuro
- [ ] Testes automatizados (pytest + vitest)
- [ ] Pipeline CI/CD com GitHub Actions

---

# 👨‍💻 Autor

**Rodrigo Mayer Alves**

🌐 Portfólio  
https://rodrigomayer.vercel.app/

💼 LinkedIn  
https://www.linkedin.com/in/rodrigo-mayer-alves-a9255675

🐙 GitHub  
https://github.com/RodrigoMA21

---

# 📄 Licença

Este projeto está licenciado sob a licença MIT.
