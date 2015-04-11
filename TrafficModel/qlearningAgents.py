# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html


#from learningAgents import ReinforcementAgent
#from featureExtractors import *

import random,util,math,sys

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
	def __init__(self, epsilon, alpha, gamma, no_of_roads, initial_temp, initialQValue):
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
		self.MaxTime = 60 
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma
		self.no_of_roads = no_of_roads
		self.temperature = initial_temp
		self.initialQValue = initialQValue


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
		legalActions = self.getLegalActions()
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
		legalActions = self.getLegalActions()
		action = None
		if algo==0:
			return useGreedyEpsilon(state, legalActions)
		elif algo==1:
			return useSoftMax(state, legalActions)
		"*** YOUR CODE HERE ***"
		
	def useGreedyEpsilon(self, state, legalActions):

		r = random.random()
		if r<self.epsilon:
			action = random.choice(legalActions)
		else:
			action=self.getBestPolicy(state)
		if action == None:
			action = random.choice(legalActions)
		return action

	def useSoftMax(self, state, legalActions):

		T = getAnnealingTemp()
		r = random.random()
		current = 0.0
		total = 0.0 
		for action in legalActions:
			total += math.exp(-1*(getQValue(state, action))/T)
		for action in legalActions:
			current += math.exp(-1*(getQValue(state, action))/T)
			if r < (current/total):
				return action




	def getAnnealingTemp(self):
		beta = 0.97
		self.temperature = beta*self.temperature
		return self.temperature


	def update(self, state, action, nextState, reward):
		"""
			The parent class calls this to observe a
			state = action => nextState and reward transition.
			You should do your Q-Value update here

			NOTE: You should never call this function,
			it will be called on your behalf
		"""
		"*** YOUR CODE HERE ***"
		#print nextState, self.Qval
		oldval = self.initialQValue
		if state in self.Qval and action in self.Qval[state]:
			oldval = self.Qval[state][action]
		else:
			self.Qval[state][action] = self.initialQValue
		inc = self.alpha*(reward + self.gamma*self.getMinValue(nextState) - oldval)

		self.Qval[state][action] += inc

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
				actions.append((f, t))
		return actions



class AutoVivification(dict):
		"""Implementation of perl's autovivification feature."""
		def __getitem__(self, item):
				try:
						return dict.__getitem__(self, item)
				except KeyError:
						value = self[item] = type(self)()
						return value