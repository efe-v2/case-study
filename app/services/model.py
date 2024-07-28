import os
import sys
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from app.services.postgre import update_model_train
from app.services.s3 import upload_to_s3
from app.utils import savePickle
from lightfm import LightFM
from lightfm import LightFM, cross_validation

import ast
import logging

from lightfm.evaluation import auc_score, precision_at_k, recall_at_k

import pandas as pd
import numpy as np

from fastapi import HTTPException
from scipy import sparse
from enum import Enum

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# class ModelStatus(Enum):
#     STARTED = 'Started'
#     COMPLETED = 'Completed'
#     ONGOING = 'Ongoing'
#     ERROR = 'Error'

def convert_itemId_to_list(item):
    if isinstance(item, str):
        try:
            # Eğer item bir liste olarak parse edilebiliyorsa parse et
            return ast.literal_eval(item)
        except:
            # Değilse, item string olarak kalır
            return item
    return item

def explode_items(df):
    df_exploded = df[df['pageType'] == 'cart'].explode('itemId')
    df_non_cart = df[df['pageType'] != 'cart']
    df_combined = pd.concat([df_exploded, df_non_cart], ignore_index=True)
    df_combined['itemId'] = df_combined['itemId'].astype(str)
    return df_combined


def processData(df):

    df["itemId"] = df["itemId"].apply(lambda item : np.nan if  item=='[]' else item )

    df = df.dropna(subset=['itemId'])

    df.loc[:, 'itemId'] = df['itemId'].apply(convert_itemId_to_list)

    df = explode_items(df)

    df =df.groupby('itemId').filter(lambda x: len(x)>=50)

    df = df[df.groupby('userId').itemId.transform('nunique')>=1]

    return df


def preProcessing(df):

    print("preProcessing started")
    df_freq = df.groupby(['userId', 'itemId']).agg('size').reset_index().rename(columns={0:'freq'})[['userId', 'itemId', 'freq']].sort_values(['freq'], ascending=False)
    df_item = pd.DataFrame(df_freq["itemId"].unique())
    df_item = df_item.reset_index()
    df_item = df_item.rename(columns={'index':'item_id', 0:'itemId'})
    df_freq = pd.merge(df_freq, df_item, how='inner', on='itemId')


    print("preProcessing completed")

    return df_freq,df_item


def create_interaction_matrix(df, user_col, item_col, rating_col, norm=False, threshold=None):
    # Group by user and item
    grouped = df.groupby([user_col, item_col])[rating_col]
    
    # Sum the ratings
    summed = grouped.sum()
  
    # Unstack to create the matrix
    unstacked = summed.unstack()
    
    # Reset index
    reset = unstacked.reset_index()
   
    # Fill NaN values with 0
    filled = reset.fillna(0)
    
    # Set user_col as index
    interactions = filled.set_index(user_col)
    
    # Normalize if required
    if norm:
        interactions = interactions.applymap(lambda x: 1 if x > threshold else 0)
        print("\nNormalized Interaction Matrix:\n", interactions)

    
    return interactions


def create_user_dict(interactions):
    
    user_id = list(interactions.index)
    user_dict = {}
    counter = 0 
    for i in user_id:
        user_dict[i] = counter
        counter += 1
    return user_dict

def create_item_dict(df, id_col, name_col):
    
    item_dict = dict(zip(df[id_col], df[name_col]))
    return item_dict


def runMF(interactionMatrix, n_components=30, loss='warp', k=15, epoch=30,n_jobs = 4):
    
    model = LightFM(no_components= n_components, loss=loss,k=k)
    model.fit(interactionMatrix,epochs=epoch,num_threads = n_jobs)
    return model

def getModelMetrics(model, train, test):
    # Calculate AUC 
    train_auc = round(float(auc_score(model, train, num_threads=4).mean()), 4)
    print('Train AUC: %s' % train_auc)

    test_auc = round(float(auc_score(model, test, train_interactions=train, num_threads=4).mean()), 4)
    print('Test AUC: %s' % test_auc)

    # Calculate Precision 
    train_precision = round(float(precision_at_k(model, train, k=10).mean()), 4)
    test_precision = round(float(precision_at_k(model, test, k=10, train_interactions=train).mean()), 4)
    print('Train Precision: %.4f, Test Precision: %.4f' % (train_precision, test_precision))

    # Calculate Recall
    train_recall = round(float(recall_at_k(model, train, k=10).mean()), 4)
    test_recall = round(float(recall_at_k(model, test, k=10, train_interactions=train).mean()), 4)
    print('Train Recall: %.4f, Test Recall: %.4f' % (train_recall, test_recall))

    metrics = {
        "train_auc": train_auc,
        "test_auc": test_auc,
        "train_precision": train_precision,
        "test_precision": test_precision,
        "train_recall": train_recall,
        "test_recall": test_recall
    }

    return metrics


def trainModel(df,versionId):

    logging.info("Starting to train the model")

    update_model_train(versionId, status="ongoing", description="Model is currently being trained.")
    try:
       
        df = processData(df)

        df_freq ,df_item = preProcessing(df)

        interactions = create_interaction_matrix(df = df_freq, user_col = "userId", item_col = 'item_id', rating_col = 'freq', norm= False, threshold = None)
      
        user_dict = create_user_dict(interactions=interactions)
     
        items_dict = create_item_dict(df = df_item, id_col = 'item_id', name_col = 'itemId')
     
        x = sparse.csr_matrix(interactions.values)
        train, test = cross_validation.random_train_test_split(x, test_percentage=0.2, random_state=None)  
    
        train_data_model = runMF(interactionMatrix = train,
                 n_components = 100,
                 loss = 'warp',
                 k = 15,
                 epoch = 50,
                 n_jobs = 4)
        
        main_model = runMF(interactionMatrix = x,
                 n_components = 100,
                 loss = 'warp',
                 k = 15,
                 epoch = 50,
                 n_jobs = 4)
        
        logging.info("Model Training Completed")
    

        local_dir = f'model/{versionId}'
        os.makedirs(local_dir, exist_ok=True)

        model_path = f'{local_dir}/model.pkl'
        items_dict_path = f'{local_dir}/items_dict.pkl'
        user_dict_path = f'{local_dir}/user_dict.pkl'
        interactions_path = f'{local_dir}/interactions.pkl'

        savePickle(model_path, main_model)
        savePickle(items_dict_path, items_dict)
        savePickle(user_dict_path, user_dict)
        savePickle(interactions_path, interactions)

        logging.info("Starting to upload the model files")

        update_model_train(versionId, status="ongoing", description="Model files are uploading to S3, this could take 10 minutes.")

        upload_to_s3(model_path, f'model/{versionId}/model.pkl')
        upload_to_s3(items_dict_path, f'model/{versionId}/items_dict.pkl')
        upload_to_s3(user_dict_path, f'model/{versionId}/user_dict.pkl')
        upload_to_s3(interactions_path, f'model/{versionId}/interactions.pkl')

        logging.info("completed")

        update_model_train(versionId,status="ongoing",description = "The model metrics are calculating")

        metrics = getModelMetrics(train_data_model,train,test)

        update_model_train(versionId,status="completed",description = "",metrics=metrics)
 
        return versionId
    
    except Exception as e:
        update_model_train(versionId, status="error", description=f"error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

    