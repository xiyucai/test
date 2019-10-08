# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 15:41:47 2019

@author: 9F3566
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from sklearn import tree
from Display import conn as cn ,dt_tree as dt ,model as md# connect mysql and get table  into dataframe
from sklearn.model_selection import train_test_split
import os
from sklearn.externals.six import StringIO
import pydotplus
from sklearn2pmml import sklearn2pmml
import  sklearn2pmml as sp 

df = pd.read_csv(r"D:\Desktop\loan_1.csv")
df['bad'] = df['dpd5_cnt'].map(lambda x: 1 if x > 0 else 0)

corrs = ['GD_M_109', 'score_y', 'score_x', 'GD_M_126',
       'GD_F_14', 'GD_M_241']
dx = df[corrs] 
dx_feature_col=dx.columns.tolist()
dy = df['bad'] 

X_train, X_test, Y_train, Y_test = train_test_split(
    dx, dy, test_size=0.2, random_state=1)

clf = tree.DecisionTreeClassifier(
    criterion='gini',
    max_depth=4,
    min_samples_split=0.02,
    min_samples_leaf=0.02)
###

clf = clf.fit(X_train, Y_train)

path_v = os.getcwd()

dot_data = StringIO()
dx_names = dx.columns.values.tolist()
target_name = ['0', '1']
tree.export_graphviz(clf, out_file=dot_data, feature_names=dx_names,
                     class_names=target_name, filled=True, rounded=True,
                     node_ids=True,#proportion=True,
                     special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
graph.write_png(path_v + '\\'  + '_decision_tree_1.png')

with open(path_v + '\\'  + "_decision_tree.txt", 'w') as f:
    f = tree.export_graphviz(clf, feature_names=dx_names, out_file=f)
    
    
a = tree_to_rulescode(clf, dx_names, fc_file_name = False)
            
model_eval=pd.DataFrame(columns=['data_catogary','KS','AUC'])
model_eval.loc[0,:]=['train_DATA',KS(clf,X_train,Y_train),auc(clf,X_train,Y_train)]
model_eval.loc[1,:]=['test_DATA',KS(clf,X_test,Y_test),auc(clf,X_test,Y_test)]

model_eval=model_ev(clf=clf,
                       df=df,
                       dx_feacolname=dx_feature_col,
                       df_result=model_eval,
                       loan_month = 'type',
                       bad_ = 'bad')    


pipeline = sp.make_pmml_pipeline(clf, active_fields=dx_names, target_fields='is_bad')
pipeline.configure(node_id=True,winner_id=True,numberofFields=True) #添加pmml文件的node_id

pmml_path=path_v + '\\'  +'_model.pmml'
sklearn2pmml(pipeline,pmml_path,with_repr=True)
       