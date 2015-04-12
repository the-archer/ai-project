from roads import Roads
import csv


def getAction(current_green, duration, no_of_roads):
	f = ()
	for i in range(no_of_roads):
		if i == current_green:
			f += (1,)
		else:
			f += (0,)
	return (f, duration[current_green])


def main(TimeToSimulate,TStep):
		wrtFile1= open("road1.csv",'w')
		wrtFile2= open("road2.csv",'w')
		#specsFile1 = open("road1_specs.csv",'rb')
		#specsFile2 = open("road2_specs.csv",'rb')
		roads = Roads([[wrtFile1,TStep,700,"road1_specs.csv","Red"],[wrtFile2,TStep,700,"road2_specs.csv","Green"]])
		NumIterations = int(TimeToSimulate*(1/TStep))
		
		no_of_roads = 2
		duration = [30, 15]
		current_green = 0
		action = getAction(current_green, duration, no_of_roads)
		print ("Action = " + str(action))
		timeToCallQL=action[1]
		#timetoCallQLorig=timeToCallQL
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
				#newstate = roads.getCurrentState()
				roads.getCurrentState()
				#print ("State = " + str(newstate))
				print ("Penalty = " + str(penalty))
				 				  
				#a.update(oldstate, action, newstate, penalty, ((itr)>=NumIterations*0.9))
				current_green = (current_green+1)%no_of_roads
				action = getAction(current_green, duration, no_of_roads)
				print ("Action = " + str(action))
				#oldstate = newstate
				penalty=0

				timeToCallQL = action[1]
				#timetoCallQLorig=timeToCallQL
				roads.updateSignals(action[0])

			Time = itr*TStep
			roads.UpdateRoads(Time)
			totaldelay = (roads.getTotalDelay()*TStep/1000000)
			#penalty += totaldelay/timetoCallQLorig
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



main(60*60*5,0.25) #input value
