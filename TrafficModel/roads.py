from road import Road
import csv

class Roads():
	def __init__(self,roadsList):
		self.roads =[]
	 	for itr in roadsList:
			self.roads.append(Road(itr[0],itr[1],itr[2],itr[3],itr[4]))

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
			if no_of_vehicles<50:
				st = no_of_vehicles/5
			else:
				st = 10
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