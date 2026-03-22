# Postboard — Backend API

A fully featured REST API built with FastAPI and PostgreSQL, powering the Postboard social media application. Handles authentication, post management, user accounts and voting.

🌐 **Live API:** [web-production-99e01.up.railway.app](https://web-production-99e01.up.railway.app)  
📄 **API Docs:** [web-production-99e01.up.railway.app/docs](https://web-production-99e01.up.railway.app/docs)  
🔗 **Frontend Repository:** [github.com/Stepha-Nek/postboard](https://github.com/Stepha-Nek/postboard)  
🌐 **Live App:** [postboard-sigma.vercel.app](https://postboard-sigma.vercel.app)

---

## Tech Stack

- **FastAPI** — Python web framework
- **PostgreSQL** — Relational database
- **SQLAlchemy** — ORM
- **Alembic** — Database migrations
- **Pydantic** — Data validation
- **JWT (JSON Web Tokens)** — Authentication
- **Bcrypt** — Password hashing
- **Railway** — Cloud deployment

---

## Features

- User registration and login with JWT authentication
- Create, read, update and delete posts
- Vote on posts (upvote and downvote)
- Search posts by title
- Pagination and limit/offset support
- Password hashing with bcrypt
- Protected endpoints — only post owners can edit or delete their posts
- Auto-generated interactive API docs via Swagger UI

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Login and receive JWT token |

### Users
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/users/` | ❌ | Register a new user |
| GET | `/users/{id}` | ❌ | Get user by ID |

### Posts
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/posts/` | ❌ | Get all posts with vote counts |
| POST | `/posts/` | ✅ | Create a new post |
| GET | `/posts/{id}` | ❌ | Get a specific post |
| PUT | `/posts/{id}` | ✅ | Update a post (owner only) |
| DELETE | `/posts/{id}` | ✅ | Delete a post (owner only) |

### Votes
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/vote/` | ✅ | Upvote or downvote a post |

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- pip

### Installation
```bash
# Clone the repository
git clone https://github.com/Stepha-Nek/fastapi-crud-app.git
cd fastapi-crud-app

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root folder:
```
database_hostname=localhost
database_port=5432
database_password=your_password
database_name=your_database_name
database_username=postgres
secret_key=your_secret_key
algorithm=HS256
access_token_expire_minutes=30
```

### Run Database Migrations
```bash
alembic upgrade head
```

### Run Locally
```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive API docs.

---

## Deployment

This backend is deployed on **Railway** with a managed PostgreSQL database. Environment variables are configured directly in the Railway dashboard.

---

## Project Structure
```
app/
├── routers/
│   ├── auth.py      # Login endpoint
│   ├── post.py      # Post CRUD endpoints
│   ├── user.py      # User endpoints
│   └── vote.py      # Vote endpoint
├── config.py        # Environment variable management
├── database.py      # Database connection and session
├── main.py          # FastAPI app and middleware
├── models.py        # SQLAlchemy database models
├── oauth2.py        # JWT token creation and verification
├── schemas.py       # Pydantic request/response schemas
└── utils.py         # Password hashing utilities
alembic/             # Database migration files
requirements.txt     # Python dependencies
```

---

## Author

**Nneka Oguh**  
[GitHub](https://github.com/Stepha-Nek) · [LinkedIn](https://linkedin.com/in/nneka-oguh)

---

## Related

- 🔗 [Postboard Frontend — React + Tailwind](https://github.com/Stepha-Nek/postboard)
- 🌐 [Live App](https://postboard-sigma.vercel.app)
