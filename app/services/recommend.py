import numpy as np
import pandas as pd

def recomment_to_user(model, interactions, user_id, user_dict, 
                      item_dict, threshold=0, number_rec_items=10, show=True):
  
    n_users, n_items = interactions.shape
    
    if user_id in user_dict:
        user_x = user_dict[user_id]
    
        # Predicts scores for all items for the given user using the trained model
        # np.arange(n_items) generates an array of item indices from 0 to n_items - 1.
        scores = pd.Series(model.predict(user_x, np.arange(n_items)))
    
        # interactions.columns contains the item IDs (or item indices) from the interaction matrix.
        #By setting scores.index = interactions.columns, we assign the item IDs as the index of the scores Series.
        #This means each score is now associated with the corresponding item ID.
        scores.index = interactions.columns
    
        # Sort scores from highest to lowest, then get the item IDs
        scores = list(pd.Series(scores.sort_values(ascending=False).index))

        # Get all interactions for the given user
        user_interactions = interactions.loc[user_id, :]

        # Filter out interactions which is ItemIds that are below the threshold
        interactions_above_threshold = user_interactions[user_interactions > threshold]

        # Get the item IDs for these interactions
        known_item_indices = interactions_above_threshold.index

        # Turn these item IDs into a Series
        known_item_series = pd.Series(known_item_indices)

        # Sort the item IDs from highest to lowest
        sorted_known_items = known_item_series.sort_values(ascending=False)

        # Convert the sorted item IDs to a list
        known_items = list(sorted_known_items)

        # Exclude Known Items from Recommendations:
        scores = [x for x in scores if x not in known_items]
        return_score_list = scores[0:number_rec_items]
        
    else:
        # For new users, recommend the most interacted items
        item_interaction_counts = interactions.sum(axis=0)
        most_interacted_items = item_interaction_counts.sort_values(ascending=False).index
        return_score_list = list(most_interacted_items[:number_rec_items])
        known_items = []
        
    
    # Handle missing keys in item_dict
    known_items = list(pd.Series(known_items).apply(lambda x: item_dict.get(x, 'Unknown Item')))
    scores = list(pd.Series(return_score_list).apply(lambda x: item_dict.get(x, 'Unknown Item')))
    
    if show:
        print("Known Interacted Items:")
        counter = 1
        for i in known_items:
            print(str(counter) + '- ' + i)
            counter += 1

        print("\nRecommended Items:")
        counter = 1
        for i in scores:
            print(str(counter) + '- ' + i)
            counter += 1
    
    return {"known_items":known_items,"recommendations":scores}
