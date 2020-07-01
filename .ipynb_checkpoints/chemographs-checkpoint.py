import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime as dt


## TODO: create numpy array over full period date range with same value as wqo in df, use that series instead of df wqo

plt.rcParams.update({'figure.max_open_warning': 0})


path = os.getcwd()
data = os.path.join(path,'data','wqtimeseries.csv')

## Create subdirectories with jupyter magic commands, great temporary solution but terrible for long term use. 
## TODO: script this in python or powershell
# !mkdir -p output_selectkeywells/tds/{santaana,kennedy,casitas,miramonte,robles}
# !mkdir -p output_selectkeywells/chloride/{santaana,kennedy,casitas,miramonte,robles}
# !mkdir -p output_selectkeywells/sulfate/{santaana,kennedy,casitas,miramonte,robles}
# !mkdir -p output_selectkeywells/boron/{santaana,kennedy,casitas,miramonte,robles}
# !mkdir -p output_selectkeywells/nitrate_as_no3/{santaana,kennedy,casitas,miramonte,robles}
# !mkdir -p output_selectkeywells/nitrate_as_n/{santaana,kennedy,casitas,miramonte,robles}


df = pd.read_csv(data)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df = df.loc['1977-01-01':'2020-01-01']
wells = df['well'].unique().tolist()
chems = df['chem'].unique().tolist()
areas = df['area'].unique().tolist()
df.head()


def get_pivot_table():
    table = pd.pivot_table(df,values='find',index='well',columns='chem', aggfunc='count')
    table.to_csv('pivot_table.csv')


def plt_chemographs(threshold):
    for chem in chems:
        for well in wells:
            for area in areas:
                df_well = df.loc[(df['well'] == well) & (df['chem'] == chem) & (df['area'] == area)]
                df_well = df_well.loc[~df_well.index.duplicated()]
                if not df_well.empty:
                    if df_well['find'].dropna().count() >= threshold:
                        fig,ax=plt.subplots()
                        line1, = ax.plot(df_well.index, df_well['find'], dashes=[4,2],
                                         marker='o', markersize=5,label='meas. conc.',
                                         c='limegreen',linewidth=2.5)
                        line2, = ax.plot(df_well.index, df_well['wqo'], label = 'wqo',c='red')
                        ax.legend(loc='center left')
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        ax.spines['bottom'].set_visible(False)
                        ax.spines['left'].set_visible(False)
                        ax.set_xlim([datetime.date(1977, 1, 1), datetime.date(2020, 1, 1)])
                        ax.set_ylabel('Concentration (mg/l)')
                        plt.title(f"{well}")
                        axes = plt.gca()
                        axes.yaxis.grid()
                        fig.savefig(f"./output_selectkeywells/{chem}/{area}/{well}.png")


get_pivot_table()
plt_chemographs(4)