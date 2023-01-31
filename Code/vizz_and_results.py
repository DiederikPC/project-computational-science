import numpy as np
import matplotlib.pyplot as plt
from get_metrics import average_error_percent
import pandas as pd
import networkx as nx

# VISUALIZATION
def get_graph(parameter,model):
        
    raw_data = pd.read_csv(fr'..\Data\Results\results_{model}_{parameter}.csv')
    data_m = raw_data.groupby(by = parameter,as_index= False).mean()
    data_sd = raw_data.groupby(by = parameter,as_index= False).std()
    
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(f'model: {model}, parameter: {parameter}')

    first_axis = [0,0,1,1]
    second_axis = [0,1,0,1]
    for_fb = [1,3,5]
    for_ba = [2,4,6] 
    title = ['infect','early_deg','speed']   

    for i in range(3):

        fb_mean = np.array(data_m.iloc[:,for_fb[i]])
        fb_error = np.array(data_sd.iloc[:,for_fb[i]])
        ba_mean = np.array(data_m.iloc[:,for_ba[i]])
        ba_error = np.array(data_sd.iloc[:,for_ba[i]])

        axs[first_axis[i], second_axis[i]].plot(data_m.iloc[:,0],fb_mean,label = 'FB', color = 'blue')
        axs[first_axis[i], second_axis[i]].plot(data_m.iloc[:,0],ba_mean,label = 'BA',color = 'orange')
        axs[first_axis[i], second_axis[i]].fill_between(data_m.iloc[:,0],fb_mean - fb_error,fb_mean + fb_error, 
        alpha = 0.2, edgecolor = 'blue')
        axs[first_axis[i], second_axis[i]].fill_between(data_m.iloc[:,0],ba_mean - ba_error,ba_mean + ba_error, 
        alpha = 0.2, edgecolor = 'orange')
        axs[first_axis[i],second_axis[i]].set_title(title[i])

    plt.show()

# AVERAGE ERROR PERCENT
