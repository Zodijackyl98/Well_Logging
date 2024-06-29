import lasio 
from pathlib import Path
import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px

las = lasio.read(r"/path/to/your/las/file/.las") #Path of your LAS file

parent_dir = r''
# directory = las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') # optional directory creator specifically for wells
directory = './wells'
path = os.path.join(parent_dir, directory)

try:
    os.mkdir(path)
except FileExistsError:
    print('Same folder is already exists')

[x for x in Path(parent_dir).iterdir() if str(x).split(sep = '\\')[-1] == directory]

df = las.df()

df['TIME'] = df['TIME'].apply(lambda x: str(int(x)).zfill(6)[:2]+ ':' + str(int(x)).zfill(6)[2:4] + ':' + str(int(x)).zfill(6)[4:]) 
df['DATE'] = df['DATE'].apply(lambda x: str(int(x))[:4] + '/'+  str(int(x))[4:6] + '/' + str(int(x))[6:])
df['N_TIME'] = df['DATE'] + '-' +  df['TIME']


time_format = "%Y/%m/%d-%H:%M:%S"
df['REAL_TIME'] = df['N_TIME'].apply(lambda x: datetime.strptime(x, time_format))
df.drop(('N_TIME'), axis = 1, inplace = True)

df['SECONDS'] = df.index.values

df_graphs = [['TOTACTIVEPITS','ACT_VOL'], ['PRESSURE_IN','FLOWPADDLE'], ['HOOK POS','WOB3']]

st_time = '2023-07-06 00:00:00'
ed_time = '2023-07-06 23:59:55'

start_time = datetime.strptime(st_time, "%Y-%m-%d %H:%M:%S")
end_time = datetime.strptime(ed_time, "%Y-%m-%d %H:%M:%S")

