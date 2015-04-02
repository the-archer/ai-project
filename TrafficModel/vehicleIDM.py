## Vehicle For Traffic simulation
## Contains: driving Algorythm and data output
from __future__ import division
from math import sqrt
#import psyco
#psyco.full()
class vehicle():
    def __init__(self,vehicleType,position,speed,TrackLength,CarNumber,TrackCar='Off',Speedlimit=33.33,T_Step=.25,T=1.6,So=2,a=0.73,b=1.67,beta=4,S1=0,vehicle_length=5):
        self.position=position
        self.speed=speed
        self.accel=0
        self.T_Step=T_Step
        self.TrackCar=TrackCar
        self.Speedlimit=Speedlimit
        self.TotalTime=0
        self.TrackLength=TrackLength
        self.CarNumber=CarNumber
        self.T=T
        self.a=a
        self.b=b
        self.beta=beta
        self.So=So
        self.S1=S1
        self.FlowFlag=0
        self.vehicle_length=vehicle_length
        self.vehicleType = vehicleType
        self.delay = 0
   
        
        
    def step(self,Signal,GlobalTime,FileName,next_car_pos,next_car_speed):  # gets called for each object
        self.FlowFlag=0
        self.delay+=1
        if Signal=="Green" and next_car_pos==self.TrackLength: #value is hardcoded now
            accel = self.a
        else:
            s=self.So+self.T*self.speed+self.speed*(self.speed-next_car_speed)/(2*(self.a*self.b)**0.5)
            pt1=(self.speed/self.Speedlimit)**self.beta    #Speedlimit = v0, beta = 4
            if next_car_pos==self.position:
                pt2=0
            else:
                pt2=(s/(next_car_pos-self.position-self.vehicle_length))**2.0 #car length = vehicle_length
            accel=self.a*(1-(pt1)-pt2)
			
        self.accel=accel# for debug
        self.speed=self.speed+self.accel*self.T_Step #assuming accel is fixed for step time
       
        if self.speed<0:
            self.speed=0.0

        velo=self.speed# debug
        self.position=self.position+self.speed*self.T_Step # needs to be changed
        #self.position=self.position + self.speed*self.T_Step - .5*(self.accel *self.T_Step *self.T_Step )
        position=self.position#debug
        self.TotalTime=self.TotalTime+self.T_Step
        Time=self.TotalTime#debug

        #if self.position> self.TrackLength:
         #   self.position=self.position-self.TrackLength
         #   self.FlowFlag=1
            
        if (self.TrackCar in('On','on') and self.position <= self.TrackLength ): #100 is signal position
            FileName.write(str(Signal)+','+str(GlobalTime)+','+str(self.vehicleType)+','+str(self.CarNumber)+','+str(position)+','+str(velo)+','+str(accel)+'\n') #data output  stdout is change to a file in "Main"
            
    def setSpeed(self,speed):
        self.speed=speed

    def getDelay(self):
        return self.delay
        
