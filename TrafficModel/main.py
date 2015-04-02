from roads import Roads
import csv

def main(TimeToSimulate,TStep):
    wrtFile1= open("road1.csv",'w')
    wrtFile2= open("road2.csv",'w')
    #specsFile1 = open("road1_specs.csv",'rb')
    #specsFile2 = open("road2_specs.csv",'rb')
    roads = Roads([[wrtFile1,TStep,30,"road1_specs.csv","Red"],[wrtFile2,TStep,30,"road2_specs.csv","Green"]])
    NumIterations = int(TimeToSimulate*(1/TStep))

    for itr in range(NumIterations):
        Time = itr*TStep
        roads.UpdateRoads(Time)
        roads.SignalCheck(itr)  #needs to change for Qlearning

    wrtFile1.close()
    wrtFile2.close()
    #specsFile1.close()
    #specsFile2.close()


main(20,0.25) #input value
