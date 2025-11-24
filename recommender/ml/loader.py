import os 
import pickle 
from functools import lru_cache

from django.conf import settings

@lru_cache(maxsize=1)
def load_bundle():
    pkl_path = os.path.join(settings.BASE_DIR,'recommender','ml','Crop_Recommendation_RF.pkl')

    with open(pkl_path,'rb') as f:
        b = pickle.load(f)

    assert "model" in b and "feature_cols" in b, "Invalid model bundle structure."
    return b

def prediction(feature_dict):

    bundle = load_bundle()

    model = bundle['model']
    feature_cols = bundle['feature_cols']

    X =  [[float(feature_dict[c]) for c in feature_cols]]
    pred = model.predict(X)[0]
    return pred 