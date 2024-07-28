
from app.services.s3 import upload_file_object_to_s3
from app.utils import generateUniqueId
from fastapi import APIRouter, File, UploadFile, HTTPException
import pandas as pd
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

router = APIRouter()

@router.post("/upload/parquet",tags=["Train Data"])
async def upload_parquet(userColumnName:str,itemColumnName:str,file: UploadFile = File(...)):
    if not file.filename.endswith('.parquet'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a '.parquet' file.")

    try:
        df = pd.read_parquet(file.file)

        # Check for required columns
        required_columns = {userColumnName,itemColumnName}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail=f"Missing required columns. Required columns are: {required_columns}")
        
        uniqueId=generateUniqueId()
       
        object_key = f"train-data/{uniqueId}/{file.filename}"


        upload_file_object_to_s3(file, object_key)
        
    
        return {"message": "File uploaded successfully to S3","data_id":f"{uniqueId}"}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except PartialCredentialsError:
        raise HTTPException(status_code=500, detail="Incomplete AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
