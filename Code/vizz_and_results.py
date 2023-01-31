import numpy as np
import matplotlib.pyplot as plt
from get_metrics import average_error_percent
import pandas as pd
import networkx as nx


def get_graph(parameter,model):
    data = pd.read_csv(fr'..\Data\Results\results_{model}_{parameter}.csv')
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(model)
    axs[0, 0].plot(data.iloc[:,0],data.infec_list_FB,label = 'FB')
    axs[0, 0].plot(data.iloc[:,0],data.infec_list_BA,label = 'BA')
    axs[0,0].set_title('infect')
    axs[0,0].legend()
    axs[0, 1].plot(data.iloc[:,0],data.early_deg_FB,label = 'FB')
    axs[0, 1].plot(data.iloc[:,0],data.early_deg_BA,label = 'BA')
    axs[0,1].set_title('early deg')
    axs[1, 0].plot(data.iloc[:,0],data.speed_list_FB,label = 'FB')
    axs[1, 0].plot(data.iloc[:,0],data.speed_list_BA,label = 'BA')
    axs[1, 0].set_title('speed')
    axs[1, 0].set_xlabel(parameter)
    axs[1, 1].plot(0,0)
    axs[1, 1].set_xlabel(parameter)
    plt.show()

get_graph('decay','SI')

