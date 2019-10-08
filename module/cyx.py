# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 10:53:44 2019

@author: 9F3566
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:21:01 2019

@author: cyx
"""

import pandas as pd
import numpy as np


import pandas as pd
import numpy as np


def divide(a, b):
    if  b !=0:
        return a / b
    else:
        return 0
    
def divide_log(a, b):
    if  a != 0 and b !=0:
        return np.log(a / b)
    else:
        return 0  

def cut_type(df, col_var, target, cuttype, n):
    
    if cuttype == 'qc':
    
        data_cut = pd.qcut(df[col_var], q = n, duplicates="drop", retbins=True)
        data_group = data_cut[0].rename(col_var)
        data_tmp = pd.concat([data_group, df[target]], axis=1)   
        df_count = pd.crosstab(data_tmp[col_var], data_tmp[target]).reset_index()
        df_col = df_count[col_var].sort_values(na_position='first').reset_index(drop = True)
        df_result = pd.concat([df_col, df_count.drop([col_var], axis = 1)], axis = 1)
            
    elif cuttype == 'c':
        
        data_cut = pd.cut(df[col_var], n, duplicates="drop", retbins=True)
        data_group = data_cut[0].rename(col_var)
        data_tmp = pd.concat([data_group, df[target]], axis=1)   
        df_count = pd.crosstab(data_tmp[col_var], data_tmp[target]).reset_index()
        df_col = df_count[col_var].sort_values(na_position='first').reset_index(drop = True)
        df_result = pd.concat([df_col, df_count.drop([col_var], axis = 1)], axis = 1)
            
    elif cuttype == 'g':
        
        df.fillna('null',inplace = True)
        df_result = pd.crosstab(df[col_var], df[target]).reset_index()
            
    else:
        df_result = pd.DataFrame()
        print('cut_type error {}'.format(df, col_var, cuttype))
        
    return df_result



def bin_cut(df, target, col_var, cuttype, n):
    df = df[[target, col_var]]
    
    df_cut = cut_type(df, col_var, target, cuttype, n)
    df_cut.rename(columns = {col_var : 'group', 
                             list(df_cut.columns)[1] : 'Good', 
                             list(df_cut.columns)[2] : 'Bad'}, inplace = True)
    
    df_cut['Total'] = df_cut['Good'] + df_cut['Bad']
    df_cut['col'] = col_var 
    
    return df_cut

def bin_groupby(df, target, col_var):
    df_data = df[[ col_var, target]]
    
    df_count = df_data.groupby([col_var]).count().reset_index()
    df_count.rename(columns = {col_var : 'group', 
                             list(df_count.columns)[1] : 'Total'}, inplace = True)
    df_count['col'] = col_var
    
    return df_count

def calculate(df, calculate_list):
    
    df['BadRatio'] = df['Bad'] / df['Total']
    
    df['T_pcnt'] = df['Total'] / df['Total'].sum()
    df['G_pcnt'] = df['Good'] / df['Good'].sum()
    df['B_pcnt'] = df['Bad'] / df['Bad'].sum()
    
    df['GoodCumRate'] = df['Good'].cumsum() / df['Good'].sum()
    df['BadCumRate'] = df['Bad'].cumsum() / df['Bad'].sum()
    df['TotalCumRate'] = df['Total'].cumsum() / df['Total'].sum()
    
    df['ks'] = df['GoodCumRate'] - df['BadCumRate']
    df['ks_max'] = abs(df['ks'].max())

    df["woe"] = df.apply(lambda x: divide_log(x["G_pcnt"], x["B_pcnt"]) , axis=1)
    df["iv_inc"] = df["woe"] * (df["G_pcnt"] - df["B_pcnt"]) 
    df["ivcum"] = df["iv_inc"].cumsum()  
    df['iv'] = df['ivcum'].max()
    
    basic = ['col', 'group', 'Good', 'Bad', 'Total']
    iv = ['G_pcnt', 'B_pcnt', 'woe', 'iv_inc', 'iv']
    ks = ['GoodCumRate', 'BadCumRate', 'ks', 'ks_max']
    
    if calculate_list == 'iv':
        calculate_list = basic + iv
        df = df.loc[:,calculate_list] 
    
    elif calculate_list == 'ks':
        calculate_list = basic + ks
        df = df.loc[:,calculate_list] 
    
    elif calculate_list != False:
        calculate_list =  basic + calculate_list
        df = df.loc[:,calculate_list]
    
    return df
    
'''
datatype : False, dataint, datafloat
cuttype : g, qc, c
n: 20
calculate_list: False
     1. basic = ['group', 'Good', 'Bad', 'Total', 'col']
     2. indicator_list = ['BadRatio', 'T_pcnt', 'G_pcnt','B_pcnt', 'GoodCumRate', 'BadCumRate', 'TotalCumRate', 
     'ks', 'ks_max', 'woe', 'iv_inc', 'iv']
     3. iv, ks
'''

def bin_detail(df, target, col_var, cuttype, n, calculate_list):
    
    df = bin_cut(df, target, col_var, cuttype, n)
    
    df_indi = calculate(df,calculate_list)

    return df_indi

def bin_main(df, target, n, calculate_list):
    result = pd.DataFrame()
    col_list = []
    for col_var in list(df.columns):
        lenth = len(df[col_var].dropna().drop_duplicates())
        if lenth > n:
            try:
                df_result = bin_detail(df, target, col_var, 'qc', n, calculate_list )
                result = pd.concat([result, df_result])
            except:
                df_result = bin_detail(df, target, col_var, 'g', n, calculate_list)
                result = pd.concat([result, df_result])
        elif lenth < 2:
            col_list.append(col_var)
            col_list.append(lenth)
        else :
            try:
                df_result = bin_detail(df, target, col_var, 'g', n, calculate_list)
                result = pd.concat([result, df_result])
            except:
                col_list.append(col_var)
                col_list.append('false')
    return result

# 改变数据类型
def fill_null(df):
    if df is None:
        df = np.NaN
    elif df == 'null':
        df = np.NaN
    return df

def type_change(df):
    for col_var in list(df.columns):
        df[col_var] = df[col_var].apply(fill_null) 
        try:
            df[col_var] = pd.to_numeric(df[col_var])
        except:
            pass
    return df



    #b = result(df, target, col_var, datatype = 'dataint', cuttype = 'c', n = 10, calculate_list = 'ks')
    #a = bin_groupby(df, target, col_var)
import sklearn as sk 

def KS(clf, dx, dy):
    fpr, tpr, thresholds = sk.metrics.roc_curve(np.array(dy), clf.predict_proba(dx)[:,1])
    return "{:.4f}".format(max(tpr - fpr))

def auc(clf, dx, dy):
    return "{:.4f}".format(sk.metrics.roc_auc_score(np.array(dy), clf.predict_proba(dx)[:,1]))

def model_ev(clf, df, dx_feacolname, df_result, loan_month, bad_, l = 2):
    month_set = sorted(set(df[loan_month]))
    for i in month_set:
        dxy_tmp = df[df[loan_month] == i]
        dx_tmp = dxy_tmp[dx_feacolname]
        dy_tmp = dxy_tmp[bad_]
        df_result.loc[l,:] = ['%s_data' %i, KS(clf,dx_tmp,dy_tmp),auc(clf,dx_tmp,dy_tmp)]
        l = l+1
    return df_result

def func_corr(cols, result_base):
    iv_col = cols
    k = 0
    while k < len(iv_col): 
        j = iv_col[k]
        m = k + 1
        for n in iv_col[k + 1 : ]:
            corr_col = abs(result_base[j].corr(result_base[n]))
            if corr_col >= 0.5:
                del iv_col[m]
            else:
                m += 1
        k += 1
        print(iv_col)
    return iv_col

def jiexi(a):
    import json
    tmp = pd.DataFrame()
    i = 0
    for j in a['features']:
        try:
            c = pd.DataFrame(json.loads(j),index = [i])
            tmp = pd.concat([tmp,c])
        except:
            print(i)
        i += 1
    tmp_result = pd.concat([a[['order_no','score']].reset_index(), tmp], axis = 1)
    
    return tmp_result


    
def tree_to_rulescode(clf, dx_names, fc_file_name = False):
    n_nodes = clf.tree_.node_count
    children_left = clf.tree_.children_left.tolist()
    children_right = clf.tree_.children_right.tolist()
    feature = clf.tree_.feature.tolist()
    threshold = clf.tree_.threshold.tolist()
    
    node_depth = np.zeros(shape = n_nodes, dtype = np.int64)
    is_leaves = np.zeros(shape = n_nodes, dtype = bool)
    stack = [(0, -1)]
    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1
        
        if (children_left[node_id] != children_right[node_id]):
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True
    
    node_depth = node_depth.tolist()
    leaves = []
    for i in range(n_nodes):
        if children_left[i] == children_right[i]:
            leaves.append(i)
    
    node_lists, node_num = [], []
    for i in leaves:
        node_num.append(i)
        node_list = []
        
        for depth in range(node_depth[i], 0, -1):
            dth = depth - 1
            depth_list = []
            
            for index, ndt in enumerate(node_depth):
                if (ndt == dth) & (index < i):
                    depth_list.append(index)
            n = depth_list[-1]
            
            if i in children_left:
                node_list.insert(0, " %s <= %s and" % (dx_names[feature[n]],
                                                       threshold[n]))
            else:
                node_list.insert(0, " %s > %s and" % (dx_names[feature[n]],
                                                      threshold[n]))
                
            i = n
            w_node = "".join(node_list)
        node_lists.append(w_node[:-4])
    
    noderule = pd.DataFrame({'node': node_num, 'rule': node_lists})
    
    if fc_file_name == False:
        pass
    else:
        with open(fc_file_name, 'w') as f:
            for i, j in zip(node_num, node_lists):
                print(str(i) + " " + j, file = f)
            
    return noderule

    
