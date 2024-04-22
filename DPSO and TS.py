import random
from load import totall_load, non_slot, non_power, pro_ear_lat, pro_len_slot, pro_power, fle_ear_lat, fle_len_slot, \
    fle_power,via_ear_lat,via_len_slot,via_low_power,via_high_power,via_totall_load,win_max_power,pol_max_power,new_cost,macro_cost,battery_max_cha,battery_max_dis,battery_cha_cost
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import copy
import datetime
import os

# 禁忌长度
tabu_limit = 10
# 禁忌表
tabu_list = []
# 候选集
del_list = []
candidate_length = 5
# 存放最优值
fitness_best = []
count = []

Z = 360 # 微电网载荷极限

def random1(num):
    work = []  # 存放打乱的粒子
    initial_c1 = []  # 存放打乱的粒子对应的索引顺序
    for i in range(num):
        work1 = []  # 存放AAAAAA
        AA = random.sample(range(90), 90)
        for j in AA:
            work1.append(totall_load[j])
        if work1 not in work:
            work.append(work1)
    return work




def fit(work):
    time_power = {}  # 定义每个时隙的功率
    machine_time = {}  # 定义机器载荷时间
    slot_load={}#每个负荷安排在的时隙
    machine_load={}#产线任务被安排在哪个机器
    for i in totall_load:
        slot_load[i]=[]
    for m in range(1, 9):#遍历所有机器
        machine_time[m] = []#定义机器载荷时间
    for i in range(1, 25):  # 所有时隙
        time_power[i] = 0
    for i in non_slot:  # 不可移动负荷占用功率
        for j in non_slot[i]:
            time_power[j] = time_power[j] + non_power[i]
    for i in range(len(work)):  # 对负荷进行遍历
        if 'A' in work[i]:  # 产线负荷调度
            #print(work[i])
            for s in pro_ear_lat[work[i]]:  # 遍历产线负荷的最早开始时隙与最晚开始时隙之间的时隙
                empty_machine = [1, 2, 3, 4, 5, 6, 7, 8]  # 空闲机器列表
                for m1 in machine_time:
                    for l in range(s, s + pro_len_slot[work[i]]):
                        for ll in machine_time[m1]:
                            if l == ll or int(pro_power[work[i]][m1 - 1]) >= Z - time_power[l]:
                                if m1 in empty_machine:
                                    empty_machine.remove(m1)
                if empty_machine != []:
                    pro_start_time = s  # 确定产线负荷的开始时隙
                    for k in range(pro_start_time,pro_start_time+pro_len_slot[work[i]]):#输出负荷被安排所占时隙
                        slot_load[work[i]].append(k)
                    break
            if empty_machine==[]:
                print('无解')
                """无解即停止"""
                os.system("pause")
            #print('kkkk', empty_machine)
            random_machine = random.sample(empty_machine, 1)  # 随机选择一台空闲机器
            machine_load[work[i]]=random_machine#产线负荷对应机器设备选择
            #print('选择', random_machine)
            for l in range(pro_start_time, pro_start_time + pro_len_slot[work[i]]):  # 产线负荷l占用的时隙
                time_power[l] = int(time_power[l]) + int(pro_power[work[i]][random_machine[0] - 1])  # 更新每个时隙的功率
            for l in range(pro_start_time, pro_start_time + pro_len_slot[work[i]]):
                machine_time[random_machine[0]].append(l)
            #print(machine_time)
            #print('A',time_power)
        elif 'B' in work[i]:#对时间灵活性负荷进行调度
            #print(work[i])
            for s in fle_ear_lat[work[i]]:
                ava_slot=[]#可行连续时隙集合
                for l in range(s, s + fle_len_slot[work[i]]):
                    if time_power[l] + fle_power[work[i]] <= Z:
                        ava_slot.append(l)
                #print('kkk',ava_slot)
                if len(ava_slot)==fle_len_slot[work[i]]:
                    fle_start_time = s
                    for k in range(fle_start_time,fle_start_time+fle_len_slot[work[i]]):#输出负荷被安排所占时隙
                        slot_load[work[i]].append(k)
                    #print(fle_start_time)
                    break
            if len(ava_slot)<fle_len_slot[work[i]]:
                print('无解')
                """无解即停止"""
                os.system("pause")
            for l in range(fle_start_time, fle_start_time + fle_len_slot[work[i]]):  # 时间灵活性负荷l占用的时隙
                time_power[l] = int(time_power[l]) + int(fle_power[work[i]])  # 更新每个时隙的功率
            #print('B',time_power)
        elif 'C' in work[i]:
            #print(work[i])
            for s in via_ear_lat[work[i]]:
                via_ava_slot=[]#变动功率负荷可行连续时隙集合
                for l in range(s, s + via_len_slot[work[i]]):
                    if time_power[l] + via_low_power[work[i]] <= Z:
                        #print('llllll')
                        via_ava_slot.append(l)
                #print('时间段：',via_ava_slot)
                dif_sum=0#负荷剩余空间求和
                for ll in via_ava_slot :
                    sig_dif_sum=Z-time_power[ll]#单个时隙剩余空间
                    #print('单个剩余量',sig_dif_sum)
                    dif_sum=dif_sum+sig_dif_sum
                if len(via_ava_slot) == via_len_slot[work[i]] and dif_sum >= via_totall_load[work[i]]:
                    via_start_time = s#定义变动功率负荷的开始时隙
                    for k in range(via_start_time,via_start_time+via_len_slot[work[i]]):#输出负荷被安排所占时隙
                        slot_load[work[i]].append(k)
                    #print('执行')
                    #print('开始时隙',via_start_time)
                    break
            if len(via_ava_slot) < via_len_slot[work[i]]:
                print('无解')
                """无解即停止"""
                os.system("pause")
            #print('name',via_start_time)
            for arr_power in range(via_start_time,via_start_time+via_len_slot[work[i]]):#分配了负荷的时隙
                #print('未加最低功率',time_power[arr_power])
                time_power[arr_power]=int(time_power[arr_power])+int(via_low_power[work[i]])#先按最低功率安排
                #print('安排完最低功率之后的时隙负荷',time_power[arr_power])
                un_arr_power=int(via_totall_load[work[i]])-(int(via_len_slot[work[i]])*int(via_low_power[work[i]]))#计算仍未被安排的负荷
            for arr_power in range(via_start_time,via_start_time+via_len_slot[work[i]]):#分配了负荷的时隙
                if un_arr_power<=int(via_high_power[work[i]])-int(via_low_power[work[i]]):#判断未被安排负荷与负荷允许变动范围差值
                   time_power[arr_power]=int(time_power[arr_power])+min(un_arr_power,Z-int(time_power[arr_power]))
                   #print('jjjj',min(un_arr_power,Z-int(time_power[arr_power])))
                   own_arr_power = int(via_low_power[work[i]]) + min(un_arr_power, Z - int(time_power[arr_power]))
                   un_arr_power=un_arr_power-min(un_arr_power,Z-int(time_power[arr_power]))
                   #print('自身已安排的负荷',own_arr_power)
                else:
                    time_power[arr_power] = int(time_power[arr_power]) + min(int(via_high_power[work[i]])-int(via_low_power[work[i]]),Z - int(time_power[arr_power]))
                    #print('j1',min(int(via_high_power[work[i]])-int(via_low_power[work[i]]),Z - int(time_power[arr_power])))
                    un_arr_power = un_arr_power - min(int(via_high_power[work[i]])-int(via_low_power[work[i]]),Z - int(time_power[arr_power]))
                    own_arr_power = int(via_low_power[work[i]]) + min(int(via_high_power[work[i]])-int(via_low_power[work[i]]),Z - int(time_power[arr_power]))
                    #print('自身已安排的负荷',own_arr_power)
            #print('C',time_power)

    user_new_ele={}#用户新能源方式用电量
    bat_new_ele={}#电池用新能源充电量
    bat_ini_ele=150#储能电池初始电量
    bat_max_cap=200#储能电池最大容量
    bat_min_thr=40#储能电池最低阈值
    bat_cap_ele={}#电池当前时隙电量（时隙结束时）
    macro_dis={}#每个时隙内大电网供电值
    bat_use_ele={}#每时隙内电池放电量
    for i in range (1,len(time_power)+1):
        if time_power[i]>win_max_power[i-1]+pol_max_power[i-1]:#判断当前时隙负荷与新能源发电量大小
            user_new_ele[i]=win_max_power[i-1]+pol_max_power[i-1]#用户使用新能源用电量
            dif_ele=int(time_power[i])-int(user_new_ele[i])#计算未满足负荷值
            bat_able_dis=min(battery_max_dis[i],bat_ini_ele-bat_min_thr)#判断电池可放电量
            if dif_ele>bat_able_dis:
                bat_use_ele[i] = bat_able_dis  # 当前时刻电池的供电量
                dif_ele=dif_ele-bat_use_ele[i]#电池先放电，更新未满足负荷值
                bat_cap_ele[i]=bat_ini_ele-bat_use_ele[i]#更新电池电量，时隙结束时的电池电量
                bat_ini_ele=bat_ini_ele-bat_use_ele[i]#更新了每个时隙的初始电量
                macro_dis[i]=dif_ele#剩余所有电量均为大电网提供，更新大电网供电值
            else :
                bat_use_ele[i] = dif_ele  # 当前时刻电池的放电量
                bat_cap_ele[i] = bat_ini_ele - bat_use_ele[i]  # 更新电池电量，时隙结束时的电池电量
                bat_ini_ele = bat_ini_ele - bat_use_ele[i]  # 更新了每个时隙的初始电量
        else :
            user_new_ele[i] = time_power[i]  # 用户用新能源用电量等于当前负荷量
            bat_lack_ele=bat_max_cap-bat_ini_ele#计算电池距离满电的缺电量
            new_res=(win_max_power[i-1]+pol_max_power[i-1])-time_power[i]#新能源剩余电量
            bat_able_cha=min(bat_lack_ele,battery_max_cha[i-1])#计算电池可充电量
            if new_res>bat_able_cha:
                bat_new_ele[i]=bat_able_cha#电池充电量等于电池可充电量
                bat_ini_ele=bat_ini_ele+bat_new_ele[i]#更新电池电量
            else :
                bat_new_ele[i]=new_res#电池充电量为新能源剩余电量
                bat_ini_ele = bat_ini_ele + bat_new_ele[i] # 更新电池电量
    # print('新能源给用户供电量',user_new_ele)
    # print('大电网供电量',macro_dis)
    #print('新能源给电池供电量',bat_new_ele)
    #print('电池放电量',bat_use_ele)

    user_new_cost=0
    for i in user_new_ele:
        user_new_cost=user_new_cost+user_new_ele[i]*new_cost[int(i)-1]#新能源给用户供电成本
    macro_dis_cost = 0
    for i in macro_dis:
        macro_dis_cost = macro_dis_cost + macro_dis[i] * macro_cost[int(i)-1]  # 大电网给用户供电成本
    bat_new_cost = 0
    for i in bat_new_ele:
        bat_new_cost = bat_new_cost + bat_new_ele[i] * battery_cha_cost[int(i)-1]  # 新能源给电池供电成本
    totall_cost=user_new_cost+macro_dis_cost+bat_new_cost
    # print('新能源给用户供电成本',user_new_cost)
    # print('大电网给用户供电成本',macro_dis_cost)
    #print('新能源给电池供电成本',bat_new_cost)

    print(totall_cost)
    fitness=totall_cost
    return time_power,machine_time,machine_load,slot_load,user_new_ele, bat_new_ele,bat_cap_ele,macro_dis,bat_use_ele,fitness #调用函数返回数值