df_stats = df[(df['REAL_TIME'] >= start_time) & (df['REAL_TIME'] <= end_time)].aggregate(['min','max',np.median]) # std & mean removed because mostly they are meaningless
df_stats.to_csv(directory + '/' + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.txt', sep = '\t')

for i in df_graphs:

    interval = df[i[0]][(df['REAL_TIME'] >= start_time) & (df['REAL_TIME'] <= end_time)]#FIRST TO DRAW
    interval_ = df[i[1]][(df['REAL_TIME'] >= start_time) & (df['REAL_TIME'] <= end_time)]
    interval_time = df['REAL_TIME'][(df['REAL_TIME'] >= start_time) & (df['REAL_TIME'] <= end_time)]#INTERVAL TIME

    fig, ax1 = plt.subplots()
    ax2 = ax1.twiny()

    p1 = ax1.plot(interval, interval_time, linewidth = 0.5, label = interval.name)
    p2 = ax2.plot(interval_, interval_time, c = 'r', linewidth = 0.5, label = interval_.name)
    ax1.set_xlabel(interval.name + '(' + las.curves[interval.name]['unit'] + ')')
    ax2.set_xlabel(interval_.name + '(' + las.curves[interval_.name]['unit'] + ')')
    ax1.set_ylabel('Hours')
    ax1.set_ylim(max(interval_time), min(interval_time))
    plt.title(las.curves[interval.name]['descr'] + '-' + las.curves[interval_.name]['descr'])
    ax1.grid(axis = 'both')
    ax1.legend(handles = p1+p2, loc = 'best')
    # ax2.spines['top'].set_position(('outward', 20))
    
    fig = px.line(df, x = [i[0], i[1]], y = 'REAL_TIME', range_y = (max(df['REAL_TIME']), min(df['REAL_TIME'])))
    fig.write_html(parent_dir + directory + '/' + i[0] + i[1] + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.html')

    plt.savefig(parent_dir + directory + '/' + i[0] + i[1] + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.png', dpi = 250)
    # plt.show()

gasses = ['C1','C2','C3','IC4','NC4','IC5','NC5']
fig, ax1 = plt.subplots(1,2, sharey = True)

for i in gasses:
    ax1[0].scatter(df[i],df['REAL_TIME'], s = 3, label = i)

ax1[0].legend()
ax1[0].set_ylim(max(df['REAL_TIME']), min(df['REAL_TIME']))
ax1[0].set_ylabel(las.curves['TIME']['mnemonic'] + las.curves['TIME']['unit'])
ax1[0].set_xlabel(las.curves[i]['unit'])
ax1[0].grid(axis = 'both')
ax1[0].set_title(las.curves['TIME']['descr'] + '-' + ' '.join(gasses))

ax1[1].scatter(df['TG'], df['REAL_TIME'], s = 3, label = 'TG', c = 'r')
ax1[1].set_ylim(max(df['REAL_TIME']), min(df['REAL_TIME']))
ax1[1].set_ylabel(las.curves['TIME']['unit'])
ax1[1].set_xlabel(las.curves['TG']['unit'])
ax1[1].grid(axis = 'both')
ax1[1].set_title(las.curves['TIME']['descr'] + '-' + las.curves['TG']['descr'])
ax1[1].legend()

plt.savefig(parent_dir + directory + '/'+ 'GAS_' + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.png', dpi = 250)
# plt.show()

fig, ax1 = plt.subplots(nrows = 1, ncols= 2, sharey = True)
ax2 = ax1[0].twiny()
# ax3 = ax1[0].twinx()
ax4 = ax1[0].twiny()
ax5 = ax1[0].twiny()

p1 = ax1[0].plot(df['ROP'], df['REAL_TIME'], c = 'g', label = 'ROP', linewidth = 0.5)

p2 = ax2.plot(df['TQ'], df['REAL_TIME'], c = 'm', label = 'TORQUE', linewidth = 0.5)

# ax3.plot(df['ROP'], df['BIT_POS'], c = 'g', label = 'TIME', linewidth = 0.01)#FOR SECOND Y AXES
# ax3.set_ylabel('BIT_POS')
# plt.yticks(rotation = 45)

p3 = ax4.plot(df['PRESSURE_IN'], df['REAL_TIME'], label = 'SPP', linewidth = 0.5, c = 'r')
ax4.set_xlabel('SPP')
ax4.spines['top'].set_position(('outward', 30))

p4 = ax5.plot(df['RPM_TOT3'], df['REAL_TIME'], label = 'RPM TOTAL', linewidth = 0.5, c = 'y')
ax5.set_xlabel('RPM TOTAL')
ax5.spines['top'].set_position(('outward', 60))

ax1[0].legend(handles=p1+p2+p3+p4, loc='best')

# ax3.plot(df['PRESSURE_IN'], df['BIT_POS'], c = 'g', label = 'SPP')
ax1[0].set_ylim(max(df['REAL_TIME']), min(df['REAL_TIME']))
# ax3.set_ylim(max(df['BIT_POS']), min(df['BIT_POS']))
ax1[0].set_xlabel(las.curves['ROP']['mnemonic'] + '(' + las.curves['ROP']['unit'] + ')')
ax1[0].set_ylabel('TIME')
ax2.set_xlabel(las.curves['TQ']['mnemonic'] + '(' + las.curves['TQ']['unit'] + ')')
ax1[0].grid()
# ax1[0].set_title(las.curves['BIT_POS']['descr'] + '-' + las.curves['ROP']['descr'] + '/' + las.curves['TQ']['descr'])

# plt.tight_layout(pad = 0)

#SECOND COLUMN GRAPH
ax1_1 = ax1[1].twiny()
ax1[1].plot(df['BIT_POS'], df['REAL_TIME'])
ax1_1.plot(df['ROTARY_3'], df['REAL_TIME'], c = 'r')
ax1_1.set_xlabel('RPM')
ax1[1].set_ylim(max(df['REAL_TIME']), min(df['REAL_TIME']))
ax1[1].set_xlabel('BIT POS')
ax1[1].set_ylabel('TIME')
ax1[1].grid(axis = 'both')
# ax6 = ax1[1].twinx()
# ax6.plot(df['BIT_POS'], df['REAL_TIME'], label = 'RPM TOTAL', linewidth = 0.5, c = 'y')

plt.savefig(parent_dir+ directory + '/' +'OPT_' + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.png',dpi = 250)

fig, ((ax1,ax2,ax3,ax4)) = plt.subplots(nrows = 1, ncols = 4, sharey = True)

ax1.plot(df['FLOWPADDLE'], df['REAL_TIME'], c = 'deeppink')
ax1.set_title('FLOWPADDLE')
ax1.set_xlabel('FLOWPADDLE')
ax1.set_ylabel('TIME')
ax1.set_ylim(max(df['REAL_TIME']), min(df['REAL_TIME']))
ax1.grid(axis = 'both')

ax2.plot(df['PRESSURE_IN'], df['REAL_TIME'], c= 'r')
ax2.set_title('SPP')
ax2.set_xlabel('SPP')
ax2.grid(axis = 'both')

ax3.plot(df['FR'], df['REAL_TIME'], c = 'c')
ax3.set_title('FLOW RATE')
ax3.set_xlabel('FLOW RATE')
ax3.grid(axis = 'both')

ax4.plot(df['STK1'], df['REAL_TIME'], label = 'PUMP-1', c = 'b')
ax4.plot(df['STK2'], df['REAL_TIME'], label = 'PUMP-2', c = 'm')
ax4.set_title('PUMP1 - PUMP2')
ax4.set_xlabel('PUMP1 - PUMP2')
ax4.grid(axis = 'both')
ax4.legend()


plt.savefig(parent_dir+ directory + '/' +'HYDROLIC_' + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.png',dpi = 250)
# plt.write_html(parent_dir + directory + '/' +'OPT_' + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.html')
plt.show()


fig= px.line(df, x = ['ROP','PRESSURE_IN','RPM_TOT3','TQ','WOB3','BIT_POS'], y = 'REAL_TIME', range_y = (max(df['REAL_TIME']), min(df['REAL_TIME'])))
fig.write_html(parent_dir+ directory + '/' +'OPT_' + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.html')

# df.to_csv('C:/Python_Works/asfsd.csv', header = True, index = True)
df.to_excel(parent_dir+ directory + '/' + las.well['WELL']['value'] + '_' + las.well['DATE']['value'].replace('/','') + '_' + '.xlsx', index = False)


