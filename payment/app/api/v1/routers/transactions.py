
from fastapi import APIRouter
from app.database import db


router = APIRouter()


@router.get("/history/",
            # response_model=List[schemas.User],
            )
def history(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Retrieve users.
    """
    print('asdf')
    # return users
