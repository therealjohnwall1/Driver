import torch
import torch.nn as nn
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import torch.nn.functional as F
import os

        
class Nmodel(nn.Module):
    def __init__(self, features,hidden1,hidden2,labels):
        super().__init__()
        self.l1 = nn.Linear(features,hidden1)
        self.l2 = nn.Linear(hidden1,hidden2)
        self.l3 = nn.Linear(hidden2,labels)
    
    def forward(self,x):
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = self.l3(x)
        return x
    
      #saving weights of model
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


# class XG_model():
#     def __init__(self):
#         self.xgb = GradientBoostingClassifier()