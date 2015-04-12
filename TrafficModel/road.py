from vehicleIDM import vehicle
import random
#import psyco
#psyco.full()
import os
import sys
import csv
import math

class Road():
	def __init__(self,FileName,Tstep,RoadLength,SpecsFile,signal, start_time_hour, start_time_min, start_time_sec, static):
		self.Tstep = Tstep
		self.RoadLength = RoadLength
		self.NumCars= 0
		self.Traffic = []
		self.FileName = FileName
		self.specificCarNumber = 0
		self.VehicleAddFlag = 0
		self.Vehicle =[[],[],[]]
		self.VehicleLength=[2,1,5]
		self.LastCarPassed=True
		self.CheckNextVehicleTime = 0
		self.Signal = signal
		self.start_time = start_time_hour*60*60 + start_time_min*60 + start_time_sec
		self.static = static

		with open(SpecsFile, 'rb') as csvfile:              # file: Type Speedlimit acc deceleration prob_k1 sin_a sin_b sin_c
                                                                     #   where 1/lambda = a*sin(bt) + c
				file = csv.reader(csvfile, delimiter=',')
				for row in file:
					for i in range(1,len(row)):
						if row[0]=="Car": self.Vehicle[0].append(float(row[i]))
						elif row[0]=="Auto": self.Vehicle[1].append(float(row[i]))
						elif row[0]=="Bus": self.Vehicle[2].append(float(row[i]))
		
		NextVehicleInfo = self.GenerateVehicle(time_now = self.start_time)
		self.NextVehicle=NextVehicleInfo[0]
		self.NextVehicleTime = NextVehicleInfo[1]

	def trafficIterator(self,CurTime):
		RoadLength = self.RoadLength
		if not self.LastCarPassed:
			if self.Traffic:
				lastVehicle=self.Traffic[-1].vehicleType
				lastVehiclePos = self.Traffic[-1].position
				if  lastVehiclePos >  self.VehicleLength[lastVehicle]+ self.Traffic[-1].So :
					self.LastCarPassed = True
					self.CheckNextVehicleTime = 0


		if  self.LastCarPassed:
			self.CheckNextVehicleTime+=self.Tstep
			if self.CheckNextVehicleTime >= self.NextVehicleTime:
					self.CheckNextVehicleTime = 0
					self.LastCarPassed = False
					self.AddVehicle()
					NextVehicleInfo = self.GenerateVehicle(time_now = self.start_time + (CurTime))
					self.NextVehicle=NextVehicleInfo[0]
					self.NextVehicleTime = NextVehicleInfo[1]

		self.trafficMove(self.Signal,CurTime) #move the vehicles      
					
	def AddVehicle(self):
		self.Traffic.append(vehicle(self.NextVehicle,0,10,self.RoadLength,self.specificCarNumber,TrackCar='On',T_Step=self.Tstep,\
									Speedlimit=self.Vehicle[self.NextVehicle][0],a=self.Vehicle[self.NextVehicle][1],b=self.Vehicle[self.NextVehicle][2],\
									vehicle_length=self.VehicleLength[self.NextVehicle]))     #car no starts with 0, v = 10 initial
		self.specificCarNumber +=1
		self.NumCars += 1
	   
	def trafficMove(self,Signal,Time):       #check the logic
			k=0
			while self.Traffic:      #check if Traffic is empty or not
			   # Traffic[k].step(10000,1000)
				if Signal =="Red":
					if k==0:
					   self.Traffic[k].step(Signal,Time,self.FileName,self.RoadLength,0)
					else: self.Traffic[k].step(Signal,Time,self.FileName,self.Traffic[k-1].position,self.Traffic[k-1].speed)
				
				else:
					if k==0:
					   self.Traffic[k].step(Signal,Time,self.FileName,self.RoadLength,50)        #green signal
					else:
						self.Traffic[k].step(Signal,Time,self.FileName,self.Traffic[k-1].position,self.Traffic[k-1].speed)

				pos=self.Traffic[k].position
				if pos>self.RoadLength:
					self.Traffic.pop(k)
					self.NumCars -= 1
				else:
					k+=1
					if k >= self.NumCars:
						break


	def GenerateVehicle(self,time_now):
		if self.static:
			rnd = random.uniform(0,1)

			if rnd < self.Vehicle[0][3] :
				NextVehicle = 0      
				
			elif rnd < self.Vehicle[0][3]+ self.Vehicle[1][3]:
				NextVehicle = 1
			else:
				NextVehicle = 2

			interArrTime=random.expovariate(float((1+0.0)/self.Vehicle[NextVehicle][4]))   ##bounds need to be set
			#print interArrTime
			#print self.Signal,NextVehicle,interArrTime
			return [NextVehicle,interArrTime]
		else:
			rnd = random.uniform(0,1)
			p1 = math.sin(self.Vehicle[0][3]* time_now)+1
			p2 = math.sin(self.Vehicle[1][3]* time_now)+1
			p3 = math.sin(self.Vehicle[2][3]* time_now)+1
			sum_p = p1+p2+p3
			p1 = (p1+0.0)/sum_p
			p2 = (p2+0.0)/sum_p
			p3 = (p3+0.0)/sum_p
	                
			if rnd < p1 :
				NextVehicle = 0      
				
			elif rnd < p1+ p2:
				NextVehicle = 1
			else:
				NextVehicle = 2

			meanInterArr = self.Vehicle[NextVehicle][4] * math.sin (self.Vehicle[NextVehicle][5]*time_now) + self.Vehicle[NextVehicle][6]
			interArrTime=random.expovariate(float((1+0.0)/meanInterArr))   ##bounds need to be set
			if self.RoadLength==1001:
				f=open("sineval.txt", "a")
				f.write(str(time_now) + "," + str(interArrTime)+"\n")
				f.close()
				#print meanInterArr
			#print float((1+0.0)/meanInterArr)
			
			#print self.Signal,NextVehicle,interArrTime
			return [NextVehicle,interArrTime]


	def getNoOfVehicles(self):
		#print self.NumCars
		return self.NumCars

	def getRoadDelay(self):
		delay=0
		for vehicle in self.Traffic:
			delay += vehicle.getDelay()
		return delay







		
	