# aa=random1(10)#原始对比数据
# fit(aa[3])

def update(lizi, pBest, Gbest):
    # 随机生成两个位置
    new_lizi = []
    # print("更新前粒子：", lizi)
    # 保证两个生成数不相等
    r = random.sample(range(1, len(lizi) - 1), 2)
    r1 = r[0]
    r2 = r[1]
    # print(r1)
    # print(r2)
    # 进行第一段原始粒子更新
    for c in range(0, min(r1, r2)):
        new_lizi.append(lizi[c])
    # 进行第二段历史最优粒子段更新
    c0 = []
    # 找到粒子对应位置的索引
    for c2 in range(min(r1, r2), max(r1, r2)):
        c3 = pBest.index(lizi[c2])  # 索引的获取
        c0.append(c3)
    c4 = sorted(c0)
    # print(c4)
    for c5 in range(len(c0)):
        new_lizi.append(pBest[c4[c5]])
    c0 = []
    # 进行第三段历史最优粒子段更新
    t0 = []
    # 找到粒子对应位置的索引
    for t2 in range(max(r1, r2), len(lizi)):
        t3 = Gbest.index(lizi[t2])  # 索引的获取
        t0.append(t3)
    t4 = sorted(t0)
    for t5 in range(len(t0)):
        new_lizi.append(Gbest[t4[t5]])
    t0 = []
    # print("更新后粒子：",new_lizi)
    return new_lizi

