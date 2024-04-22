import pandas as pd
df1 = pd.read_excel(io='C:\\Users\\86178\\Desktop\\算例数据.xlsx', sheet_name='production line load')
production_load = df1['负荷号'].tolist()
df2 = pd.read_excel(io='C:\\Users\\86178\\Desktop\\算例数据.xlsx', sheet_name='time-flexible load')
time_flexible_load = df2['负荷号'].tolist()
df3 = pd.read_excel(io='C:\\Users\\86178\\Desktop\\算例数据.xlsx', sheet_name='variable power load')
variable_power_load=df3['负荷号'].tolist()
totall_load=production_load+time_flexible_load+variable_power_load

df4 = pd.read_excel(io='C:\\Users\\86178\\Desktop\\算例数据.xlsx', sheet_name='non-flexible load')
df5 = pd.read_excel(io='C:\\Users\\86178\\Desktop\\算例数据.xlsx', sheet_name='wind_polar_generation')
df6 = pd.read_excel(io='C:\\Users\\86178\\Desktop\\算例数据.xlsx', sheet_name='battery_macro-grid')
#负荷号对应的时隙
non_slot={}#不可移动负荷占用时隙
non_power={}#不可移动负荷功率
for i in range(len(df4['负荷号'])):
    j=range(df4['开始时隙'][i],df4['开始时隙'][i]+df4['时隙数量'][i])
    non_slot[df4['负荷号'][i]]=list(j)
    non_power[df4['负荷号'][i]]=df4['功率大小'][i]
#print('非移动负荷所在时隙对应的功率',non_power)

pro_ear_lat={}#产线负荷的最早和最晚开始时隙
pro_len_slot={}#获取时隙长度
pro_power={}#获取负荷加工功率
for i in range(len(df1['负荷号'])):
    j=range(df1['最早开始时隙'][i],df1['最晚开始时隙'][i]+1)
    pro_ear_lat[df1['负荷号'][i]]=list(j)
    pro_len_slot[df1['负荷号'][i]]=df1['时隙长度'][i]
    pro_power[df1['负荷号'][i]]=df1['加工功率'][i].split('，')#把一长串字符分割成单个字符
#print(pro_len_slot)

fle_ear_lat={}#时间灵活性负荷最早和最晚开始时隙
fle_len_slot={}#获取时隙长度
fle_power={}#获取负荷加工功率
for i in range(len(df2['负荷号'])):
    j=range(df2['最早开始时隙'][i],df2['最晚开始时隙'][i]+1)
    fle_ear_lat[df2['负荷号'][i]]=list(j)
    fle_len_slot[df2['负荷号'][i]]=df2['时隙长度'][i]
    fle_power[df2['负荷号'][i]]=df2['功率大小'][i]
#print(fle_ear_lat)

via_ear_lat={}#变动功率负荷最早和最晚开始时隙
via_len_slot={}#变动功率负荷的时隙长度
via_low_power={}#变动功率负荷的最低功率
via_high_power={}#变动功率负荷的最高功率
via_totall_load={}#变动功率的总负荷
for i in range(len(df3['负荷号'])):
    j=range(df3['最早开始时隙'][i],df3['最晚开始时隙'][i]+1)
    via_ear_lat[df3['负荷号'][i]]=list(j)
    via_len_slot[df3['负荷号'][i]]=df3['时隙长度'][i]
    via_low_power[df3['负荷号'][i]]=df3['最低功率'][i]
    via_high_power[df3['负荷号'][i]] = df3['最高功率'][i]
    via_totall_load[df3['负荷号'][i]] = df3['总负荷'][i]
#print(via_len_slot)

win_max_power=df5.iloc[1:,2].tolist()
pol_max_power=df5.iloc[1:,4].tolist()
new_cost=df5.iloc[1:,5].tolist()
print(win_max_power)
print(pol_max_power)
print(new_cost)

macro_cost=df6.iloc[1:,1].tolist()
battery_max_cha=df6.iloc[1:,2].tolist()
battery_max_dis=df6.iloc[1:,3].tolist()
battery_cha_cost=df6.iloc[1:,7].tolist()
print(macro_cost)
print(battery_max_cha)
print(battery_max_dis)
print(battery_cha_cost)






