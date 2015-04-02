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
        
