# Lyte API

A FastAPI-based task management application.

## Setup

### 1. Environment Variables

Create a `.env` file in the project root by copying the `.env.example` template:

```bash
cp .env.example .env
```

Then update the `.env` file with your actual database credentials:

```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/lyte_inspired_db
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at:

**[http://localhost:8000/docs](http://localhost:8000/docs)**

Alternative documentation (ReDoc) is available at:

**[http://localhost:8000/redoc](http://localhost:8000/redoc)**

## Features

- User management
- Task management with CRUD operations
- PostgreSQL database integration
- Automatic API documentation with Swagger/OpenAPI
