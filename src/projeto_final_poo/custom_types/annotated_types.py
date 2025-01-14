from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from projeto_final_poo.db.connection import get_session

T_Session = Annotated[Session, Depends(get_session)]
