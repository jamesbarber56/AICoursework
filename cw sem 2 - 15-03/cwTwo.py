import random
import csv
import math
import matplotlib.pyplot as plt

stepSizePara = 0.1

def standardiseInputs():
    ''' function to get the data from the file and standardised the predictors
    '''
    #init the min and max, so that the actual ones can be found
    maxT = -9999
    minT = 9999
    maxW = -9999
    minW = 9999
    maxSR = -9999
    minSR = 9999
    maxDSP = -9999
    minDSP = 9999
    maxDRH = -9999
    minDRH = 9999
    maxPanE = -9999
    minPanE = 9999
    
    #init the lines to ignore that have outliers or errors, and what the current row is
    ignoreLines = []
    rowNum = 0
    #rows that will be standardised and used for training
    standardData = []

    #read the datafile, can change the name to do different files
    with open('data sheet.csv', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            add = True
            #change the type to float so can compare
            #if it cannot convert, then the line will be ingored
            #assumed value is not a number
            try:
                row[0] = float(row[0])
                row[1] = float(row[1])
                row[2] = float(row[2])
                row[3] = float(row[3])
                row[4] = float(row[4])
                row[5] = float(row[5])
                
                #testing for outliers that would skew the data
                if (row[0] > 56.7):
                    add = False
                    ignoreLines.append(rowNum)
                elif (row[1] < 0):
                    add = False
                    ignoreLines.append(rowNum)
                elif (row[2] < 0):
                    add = False
                    ignoreLines.append(rowNum)
                elif (row[3] < 90):
                    add = False
                    ignoreLines.append(rowNum)
                elif (row[4] < 0):
                    add = False
                    ignoreLines.append(rowNum)
                elif (row[5] < 0):
                    add = False
                    ignoreLines.append(rowNum)
                else:
                    #find min/max of each predictor
                    if row[0] > maxT:
                        maxT = row[0]
                    if row[0] < minT:
                        minT = row[0]
                        
                    if row[1] > maxW:
                        maxW = row[1]
                    if row[1] < minW:
                        minW = row[1]

                    if row[2] > maxSR:
                        maxSR = row[2]
                    if row[2] < minSR:
                        minSR = row[2]

                    if row[3] > maxDSP:
                        maxDSP = row[3]
                    if row[3] < minDSP:
                        minDSP = row[3]
                        
                    if row[4] > maxDRH:
                        maxDRH = row[4]
                    if row[4] < minDRH:
                        minDRH = row[4]

                    if row[5] > maxPanE:
                        maxPanE = row[5]
                    if row[5] < minPanE:
                        minPanE = row[5]
            except:
                add = False
                ignoreLines.append(rowNum)

            #increase row number
            
            rowNum = rowNum + 1
            if add:
                standardData.append(row)
        
    csvfile.close()        
    print( maxT,minT,'\n',maxW,minW,'\n',maxSR,minSR,'\n',maxDSP,minDSP,'\n',maxDRH,minDRH,'\n',maxPanE,minPanE)

    #standardise all the data [0, 1]
    for row in standardData:
        row[0] = (row[0] - minT) / (maxT - minT)
        row[1] = (row[1] - minW) / (maxW - minW)
        row[2] = (row[2] - minSR) / (maxSR - minSR)
        row[3] = (row[3] - minDSP) / (maxDSP - minDSP)
        row[4] = (row[4] - minDRH) / (maxDRH - minDRH)
        row[5] = (row[5] - minPanE) / (maxPanE - minPanE)
        #print(row)

    #add to write to file to save results - if error occurs, results can be saved and continued
    return standardData, maxPanE, minPanE

    
    
class startingNode():
    iden = 0
    output = None
    def __init__(self, id, inputVal):
        self.iden = id
        self.output = inputVal

class edge():
    iden = 0
    startNode = None
    endNode = None
    weight = None
    prevWeight = None
    def __init__(self, id, startNode, endNode, weight):
        self.iden = id
        self.startNode = startNode
        self.endNode = endNode
        self.weight = weight
        self.prevWeight = weight

class hiddenNode():
    iden = 0
    bias = None
    prevBias = None
    weightedSum = 0
    deltaValue = 0
    output = None
    def __init__(self, id, hdBias):
        self.iden = id
        self.bias = hdBias
        self.prevBias = hdBias

class endNode():
    iden = 0
    weightedSum = 0
    bias = None
    prevBias = None
    deltaValue = 0
    output = None
    correct = 1
    prevError = None
    def __init__(self, id, eBias):
        self.iden = id
        self.bias = eBias
        self.prevBias = eBias

class graph():
    predictedValues = []
    actualValues = []

    errorValue = []
    epoch = []
    
    def __init__(self):
        pass

    def addPAValues(self, predicted, actual):
        self.predictedValues.append(predicted)
        self.actualValues.append(actual)

    def plotAndShowPA(self):
        #plt.scatter(self.predictedValues, self.actualValues)
        #plt.xlabel("Predicted")
        #plt.ylabel("Actual")
        #plt.show()
        pass

    def addErrorValues(self, error, currentEpoch):
        self.errorValue.append(error)
        self.epoch.append(currentEpoch)

    def plotAndShowError(self):
        plt.plot(self.epoch, self.errorValue)
        plt.xlabel("Epoch")
        plt.ylabel("Error Value")
        plt.show()
        pass

def initiliseNodes(startNodes, hidNodes):
    ''' initilises the nodes, depending on the ammount of start and end nodes you want
    '''
    randomRange = [-2/startNodes, 2/startNodes] #random range, depends on the ammount of input nodes
    nextID = 1 #start id
    startingNodes = [] #list storing the starting nodes
    hiddenNodes = [] #list storing the hidden nodes
    edges = [] #list storing the edges
    eNode = None #the single end node
    #----initilise the startingNodes
    for i in range(startNodes):
        startingNodes.append(startingNode(nextID, 0))
        nextID = nextID + 1

    ##----initilise the hidden nodes
    for x in range(hidNodes):
        
        #randomise the bais
        hidBias = random.uniform(randomRange[0],randomRange[1])
        hiddenNodes.append(hiddenNode(nextID, hidBias))
        nextID = nextID +1
    
    ##----initilise the end node
    
    #randomise the bias
    endBias = random.uniform(randomRange[0],randomRange[1])
    eNode = endNode(nextID, endBias)
    nextID = nextID + 1

    ##----init all edges between each

    #cycle through each hidden node to add edges
    for hNode in hiddenNodes:
        #add edge for each starting node - hidden node pair
        for startNode in startingNodes:
            #random weight in range
            weight = random.uniform(randomRange[0],randomRange[1]) #randomise weight
            edges.append(edge(nextID, startNode, hNode, weight))
            nextID = nextID + 1
        #add edge for each hidden node - end node pair
        weight = random.uniform(randomRange[0],randomRange[1]) #randomise weight
        edges.append(edge(nextID, hNode, eNode, weight))
        nextID = nextID + 1

        
    nodes = [startingNodes, hiddenNodes, edges, eNode]
    printNodes(nodes)
    return nodes
            

#main function that wil run the algorithm    
def main(hiddenNodes, momentum=0, boldDriver=0, anneal=0):
    '''main function that will set up, and then run the algorithm
    '''
    predictants, maxPanE, minPanE = standardiseInputs()
    graphs = graph()
    stepSize = 0.1
    epochsLeft = 100 #chose how many epochs
    epochs = epochsLeft
    startingNodes = len(predictants[0]) - 1 #gets ammount of predictants
    #init nodes depending on how many predictants and hidden nodes
    nodes = initiliseNodes(startingNodes, hiddenNodes)
    while epochsLeft != 0:    
        #loop for each training example in data sheet file
        for row in predictants:
            #print(i)
            
            T = float(row[0]) #mean daily temperature (*C)
            W = float(row[1]) #wind speed (mph)
            SR = float(row[2]) #solar radiation (Langleys)
            DSP = float(row[3]) #air pressure (kPa)
            DRH = float(row[4]) #humidity (%)
            correctOutput = float(row[5]) #Pan evap (mm/day)

            changePredictants([T,W,SR,DSP,DRH],correctOutput,nodes)
            forwardPass(nodes) #forward pass of the nodes
            backwardPass(nodes) #backward pass through the nodes
            updateWeights(nodes, momentum, stepSizePara=stepSize) #update the weights and bias'
            #adding values to the graph
            #change values back into non-standardised data and add them into the data set for the graph
            graphs.addPAValues(((nodes[3].output * (maxPanE - minPanE)) + minPanE), ((correctOutput* (maxPanE - minPanE)) + minPanE))
        #add error value and epochs into the graph data set
        graphs.addErrorValues(nodes[3].output - nodes[3].correct, epochs - epochsLeft)

        #bold driver improvement
        if boldDriver == 1:
            if nodes[3].prevError != None:
                error = nodes[3].output - nodes[3].correct
                #print(error, nodes[3].prevError)
                if abs(error) > abs(nodes[3].prevError):
                    if stepSize > 0.01:
                        stepSize = stepSize * 0.5
                elif abs(error) < abs(nodes[3].prevError):
                    if stepSize < 0.5:
                        stepSize = stepSize * 1.1
                #print(stepSize)
            nodes[3].prevError = nodes[3].output - nodes[3].correct

        #annealing improvement
        if anneal == 1:
            startStepSize = 0.1
            endStepSize = 0.01
            #print(epochs, epochs-epochsLeft)
            stepSize = endStepSize + (startStepSize - endStepSize)
            stepSize = stepSize  * ( 1 - ( 1 / ( 1 + (math.e ** ( 10 - ((20 * (epochs - epochsLeft)) / epochs))))))
            #print(stepSize)
        epochsLeft = epochsLeft - 1
    
    printNodes(nodes)

    #show graphs
    graphs.plotAndShowPA()
    graphs.plotAndShowError()

def changePredictants(inputs,correct,nodes):
    for i in range(len(inputs)):
        #print(inputs[i])
        nodes[0][i].output = inputs[i]
    nodes[3].correct = correct
    #printNodes(nodes)
    

def forwardPass(nodes):
    '''forwars pass through the network, calculating the wighted sum and the outputs of each node'''
    #startingNode : hiddenNodes : edges : endNode
    for hiddenNode in nodes[1]+[nodes[3]]: #cycle through the hidden and end nodes
        inputs = []
        for edge in nodes[2]: ##get all edges that input the node
            if edge.endNode == hiddenNode:
                inputs.append(edge)
        hiddenNode.weightedSum = computeWeightedSum(inputs, hiddenNode) #calculate weighted sum
        hiddenNode.output = activation(hiddenNode.weightedSum, 0) #calculate the output
    
    #printNodes(nodes)
    return nodes

def backwardPass(nodes):
    '''algorithm for the backward pass through the network'''
    fSend = nodes[3].output * (1 - nodes[3].output) #calculates the end node f'(S) function
    nodes[3].deltaValue = (nodes[3].correct - nodes[3].output) * fSend #calculates the end node delta value
    #print("endNode dV: ", nodes[3].deltaValue)

    for hiddenNode in nodes[1]: #cycles through all the hidden nodes to get delta values
        fS = hiddenNode.output * (1 - hiddenNode.output) #f'(S) of the current hidden node
        for edge in nodes[2]: 
            if edge.startNode == hiddenNode and edge.endNode == nodes[3]: #get the edge: hidden -> end
                hiddenNode.deltaValue = edge.weight * nodes[3].deltaValue * fS #calculate delta value
                #print("deltaValue: ", edge.startNode.iden, edge.endNode.iden, hiddenNode.deltaValue)
    return nodes

def updateWeights(nodes, momentum=0, stepSizePara=0.1):
    '''updates all the weights/bias' after calculating the delta values form the backward pass'''
    for edge in nodes[2]: ##changes all weights of all edges
        edge.prevWeight = edge.weight
        if momentum == 1: #improvement, momentum added
            edge.weight = edge.weight + stepSizePara * edge.startNode.output * edge.endNode.deltaValue + (0.9 * (edge.weight - edge.prevWeight))
        else:
            edge.weight = edge.weight + stepSizePara * edge.startNode.output * edge.endNode.deltaValue
    for node in nodes[1]+[nodes[3]]: ##changes bias of all hidden nodes and the end node
        node.prevBias = node.bias
        if momentum == 1: # improvemtne, momentum added
            node.bias = node.bias + stepSizePara * node.deltaValue * 1 + (0.9 * (node.bias - node.prevBias))
        else:
            node.bias = node.bias + stepSizePara * node.deltaValue * 1

    #printNodes(nodes)
    #print(end="")
    return nodes

def computeWeightedSum(inputs, node):
    '''computes the weights, given the inputs and the node
    '''
    total = 0
    for inp in inputs:
        total = total + inp.weight * inp.startNode.output #calculates the total weighted sum from the inputs
    total = total + node.bias
    return total

def activation(S, n):
    '''has the activation fuinctions, can change between to see the difference
    '''
    #sigmoid (0) or tanh (1)
    if n == 0:
        result = 1 / ( 1 + math.e**(S*-1)) #sigmoid function
    elif n == 2:
        result = (math.e**S - math.e**(S*-1)) / (math.e**S - math.e**(S*-1)) #tanh function
    return result

    
def printNodes(nodes):
    '''overview of the network, showing id, bias, output (weight for edges)
    '''
    print("\n---Starting nodes---") #prints start nodes and their output
    for x in nodes[0]:
        print(x.iden, " - ", x.output)

    print("\n---Hidden Nodes---") #prints hidden nodes, their bias and output
    for x in nodes[1]:
        print(x.iden, " - ", x.bias, " - ", x.output)   

    print("\n---End Node---") #prints the end node, its bias and output
    print(nodes[3].iden, "-", nodes[3].bias, " - ", nodes[3].output, " - ", nodes[3].correct)

    print("\n--Edges--") #print all the edges, their start and end node id, and their weight
    for x in nodes[2]:
        print(x.startNode.iden, " -- ", x.endNode.iden, " - ", x.weight)
