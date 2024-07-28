
from typing import List

import pandas as pd
from app.services.model import trainModel
from app.services.postgre import get_completed_train_models, get_model_train, insert_model_train
from app.utils import download_file_from_s3, removeFile
from fastapi import  BackgroundTasks, HTTPException,APIRouter
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class UserInteraction(BaseModel):
    date: str
    user_id: str
    session_id: str
    page_type: str
    item_id: str
    category: List[str]
    product_price: float
    old_product_price: float


class TrainedModelResponse(BaseModel):
    id:str
    status: str
    description: Optional[str] = None
    created_at: datetime
    train_auc: Optional[float] = None
    test_auc: Optional[float] = None
    train_precision: Optional[float] = None
    test_precision: Optional[float] = None
    train_recall: Optional[float] = None
    test_recall: Optional[float] = None
    

@router.post("/model/train", tags=["Model"])
async def train_model(data_id: str, background_tasks: BackgroundTasks):
    try:
    
        modelId = insert_model_train()

        background_tasks.add_task(start_training, data_id,modelId)


        return {'status': 'Model created successfully','model_id':modelId}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    

@router.get("/model/train/status", tags=["Model"])
async def model_status(model_id: str):
    try:
    
       model = get_model_train(model_id=model_id)
        
       return {'status': {model.status},'version_id':{model.id},'description':{model.description}}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

def start_training(data_id: str,model_id: str):
    try:
        file_path = f'train-data/{data_id}/train.parquet'
        local_path = f'data/{data_id}/train.parquet'

        download_file_from_s3(file_path,local_path)
        df = pd.read_parquet(local_path)
     
        trainModel(df,model_id)
        
        removeFile(local_path)
    except Exception as e:
        print(f"An error occurred: {e}")    


@router.get("/model/train/completed", tags=["Model"])
async def trained_models(page:int=1,page_size:int=10):
    try:
    
       models = get_completed_train_models(page,page_size)
        
       return [TrainedModelResponse(
            id=model.id,
            status=model.status,
            description=model.description,
            created_at=model.created_at,
            train_auc=model.train_auc,
            test_auc=model.test_auc,
            train_precision=model.train_precision,
            test_precision=model.test_precision,
            train_recall=model.train_recall,
            test_recall=model.test_recall
        ) for model in models]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/model", tags=["Model"])
async def trained_models(model_id:str):
    try:
    
       model = get_model_train(model_id=model_id)
        
       return TrainedModelResponse(
            id=model.id,
            status=model.status,
            description=model.description,
            created_at=model.created_at,
            train_auc=model.train_auc,
            test_auc=model.test_auc,
            train_precision=model.train_precision,
            test_precision=model.test_precision,
            train_recall=model.train_recall,
            test_recall=model.test_recall
        ) 
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
