import numpy as np

def recommend_existing_user(model, user_id, user_mapping, item_mapping, item_features, top_n=10):
    user_idx = user_mapping.get(user_id, None)
    if user_idx is None:
        raise ValueError(f"User ID {user_id} not found in user mapping.")
    
    item_indices = np.arange(len(item_mapping))
    scores = model.predict(user_idx, item_indices, item_features=item_features)
    top_items = np.argsort(-scores)[:top_n]
    
    reverse_item_mapping = {v: k for k, v in item_mapping.items()}
    recommendations = [reverse_item_mapping[item] for item in top_items]
    return recommendations