def exchange(index1, index2, arr):
    current_list = arr.copy()
    current_list[index1] = arr[index2]
    current_list[index2] = arr[index1]
    return current_list

def get_candidate(p, tabu_list):
    candidate = []
    exchange_position = []
    i = 0
    while i < candidate_length:
        current = random.sample(range(0, len(p)), 2)
        if current not in tabu_list:
            if current not in exchange_position:
                exchange_position.append(current)
                candi = exchange(current[0], current[1], p)
                candidate.append(candi)
                i = i + 1
    return candidate, exchange_position

def draw(fitness_best, count):
    # map_show()
    fig = plt.figure()
    ax3 = fig.add_subplot()
    # ax3.set_title('适应度值迭代图')
    # 设置字体为楷体
    plt.rcParams['font.sans-serif'] = ['KaiTi']
    y = fitness_best
    x = count
    print(x)
    print(y)
    plt.plot(x, y)
    # plt.plot(np.array(fitness_best))
    plt.xlabel('迭代次数')
    plt.ylabel('适应度值')
    plt.show()


Num = 100  # 粒子个数
work= random1(Num)
fitness1 = []
for i in range(Num):
    time_power,machine_time,machine_load,slot_load,user_new_ele, bat_new_ele,bat_cap_ele,macro_dis,bat_use_ele,fitness = fit(work[i])
    print('初始粒子',work[i])
    fitness1.append(fitness)
