from road import Road
import csv
import math

class Roads():
	def __init__(self,roadsList):
		self.roads =[]
	 	for itr in roadsList:
			self.roads.append(Road(itr[0],itr[1],itr[2],itr[3],itr[4],itr[5],itr[6], itr[7], itr[8]))

	def SignalCheck(self,itr):
		if (itr+1)%20 == 0:            #check itr logic
			for road in self.roads:
				if road.Signal == "Red": road.Signal="Green"
				else : road.Signal="Red"

	def UpdateRoads(self,Time):
		for road in self.roads:
			road.trafficIterator(Time)	
		 				
	def getCurrentState(self):
		state = ()
		for road in self.roads:
			no_of_vehicles = road.getNoOfVehicles()
			print (no_of_vehicles)
			if no_of_vehicles<200:
				st = no_of_vehicles/10
			else:
				st = 20
			state += (st, )

		return state

	def updateSignals(self, signal):
		for i in range(0, len(self.roads)):
			if signal[i]==0:
				self.roads[i].Signal="Red"
			else:
				self.roads[i].Signal="Green"
		return

	def getTotalDelay(self):
		delay=0
		for road in self.roads:
			delay += road.getRoadDelay()
		return delay

	# def getAvgDelay(self):
	# 	delay = 0
	# 	for road in self.roads:
	# 		if road.getNoOfVehicles() > 0:
	# 			delay += float(road.getRoadDelay())/road.getNoOfVehicles()
	# 	return delay

	def getTotalNoOfVehicles(self):
		vehicles_count = 0
		for road in self.roads:
			vehicles_count += road.getNoOfVehicles()

		return vehicles_count
