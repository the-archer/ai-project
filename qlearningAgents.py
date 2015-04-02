# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
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
	def __init__(self, epsilon, alpha, gamma):
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
		2-tuple {int i, int t}
		i = r-tuple of light states: 0: red, 1: green
		t = time for which to do so (eval again after that time)
		t<MaxTime Time = t
		t=MaxTime Time>=20


		"""
		self.Qval = AutoVivification() #implements dictionary of dictionaries
		self.MaxTime = 20 
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma


	def getQValue(self, state, action):
		"""
			Returns Q(state,action)
			Should return 0.0 if we never seen
			a state or (state,action) tuple
		"""
		"*** YOUR CODE HERE ***"

		
		if state in self.Qval and action in self.Qval[state]:
			return self.Qval[state][action]
		else
			return 0.0
			
			

	def getValue(self, state):

		"""
			Returns min_action Q(state,action)
			where the min is over legal actions.  Note that if
			there are no legal actions, which is the case at the
			terminal state, you should return a value of 0.0.
			NOTE: 0.0 value was for the max case. What should be the value here? -- Discuss
		"""
		"*** YOUR CODE HERE ***"
		minval=sys.maxsize
		legalActions = self.getLegalActions(state)
		if state in self.Qval:
			for t in self.Qval[state]:
				if self.Qval[state][t]< minval:
					minval=self.Qval[state][t]
			return minval
		else:
			return 0.0




		
	def getPolicy(self, state):
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
	

	def getAction(self, state):
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
		legalActions = self.getLegalActions(state)
		action = None
		"*** YOUR CODE HERE ***"
		r = random.random()
		if r<self.epsilon:
			action - random.choice(legalActions)
		else:
			action=self.getPolicy(state)
		return action

	def update(self, state, action, nextState, reward):
		"""
			The parent class calls this to observe a
			state = action => nextState and reward transition.
			You should do your Q-Value update here

			NOTE: You should never call this function,
			it will be called on your behalf
		"""
		"*** YOUR CODE HERE ***"
		oldval = 0.0
		if state in self.Qval and action in self.Qval[state]:
			oldval = self.Qval[state][action]
		else:
			Qval[state][action]=0
		inc = self.alpha*(reward + self.gamma*getValue(nextState) - oldval)

		Qval[state][action] += inc

		

class PacmanQAgent(QLearningAgent):
	"Exactly the same as QLearningAgent, but with different default parameters"

	def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
		"""
		These default parameters can be changed from the pacman.py command line.
		For example, to change the exploration rate, try:
				python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

		alpha    - learning rate
		epsilon  - exploration rate
		gamma    - discount factor
		numTraining - number of training episodes, i.e. no learning after these many episodes
		"""
		args['epsilon'] = epsilon
		args['gamma'] = gamma
		args['alpha'] = alpha
		args['numTraining'] = numTraining
		self.index = 0  # This is always Pacman
		QLearningAgent.__init__(self, **args)

	def getAction(self, state):
		"""
		Simply calls the getAction method of QLearningAgent and then
		informs parent of action for Pacman.  Do not change or remove this
		method.
		"""
		action = QLearningAgent.getAction(self,state)
		self.doAction(state,action)
		return action


class AutoVivification(dict):
		"""Implementation of perl's autovivification feature."""
		def __getitem__(self, item):
				try:
						return dict.__getitem__(self, item)
				except KeyError:
						value = self[item] = type(self)()
						return value