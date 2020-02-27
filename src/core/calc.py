import os
import pandas as pd
from utils.utils import pop_row, get_by_hour
import settings
SOURCE = os.getcwd() + '\\assets\\result.xlsx'

def calc():
    #////////////////////////////////////////////////////////
    #   data setup
    #////////////////////////////////////////////////////////
    df = pd.read_excel(SOURCE, index_col=0)
    df = pop_row(df,17)
    #////////////////////////////////////////////////////////
    #   range of hours
    #////////////////////////////////////////////////////////
    h_start = 9
    h_end = 16
    vs = []
    std = []
    q ={}
    for i in range(h_start,h_end + 1):
        tmp = get_by_hour(df, i)
        tmp = tmp.reset_index(drop = True)
        avg = tmp["volume"].mean()
        sd = tmp["volume"].std()
        tmp["std"] = sd
        tmp["avg"] = avg
        vs.append(avg)
        std.append(sd)
        q[str(i)] = avg

        # tmp.to_excel(settings.OUTDIR+str(i)+"-"+str(i+1)+".xlsx") 


    #output table
    final_frame = pd.DataFrame({'Hours': ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8'],'average': vs, 'std': std})
    final_frame.to_excel(settings.OUTDIR+"data.xlsx")

    #build plot
    frame = pd.DataFrame({'Hours': ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8'], 'average': vs}) 
    plt = frame.plot.bar(x='Hours', y='average', rot=0)
    fig = plt.get_figure()
    fig.savefig(settings.OUTDIR+"plot.png")
    print(df[['date']].drop_duplicates())

