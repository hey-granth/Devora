# Devora

AI-native Developer Relations Intelligence Platform that unifies telemetry, documentation, GitHub activity, and community signals into a single intelligence layer.

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- Neon PostgreSQL account
- Redis (local Docker or Upstash)

### Setup

1. **Clone and setup workspace**
   ```bash
   git clone <repository>
   cd devora
   ```

2. **Install dependencies**
   ```bash
   # Python dependencies
   uv sync
   
   # JavaScript dependencies  
   bun install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database and API keys
   
   cp apps/web/.env.local.example apps/web/.env.local
   ```

4. **Start development environment**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

5. **Run database migrations**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Development

### Running services individually
```bash
# API server
cd apps/api && uv run uvicorn src.main:app --reload

# Web frontend  
cd apps/web && bun run dev

# Background worker
cd apps/api && uv run python -m rq worker --url $REDIS_URL devora
```

### Code quality
```bash
# Python linting and formatting
ruff check .
ruff format .

# TypeScript type checking
bun run typecheck

# Run tests
pytest
```

## Architecture

- **Backend**: FastAPI + SQLModel + PostgreSQL + Redis + RQ
- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui
- **AI Layer**: LiteLLM for unified LLM access
- **Infrastructure**: Docker Compose, GitHub Actions

## License

AGPL v3 - see LICENSE file for details.
