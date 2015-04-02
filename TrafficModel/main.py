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
		gamma: 0.8, 
		alpha: 0.2, 
		epsilon: 0.1 # Have to make it variable
		timeToCallQL=0								
		a = qlearningAgents.QLearningAgent(epsilon, alpha, gamma)
		oldstate = ()
		newstate = (0, 0)
		action = a.getAction(newstate)
		oldstate = newstate
		for itr in range(NumIterations):
			if(timeToCallQL==0):
				newstate = roads.getCurrentState()
				#reward = roads.calculateReward() Have to implement this
				a.update(oldstate, action, newstate, reward)
				action = a.getAction(newstate)
				oldstate = newstate
				timeToCallQL = action[1]

			Time = itr*TStep
			roads.UpdateRoads(Time)
			roads.SignalCheck(itr)  #needs to change for Qlearning
			
		wrtFile1.close()
		wrtFile2.close()
		#specsFile1.close()
		#specsFile2.close()


main(20,0.25) #input value
