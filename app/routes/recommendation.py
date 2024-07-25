from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..utils import load_model, load_user_mapping, load_item_mapping, load_item_features
from ..model import recommend_existing_user

router = APIRouter()

model = load_model()
user_mapping = load_user_mapping()
item_mapping = load_item_mapping()
item_features = load_item_features()

class RecommendationRequest(BaseModel):
    user_id: str

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[str]

@router.get("/recommend", response_model=RecommendationResponse)
def recommend(user_id: str):
    try:
        recommendations = recommend_existing_user(model, user_id, user_mapping, item_mapping, item_features)
        return RecommendationResponse(user_id=user_id, recommendations=recommendations)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update-model")
def update_model(version_id: str):
    try:
        global model, user_mapping, item_mapping, item_features
        model = load_model('models/lightfm_model.pkl', version_id=version_id)
        user_mapping = load_user_mapping('models/user_mapping.pkl', version_id=version_id)
        item_mapping = load_item_mapping('models/item_mapping.pkl', version_id=version_id)
        item_features = load_item_features('models/item_features.pkl', version_id=version_id)
        return {"status": "Model updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
