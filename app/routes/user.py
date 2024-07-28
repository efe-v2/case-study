from app.services.postgre import get_latest_train_model
from app.utils import load_model_and_data
from fastapi import APIRouter

router = APIRouter()

@router.get("/user/exist", tags=["User"])
def userExist(user_id: str,model_id:str=None):

    if model_id:
        _, user_dict, _, _ = load_model_and_data(model_id)

    else:
        latest_completed_model = get_latest_train_model()

        model_id = latest_completed_model.id if latest_completed_model else "default"

        _, user_dict, _, _ = load_model_and_data(model_id)


    if user_id in user_dict:

        return True
    else:
        return False


    

