from app.services.postgre import get_latest_train_model
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..utils import  load_model_and_data
from ..services.recommend import recomment_to_user

router = APIRouter()

latest_completed_model = get_latest_train_model()

model_id = latest_completed_model.id if latest_completed_model else "default"

load_model_and_data(model_id)
class RecommendationRequest(BaseModel):
    user_id: str

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[str]
    known_items: List[str]

@router.get("/recommend/latest", response_model=RecommendationResponse,tags=["Recommendation"])
def recommend(user_id: str,n_recommendation:int=10,threshold:int=0):

    latest_completed_model = get_latest_train_model()

    model_id = latest_completed_model.id if latest_completed_model else "default"

    model, user_dict, items_dict, interactions = load_model_and_data(model_id)

    try:
        rec_list = recomment_to_user(model = model, 
                            interactions = interactions, 
                            user_id = user_id, 
                            user_dict = user_dict,
                            item_dict = items_dict, 
                            threshold = 0,
                            number_rec_items = n_recommendation,
                            show = False)
        
        return RecommendationResponse(user_id=user_id, 
                                      recommendations=rec_list["recommendations"],
                                      known_items=rec_list["known_items"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recommend/model", response_model=RecommendationResponse,tags=["Recommendation"])
def recommend(user_id: str,n_recommendation:int=10,threshold:int=0,model_id:str=None):

    if model_id:
        model, user_dict, items_dict, interactions = load_model_and_data(model_id)
    else:
         model, user_dict, items_dict, interactions = load_model_and_data("default")

    try:
        rec_list = recomment_to_user(model = model, 
                            interactions = interactions, 
                            user_id = user_id, 
                            user_dict = user_dict,
                            item_dict = items_dict, 
                            threshold = threshold,
                            number_rec_items = n_recommendation,
                            show = False)
        
        return RecommendationResponse(user_id=user_id, 
                                      recommendations=rec_list["recommendations"],
                                      known_items=rec_list["known_items"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