aa = 9999999
loop = 0
for i in range(len(fitness1)):
    if fitness1[i] < aa:
        aa = fitness1[i]
        index = i
pbest1 = work
gbest1 = work[index]
GB = aa
fitness_best.append(GB)
count.append(0)
nowfitness = []
# 粒子群循环
while loop < 100:
    for i in range(Num):
        work[i]= update(work[i], pbest1[i], gbest1)
        time_power, machine_time, machine_load, slot_load, user_new_ele, bat_new_ele, bat_cap_ele, macro_dis, bat_use_ele, fitness = fit(
            work[i])
        nowfitness.append(fitness)
        if nowfitness[i] < fitness1[i]:
            fitness1[i] = nowfitness[i]
            pbest1[i] = work[i]
        if nowfitness[i] < GB:
            print('最优更新次数')
            GB = nowfitness[i]
            gbest1 = work[i]
        pp = 0
        GMax = 5
        # 禁忌搜索步骤
        tsfitness = []
        tabu_list1 = []
        ll1_1 = work[i]
        GB1 = GB
        for pp in range(GMax):
            g1, exchange_position1 = get_candidate(ll1_1, tabu_list1)
            for zz in range(candidate_length):
                time_power,machine_time,machine_load,slot_load,user_new_ele, bat_new_ele,bat_cap_ele,macro_dis,bat_use_ele,fitness = fit(g1[zz])
                tsfitness.append(fitness)
            min_index = np.argmin(tsfitness)
            ll1_1 = g1[min_index].copy()
            if exchange_position1[min_index] not in tabu_list1:
                if tsfitness[min_index] < nowfitness[i]:
                    work[i] = g1[min_index].copy()
                    nowfitness[i] = tsfitness[min_index]

                if tsfitness[min_index] < GB1:
                    GB1 = tsfitness[min_index]
                    fitness1[i] = tsfitness[min_index]
                    gbest1 = g1[min_index].copy()
                    pbest1[i] = g1[min_index].copy()
                    fitness_current = tsfitness[min_index]

                elif tsfitness[min_index] < fitness1[i]:
                    fitness1[i] = tsfitness[min_index]
                    pbest1[i] = g1[min_index].copy()
                tabu_list1.append(exchange_position1[min_index])
            if len(tabu_list1) > tabu_limit:
                del tabu_list1[0]

            tsfitness = []
    if GB1 == GB:
        print('第%d代第%d个粒子禁忌搜索之后的最小化最大成本：' % (loop + 1, i + 1), GB)
        # print('禁忌搜素之后的第一层粒子：', gbest1)
        # print('禁忌搜素之后的第二层粒子：', gbest2)
        # print('禁忌搜素之后的第三层粒子：', gbest3)
        # print('禁忌搜素之后的第四层粒子：', gbest4)
        time_power, machine_time, machine_load, slot_load, user_new_ele, bat_new_ele, bat_cap_ele, macro_dis, bat_use_ele, fitness = fit(
            work[i])
    else:
        print('第%d代第%d个粒子禁忌搜索之后的最小化最大成本：' % (loop + 1, i + 1), GB1)
        # print('禁忌搜素之后的第一层粒子：', tsbest1)
        # print('禁忌搜素之后的第二层粒子：', tsbest2)
        # print('禁忌搜素之后的第三层粒子：', tsbest3)
        # print('禁忌搜素之后的第四层粒子：', tsbest4)
        time_power, machine_time, machine_load, slot_load, user_new_ele, bat_new_ele, bat_cap_ele, macro_dis, bat_use_ele, fitness = fit(
            work[i])
    GB = GB1
    fitness_best.append(GB1)
    count.append(loop + 1)
    nowfitness = []
    loop = loop + 1
print('最优值',GB1)
# print(machine_load)
# print(gbest1)
# print(slot_load)
# print(machine_time)
print('每时隙内功率',time_power)
print('用户用新能源电量',user_new_ele)
print('储能设备用新能源充电量',bat_new_ele)
print('大电网供电量',macro_dis)
print('储能设备放电量',bat_use_ele)
draw(fitness_best, count)



