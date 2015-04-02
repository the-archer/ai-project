from roads import Roads
import csv

import qlearningAgents

def main(TimeToSimulate,TStep):
		wrtFile1= open("road1.csv",'w')
		wrtFile2= open("road2.csv",'w')
		#specsFile1 = open("road1_specs.csv",'rb')
		#specsFile2 = open("road2_specs.csv",'rb')
		roads = Roads([[wrtFile1,TStep,30,"road1_specs.csv","Red"],[wrtFile2,TStep,30,"road2_specs.csv","Green"]])
		NumIterations = int(TimeToSimulate*(1/TStep))
		gamma = 0.8 
		alpha = 0.2 
		epsilon = 0.5 # Have to make it variable
		no_of_roads = 2
		a = qlearningAgents.QLearningAgent(epsilon, alpha, gamma, no_of_roads)
		oldstate = ()
		newstate = (0, 0)
		action = a.getAction(newstate)
		oldstate = newstate
		timeToCallQL=action[1]
		roads.updateSignals(action[0])
		penalty=0							
		for itr in range(NumIterations):
			print action
			if(timeToCallQL==0):
				newstate = roads.getCurrentState()
				print newstate				  
				a.update(oldstate, action, newstate, penalty)
				action = a.getAction(newstate)
				oldstate = newstate
				penalty=0
				timeToCallQL = action[1]
				roads.updateSignals(action[0])

			Time = itr*TStep
			roads.UpdateRoads(Time)
			penalty += roads.getTotalDelay()
			#roads.SignalCheck(itr)  #needs to change for Qlearning
			timeToCallQL-=1
		wrtFile1.close()
		wrtFile2.close()
		#specsFile1.close()
		#specsFile2.close()


main(1000,0.25) #input value
