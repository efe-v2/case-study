import pickle
import os
import pickle
import uuid

from app.services.s3 import download_file_from_s3


def load_pickle_file(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def load_file(local_path,s3_path):
    download_file_from_s3(s3_path, local_path)
    return load_pickle_file(local_path)

def openFile(filename):
    try:
        with open(filename, 'rb') as file:
            loadedFile = pickle.load(file)
        return loadedFile
    except Exception as e:
        print(f"An error occurred while loading the file {filename}: {e}")
        return None


def savePickle(path, file):
    try:
        with open(path, 'wb') as f:
            pickle.dump(file, f)
        return "Success"
    except Exception as e:
        return f"Failed: {e}"


def generateUniqueId():
    return str(uuid.uuid4())

def removeFile(local_path):

    if os.path.exists(local_path):
            os.remove(local_path)


def load_model_and_data(model_id):
   
    base_path = f'model/{model_id}'
     
    paths = {
        'model': f'{base_path}/model.pkl',
        'user_dict': f'{base_path}/user_dict.pkl',
        'items_dict': f'{base_path}/items_dict.pkl',
        'interactions': f'{base_path}/interactions.pkl'
    }

    loaded_data = {}

    for key, path in paths.items():
        if os.path.exists(path):
            loaded_data[key] = load_pickle_file(path)
        else:
            loaded_data[key] = load_file(path, path)  
    
    return (loaded_data['model'], loaded_data['user_dict'], loaded_data['items_dict'], loaded_data['interactions'])

