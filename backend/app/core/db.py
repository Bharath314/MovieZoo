from sqlalchemy.engine.base import Engine
from sqlmodel import Session, SQLModel, create_engine, select

from app.core.config import settings
from app.core.security import get_password_hash
from app.models import User, UserCreate

# TODO: move to config
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args: dict[str, bool] = {"check_same_thread": False}
engine: Engine = create_engine(sqlite_url, connect_args=connect_args)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def init_db():
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == settings.FIRST_SUPERUSER)
        ).first()
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = create_user(session=session, user_create=user_in)
