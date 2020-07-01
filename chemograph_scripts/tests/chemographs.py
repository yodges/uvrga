import pandas as pd
import matplotlib as plt
import os

plt.rcParams.update({'figure.max_open_warning': 0})

path = os.getcwd()
data = os.path.join(path,'data','wqtimeseries.csv')
out = os.path.join(path,'data','output')

df = pd.read_csv(data)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
wells = df['well'].drop_duplicates().tolist()
chems = df['chem'].unique().tolist()


def plot_chemographs():
    for chem in chems:
        for well in wells:
            df_well = df.loc[(df['well'] == well) & (df['chem'] == chem)]
            fig = df_well.plot(title=f"{well}: {chem}").get_figure()
            fig.savefig(f"./output/{chem}_{well}.png")


plot_chemographs()