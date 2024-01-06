import torch
import torch.nn as nn
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import torch.nn.functional as F
import os


class Lmodel(nn.Module):
    def __init__(self,features,hidden,labels):
        super().__init__()
        self.l1 = nn.Linear(features,hidden)
        self.l2 = nn.Linear(hidden,labels)
    
    def forward(x):
        x = F.relu(self.l1(x))
        x = self.l2(x)
        return x
    
    #saving weights of model
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
    

    


class xgBoostModel():
    pass
