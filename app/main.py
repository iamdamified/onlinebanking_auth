from dotenv import load_dotenv
load_dotenv()   # MUST be before os.getenv is used
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.auth.routes import router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    #  Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (optional cleanup)

app = FastAPI(lifespan=lifespan)

# #For Dev
# origins = [
#     "http://localhost:3000",   # React / Next.js
#     "http://localhost:5173",   # Vite
#     "http://127.0.0.1:3000",
# ]

# #For Prod
# origins = [
#     "https://bankapp.com",
#     "https://www.bankapp.com",
# ]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix="/auth")
