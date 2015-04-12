from roads import Roads
import csv

import qlearningAgents
import sys

def main(TimeToSimulate,TStep):
		wrtFile1= open("road1.csv",'w')
		wrtFile2= open("road2.csv",'w')
		#specsFile1 = open("road1_specs.csv",'rb')
		#specsFile2 = open("road2_specs.csv",'rb')
		static = True
		var = ""
		if sys.argv[1]=="1":
			static = False
			var = "_var"
		roads = Roads([[wrtFile1,TStep,1000,"road1_specs"+var+".csv","Red", 15, 0, 0, static],[wrtFile2,TStep,1000,"road2_specs"+var+".csv","Green", 15 , 0, 0, static]])
		NumIterations = int(TimeToSimulate*(1/TStep))
		gamma = 0.8 
		#alpha = 0.2 
		epsilon = 0.5 # Have to make it variable
		no_of_roads = 2
		a = qlearningAgents.QLearningAgent(gamma, no_of_roads, initial_temp = float(sys.argv[3]), initialQValue = 0.0)
		oldstate = ()
		newstate = (0, 0)
		action = a.getAction(newstate, algo = 1)
		print ("Action = " + str(action))
		oldstate = newstate
		timeToCallQL=action[1]
		timetoCallQLorig=timeToCallQL
		roads.updateSignals(action[0])
		penalty=0
		episodelength = 5*60
		episodecount = 0 
		f1 = open("results.txt", "w")
		totaldelay  = 0
		avgdelay  = 0
		f2 = open("vehiclecounts.txt", "w")	
		vehiclecounts = 0	
		totdelay = 0						
		for itr in range(NumIterations):
			

			if(timeToCallQL<=0):
				print (" ")
				print ("Time = " +  str(itr*TStep))	
				newstate = roads.getCurrentState()
				print ("State = " + str(newstate))
				print ("Penalty = " + str(penalty))
				 				  
				a.update(oldstate, action, newstate, penalty, ((itr)>=NumIterations*0.9))
				action = a.getAction(newstate, algo = 1)
				print ("Action = " + str(action))
				oldstate = newstate
				penalty=0

				timeToCallQL = action[1]
				timetoCallQLorig=timeToCallQL
				roads.updateSignals(action[0])

			Time = itr*TStep
			roads.UpdateRoads(Time)
			totaldelay = (roads.getTotalDelay()*TStep/1000000)
			penalty += totaldelay/timetoCallQLorig
			totdelay += totaldelay
			if roads.getTotalNoOfVehicles() > 0:
				avgdelay += float(totaldelay)/roads.getTotalNoOfVehicles()	#total_no_of_vehicles = 
			#vehiclecounts += roads.getTotalNoOfVehicles()
			f2.write(str(Time+TStep)+ "," + str(roads.getTotalNoOfVehicles()) + "\n")
			if((Time+TStep)%episodelength==0):
				episodecount += 1
				f1.write(str(episodecount*episodelength)+ "," + str(totdelay) + "\n")
				avgdelay = 0
				totdelay = 0
				#f2.write(str(episodecount*episodelength)+ "," + str(vehiclecounts) + "\n")
				#vehiclecounts = 0
			#roads.SignalCheck(itr)  #needs to change for Qlearning
			timeToCallQL-=TStep
		wrtFile1.close()
		wrtFile2.close()
		f1.close()
		f2.close()		
		#specsFile1.close()
		#specsFile2.close()



main(60*60*int(sys.argv[2]),0.25) #input value
