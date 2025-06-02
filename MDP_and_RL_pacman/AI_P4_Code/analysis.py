# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0.001 # I reduced it to 0.001
    return answerDiscount, answerNoise

def question3a():
    answerDiscount = 0.31 # dicount^3 > discount^5 * 10 => dicount<0.316
    answerNoise = 0.01 # We need low noise in order lower the risk of getting -10 
    answerLivingReward = 0.0 # Living should not have reward bacause we want to choose the closest terminal
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.31 # dicount^7 > discount^9 * 10 => dicount<=0.316
    answerNoise = 0.2 # We need high noise in order to choose the safe path
    answerLivingReward = 0.0 # Living should not have reward bacause we want to choose the closest terminal
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.4 # dicount^3 < discount^5 * 10 => dicount>0.316
    answerNoise = 0.01 # We need low noise in order lower the risk of getting -10 
    answerLivingReward = 0.2 # We need living reward in order to choose the furthest terminal
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.4 # dicount^3 < discount^5 * 10 => dicount>0.316
    answerNoise = 0.2 # We need high noise in order to choose the safe path
    answerLivingReward = 0.2 # We need living reward in order to choose the furthest terminal
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0.0 # It should be zero in order to neglect the terminals
    answerNoise = 0.5 # Noise does not matter. it can be between 0 and 1
    answerLivingReward = 0.0 # Living reward also does not matter
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE'
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
