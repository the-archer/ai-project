# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html




import random,util,math,sys
from pprint import pprint
from numpy import var

class QLearningAgent():
	"""
		Q-Learning Agent

		Functions you should fill in:
			- getQValue
			- getAction
			- getValue
			- getPolicy
			- update

		Instance variables you have access to
			- self.epsilon (exploration prob)
			- self.alpha (learning rate)
			- self.discount (discount rate)

		Functions you should use
			- self.getLegalActions(state)
				which returns legal actions
				for a state
	"""
	def __init__(self, gamma, no_of_roads, initial_temp, initialQValue):
		"You can initialize Q-values here..."
		#ReinforcementAgent.__init__(self, **args)


		"*** YOUR CODE HERE ***"

		"""
		State definition: No of vehicles in each road.
		If there are r roads then its a r-tuple.
		{k1, k2, ..., kr}
		No of vehicles
		k<10 [k*5, k*5 + 5)
		k=10 [50, inf)

		Actions
		2-tuple {tuple i, int t}
		i = r-tuple of light states: 0: red, 1: green
		t = time for which to do so (eval again after that time)
		0<t<MaxTime Time = t
		t=MaxTime Time>=20


		"""
		self.Qval = AutoVivification() #implements dictionary of dictionaries
		self.Visited = AutoVivification()
		self.MaxTime = 30 
		#self.epsilon = 1
		#self.alpha = alpha
		self.gamma = gamma
		self.no_of_roads = no_of_roads
		self.initial_temp = initial_temp
		self.temperature = initial_temp
		self.initialQValue = initialQValue
		#self.static = static
		self.stablized = False
		self.varValues = []


	def getQValue(self, state, action):
		"""
			Returns Q(state,action)
			Should return initialQValue if we have never seen
			a state or (state,action) tuple
		"""
		"*** YOUR CODE HERE ***"

		
		if state in self.Qval and action in self.Qval[state]:
			return self.Qval[state][action]
		else:
			return self.initialQValue
			
			

	def getMinValue(self, state):

		"""
			Returns min_action Q(state,action)
			where the min is over legal actions.  Note that if
			there are no legal actions, which is the case at the
			terminal state, you should return a value of 0.0.
			NOTE: 0.0 value was for the max case. What should be the value here? -- Discuss
		"""
		"*** YOUR CODE HERE ***"
		minval=sys.maxsize
		#legalActions = self.getLegalActions()
		if state in self.Qval:
			for t in self.Qval[state]:
				if self.Qval[state][t]< minval:
					minval=self.Qval[state][t]
			return minval
		else:
			return self.initialQValue




		
	def getBestPolicy(self, state):
		"""
			Compute the best action to take in a state.  Note that if there
			are no legal actions, which is the case at the terminal state,
			you should return None.
		"""
		"*** YOUR CODE HERE ***"
		minval=sys.maxsize
		#legalActions = self.getLegalActions(state)
		if state in self.Qval:
			for t in self.Qval[state]:
				if self.Qval[state][t]< minval:
					minval=self.Qval[state][t]
			return t
		else:
			return None
	

	def getAction(self, state, algo):
		"""
			Compute the action to take in the current state.  With
			probability self.epsilon, we should take a random action and
			take the best policy action otherwise.  Note that if there are
			no legal actions, which is the case at the terminal state, you
			should choose None as the action.

			HINT: You might want to use util.flipCoin(prob)
			HINT: To pick randomly from a list, use random.choice(list)
		"""
		# Pick Action
		T = self.getAnnealingTemp()
		legalActions = self.getLegalActions()
		r = random.random()
		epsilon = self.getEpsilonValue()
		f1=open("eps.txt", "a")
		f1.write(str(epsilon)+"\n")
		f1.close()
		print ("epsilon  = " + str(epsilon))
		if r < epsilon:
			#print r, epsilon
			#print legalActions
			return random.choice(legalActions)
		else:		
			if algo==0:
				return self.useGreedyEpsilon(state, legalActions)
			elif algo==1:
				return self.useSoftMax(state, legalActions, T)
	


	def getEpsilonValue(self):

		#=EXP(-1/(A1))/EXP(-1/(100))

		return (math.exp(-1/self.temperature)/math.exp(-1/self.initial_temp))



	def useGreedyEpsilon(self, state, legalActions):

		
		action = self.getBestPolicy(state)
		if action == None:
			action = random.choice(legalActions)
		return action


	def useSoftMax(self, state, legalActions, T):

		
		
		r = random.random()
		current = 0.0
		total = 0.0

		if state in self.Qval:
			for action in self.Qval[state]:
				total += math.exp(-1*(self.getQValue(state, action))/T)
				#print total

			if total > 0:
			#print self.Qval[state]
				for action in self.Qval[state]:
					current += math.exp(-1*(self.getQValue(state, action))/T)
					if r <= (current/total):
						return action	
				
		
		return random.choice(legalActions) 
		




	def getAnnealingTemp(self):
		beta = 0.995
		print ("Temp = " + str(self.temperature))
		self.temperature = beta*self.temperature
		if (self.temperature < 0.5):
		 	self.temperature = 0.5
		return self.temperature


	def update(self, state, action, nextState, reward, save):
		"""
			The parent class calls this to observe a
			state = action => nextState and reward transition.
			You should do your Q-Value update here

			NOTE: You should never call this function,
			it will be called on your behalf
		"""
		"*** YOUR CODE HERE ***"
		#print nextState, self.Qval
		#alpha = self.temperature/self.initial_temp
		alpha = self.getEpsilonValue()
		print ("Alpha = " + str(alpha))
		oldval = self.initialQValue
		if state in self.Qval and action in self.Qval[state]:
			oldval = self.Qval[state][action]
		else:
			self.Qval[state][action] = self.initialQValue
		inc = alpha*(reward + self.gamma*self.getMinValue(nextState) - oldval)
		if state in self.Visited and action in self.Visited[state]:
			self.Visited[state][action] += 1
		else:
			self.Visited[state][action] = 0
		self.Qval[state][action] += inc
		if (save):
			f2=open("qval.txt", "w")
			pprint(self.Qval, stream = f2)

			#f2.write("\n------------\n")
			#f2.write(str(self.Visited))
			pprint(self.Visited, stream = f2)
			f2.close()
			#a = raw_input()
		#print self.Qval

	def getLegalActions(self):
		actions=[]
		for r in range(0, self.no_of_roads):
			f=()
			for i in range(0, self.no_of_roads):
				if i==r:
					f += (1,)
				else:
					f += (0,)
			for t in range(1, self.MaxTime+1):
				if t%5==0:
					actions.append((f, t))
		return actions

	def calculateVariance(self, delayValues, intervalLength):
		#print intervalLength
		variance = var(delayValues[-intervalLength:])
		self.varValues.append(variance)
		#print delayValues
		return self.varValues[-1]
			

	def checkStability(self, intervalLength):
		if self.varValues[-1] < 2000000:
			self.stablized = True
	
	def checkForModelChange(self, intervalLength):
		if self.stablized:

			if self.varValues[-1] > 3000000:
				#Model change detected
				self.temperature = self.initial_temp/2
				self.stablized = False
				print "Model Change detected"






class AutoVivification(dict):
		"""Implementation of perl's autovivification feature."""
		def __getitem__(self, item):
				try:
						return dict.__getitem__(self, item)
				except KeyError:
						value = self[item] = type(self)()
						return value