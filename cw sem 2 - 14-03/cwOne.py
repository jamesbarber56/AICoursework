import random
import csv
import math
import re

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
            
    print( maxT,minT,'\n',maxW,minW,'\n',maxSR,minSR,'\n',maxDSP,minDSP,'\n',maxDRH,minDRH,'\n',maxPanE,minPanE)

    #standardise all the data [0, 1]
    for row in standardData:
        row[0] = (row[0] - minT) / (maxT - minT)
        row[1] = (row[1] - minW) / (maxW - minW)
        row[2] = (row[2] - minSR) / (maxSR - minSR)
        row[3] = (row[3] - minDSP) / (maxDSP - minDSP)
        row[4] = (row[4] - minDRH) / (maxDRH - minDRH)
        row[5] = (row[5] - minPanE) / (maxPanE - minPanE)
        print(row)

    #add to write to file to save results - if error occurs, results can be saved and continued
    

    
    
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
    def __init__(self, id, startNode, endNode, weight):
        self.iden = id
        self.startNode = startNode
        self.endNode = endNode
        self.weight = weight

class hiddenNode():
    iden = 0
    bias = None
    weightedSum = 0
    output = None
    
    def __init__(self, id, hdBias):
        self.iden = id
        self.bias = hdBias

class endNode():
    iden = 0
    weightedSum = 0
    output = None
    correct = 1
    def __init__(self, id, eBias):
        self.iden = id
        self.bias = eBias
    

def initiliseNodes(inputValues, hidNodes=2):
    ''' initilises the nodes, depending on the ammount given in the input
    '''
    nextID = 0
    startingNodes = []
    hiddenNodes = []
    edges = []
    eNode = None
        
    #elif ---test if all inputvalues can be floats
    
    for inputval in inputValues:
        startingNodes.append(startingNode(nextID, inputval))
        nextID = nextID + 1

    ##----initilise the hidden nodes
    for x in range(hidNodes):
        
        #randomise the bais
        hidBias = [1,-6]
        
        hiddenNodes.append(hiddenNode(nextID, hidBias[x]))
        nextID = nextID +1
    

    ##----initilise the end node
    
    #randomise the bias
    endBias = -3.92
    eNode = endNode(nextID, endBias)
    nextID = nextID + 1

    ##----init all edges between each
    
    #id each with a different id
    nextWeight = 0

    #cycle through each hidden node to add edges
    for hNode in hiddenNodes:
        
        #randomise weights
        weights = [3,4,2,6,5,4]

        #add edge for each starting node - hidden node pair
        for startNode in startingNodes:
            edges.append(edge(nextID, startNode, hNode, weights[nextWeight]))
            nextID = nextID + 1
            nextWeight = nextWeight+  1
        #add edge for each hidden node - end node pair
        edges.append(edge(nextID, hNode, eNode, weights[nextWeight]))
        nextID = nextID + 1
        nextWeight = nextWeight + 1

        
    nodes = [startingNodes, hiddenNodes, edges, eNode]
    printNodes(nodes)
    return nodes
            

#main function that wil run the algorithm    
def main(stepSize, standardisedInputs, nodes):

    #initlise nodes, change input for a differnet network
    nodes = initiliseNodes([1,0])
    
    #loop for each training example in data sheet file
    for row in standardisedInputs:
        T = float(row[0]) #mean daily temperature (*C)
        W = float(row[1]) #wind speed (mph)
        SR = float(row[2]) #solar radiation (Langleys)
        DSP = float(row[3]) #air pressure (kPa)
        DRH = float(row[4]) #humidity (%)
        correctOutput = float(row[5]) #Pan evap (mm/day)

        

def fowardPass(nodes):
    #startingNode : hiddenNodes : edges : endNode
    for hiddenNode in nodes[1]+[nodes[3]]:
        inputs = []
        for edge in nodes[2]:
            if edge.endNode == hiddenNode:
                inputs.append(edge)
        hiddenNode.weightedSum = computeWeightedSum(inputs, hiddenNode)
        hiddenNode.output = activation(hiddenNode.weightedSum, 0)
    

    printNodes(nodes)



def computeWeightedSum(inputs, node):
    '''computes the weights, given the inputs and the node
    '''
    total = 0
    for inp in inputs:
        total = total + inp.weight * inp.startNode.output
    total = total + node.bias
    return total
    


def activation(S, n):
    '''has the activation fuinctions, can change between to see the difference
    '''
    print(S)
    #sigmoid (0) or tanh (1)
    if n == 0:
        result = 1 / ( 1 + math.e**(S*-1))
    elif n == 2:
        result = (math.e**S - math.e**(S*-1)) / (math.e**S - math.e**(-S))

    return result

    
def printNodes(nodes):
    '''overview of the network, showing id, bias, output (weight for edges)
    '''
    print("---Starting nodes---")
    for x in nodes[0]:
        print(x.iden, " - ", x.output)

    print("\n---Hidden Nodes---")
    for x in nodes[1]:
        print(x.iden, " - ", x.bias, " - ", x.output)   

    print("\n---End Node---")
    print(nodes[3].iden, "-", nodes[3].bias, " - ", nodes[3].output)

    print("\n--Edges--")
    for x in nodes[2]:
        print(x.startNode.iden, " -- ", x.endNode.iden, " - ", x.weight)
