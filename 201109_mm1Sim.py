# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 11:40:16 2020

@author: Administrator
"""
# 引入数学计算模块
import math
# 引用随机数模块
import random

# 排队者（人）类
class Person:    
    # 到达、开始服务、离开时间点、人员ID
    arriveTime = 0
    serviceBeginTime = 0
    departTime = 0
    pID = 0
    
    # 排队者实时状态：0即未进入；1即到达并排队中；2即服务中；3即离开了   
    status = 0
    
    def __init__(self, arriveTime, pid):
        self.arriveTime = arriveTime
        self.status = 1
        self.pID = pid

# 队列（排队）类
class QueueSim:
    
    # 数组类变量
    # 服务站状态：0即空闲；1即忙碌
    serverStatus = 0
    
    # 到达排队队列；Person一个挨一个
    # 队列中第一个Person为正在服务中
    queueList = []
    
    # 事件队列
    # eventList = []
    
    # 所有离开的Person队列，用于统计方便
    deptList = []
    
    nextArrTime = 0
    # 最近一个离开时间，初始值必须最大值！
    nextDeptTime = 999999
    
    # 实时变量
    # 仿真计时：实时时间
    simClock = 0
    
    # 统计变量
    # 设备累计繁忙时间
    servTimeAccum = 0    
    # 累计等待时间
    delayTimeAccm = 0
    # 累计总等待时间
    totalTimeAccm = 0
    
    # 仿真人数统计
    maxPeopleNums = 0
    # 人员编号
    personID = 0
    
    # 负指数分布参数
    arrMean = 0
    servMean = 0
    
    def initialize(self, num, aMean, sMean): 
        self.maxPeopleNums = num
        self.arrMean = aMean
        self.servMean = sMean
        self.nextArrTime = self.expRand(self.arrMean)

        print("Simulation initialize()--nextArrTime: " 
              + str(round(self.nextArrTime, 2))
              + " nextDeptTime: " + str(round(self.nextDeptTime, 2)))
    
    # 仿真终止函数    
    def isFinished(self):
        if(len(self.deptList) >= self.maxPeopleNums):
            return True
        
        else:
            return False        
               
    # 时间步进函数    
    def clockUpd(self):
        
        # 检测是否到达“满员”，闭门谢客
        if(self.personID >= self.maxPeopleNums):
            print(str(self.personID) 
                  + ' persons has arrived! $ 准备收工!')
            self.nextArrTime = 999999
            print('clockUpd()--nextArrTime: ' 
                  + str(round(self.nextArrTime, 2)))
        
        # 对比，找出下一个事件时间
        if (self.nextArrTime < self.nextDeptTime):
            self.simClock = self.nextArrTime
        else:
            self.simClock = self.nextDeptTime
        
        # print('clockUpd()--SimClock: ' + str(round(self.simClock, 2)))
        
        print('clockUpd()--SimClock: ' + str(round(self.simClock, 2)) 
              + " nextArrTime: " + str(round(self.nextArrTime, 2))
              + " nextDeptTime: " + str(round(self.nextDeptTime, 2)))        
            
    
    # 随机数生成（时间间隔）
    def expRand(self, mean):
        
        # 基于import模块rando，生成均匀分布随机数
        r = random.uniform(0, 1)
        
        # 返回负指数分布随机数
        return - mean * math.log(r)
    
    # 到达函数    
    def arrive(self):
        
        # print("New person arrived!")
        
        self.personID += 1
        newPerson = Person(self.simClock, self.personID)
        # 加入排队队列
        self.queueList.append(newPerson)       
        
        # 查看是设备是否空闲，忙则排队
        if (self.serverStatus == 0):
            
            # print('New person is serving!')
            
            # 设备空闲，则马上服务
            self.serverStatus = 1
            # 关键：设置新的depart时间
            self.nextDeptTime = self.simClock + self.expRand(self.servMean)
            print("arrive()--Begin serving--set nextDeptTime: " 
                  + str(round(self.nextDeptTime, 2)))
            
            # person进入服务状态
            newPerson.status = 2
            newPerson.serviceBeginTime = self.simClock
                    
        # 生成下一个新到达时间
        self.nextArrTime += self.expRand(self.arrMean)
        print("arrive()--set nextArrTime: " 
                  + str(round(self.nextArrTime, 2)))

    # 离开（服务完毕）函数    
    def depart(self):
        
        # print('A person depart!')
        
        # 服务完毕
        deptPerson = self.queueList.pop(0)
        # 设为离开状态
        deptPerson.status = 3
        deptPerson.departTime = self.simClock
                
        # 加入离开队列
        self.deptList.append(deptPerson)

        # 安排下一个服务
        if(len(self.queueList) == 0):
            
            # 如果没有人排队，设备设为空闲
            self.serverStatus = 0
            # 无人准备离开，恢复nextDeptTime为最大值
            self.nextDeptTime = 9999999
            print("depart()--The queue is empty, RESET nextDeptTime: " 
                  + str(round(self.nextDeptTime, 2)))
        
        else:
            # 下一个服务
            servPerson = self.queueList[0]
            servPerson.status = 2
            servPerson.serviceBeginTime = self.simClock
            # 设备设为忙
            self.serverStatus = 1
            # 生成下一个新离开时间
            self.nextDeptTime += self.expRand(self.servMean)
            print("depart(): " + str(len(self.queueList)) 
                  + " persons in the queue!")
            print("And set nextDeptTime: " 
                  + str(round(self.nextDeptTime, 2)))
        
    # 统计更新函数，离开事件才能触发！
    def statUpd(self):
        
        # 判断是否无人离开
        if (len(self.deptList) == 0):
            print('No one depart.')
        
        else:
            # 排队时间累计更新
            self.delayTimeAccm += (self.deptList[-1].serviceBeginTime
                                   - self.deptList[-1].arriveTime)
            
            # 设备繁忙时间累计更新
            self.servTimeAccum += (self.deptList[-1].departTime
                                   - self.deptList[-1].serviceBeginTime)
            
            # 累计总时间（含等待时间与服务时间）更新
            self.totalTimeAccm += (self.deptList[-1].departTime
                                   - self.deptList[-1].arriveTime)
    
    
    # 报告生成函数
    def report(self):
        print('')
        print('==================== Simulation  Report ====================')
        
        print('')
        print('==================== Persons Information ====================')
        for i in range(len(self.deptList)):
            print('Person ID: ' + str(self.deptList[i].pID)
                  + '! Arrive Time: ' 
                  + str(round(self.deptList[i].arriveTime,2)) 
                  + '! Start Service Time: ' 
                  + str(round(self.deptList[i].serviceBeginTime,2))
                  + '! Depart Time: ' 
                  + str(round(self.deptList[i].departTime,2))) 
       
        print('')
        print('==================== System Statistics ====================')
        print('M/M/1 仿真')
        print('仿真人数：' + str(round(self.personID, 2)))
        print('到达平均间隔时间：' + str(round(self.arrMean, 2)))
        print('服务平均时间：' + str(round(self.servMean, 2)))
        
        print('')
        print('仿真运行时间：' 
              + str(round(self.simClock, 2)))
        print('总排队时间（delay）：' 
              + str(round(self.delayTimeAccm, 2)))
        print('总服务时间：' 
              + str(round(self.totalTimeAccm, 2)))
        print('设备繁忙累计时间（serving）：' 
              + str(round(self.servTimeAccum, 2)))
        
        print('')
        print('平均排队时间：' 
              + str(round(self.delayTimeAccm / self.personID, 2)))
        print('平均服务时间：' 
              + str(round(self.totalTimeAccm / self.personID, 2)))
        print('设备使用率：' 
              + str(round(self.servTimeAccum / self.simClock, 2)))
        print('平均排队人数：' 
              + str(round(self.delayTimeAccm / self.simClock, 2)))
        
        return
    

# 主函数
def main():
    
    # 仿真次数
    num_queuer = 1000
    arriveMean = 1.0
    serviceMean = 0.5
        
    # 创建QueueSim对象
    qs = QueueSim()
    
    # 仿真初始化
    qs.initialize(num_queuer, arriveMean, serviceMean)
    
    print("Welcome! The simulation begin: Testing " 
          + str(num_queuer) + " persons!")
    print('')
    print('==================== Simulation  LOG ====================')
    print('')
    
    # 仿真循环，设置仿真终止条件
    while(qs.isFinished() == False):
        
        qs.clockUpd()
                
        # 时间步进，调度arrive与depart事件
        if(qs.simClock == qs.nextArrTime):        
            qs.arrive()
        else:
            qs.depart()
            
            # 仿真统计更新
            qs.statUpd()
    
    else:
        print("The Queue Simulation FHINSHED! THANK YOU!")
        qs.report()
                
    return

if __name__ == '__main__':
    main()    
        
