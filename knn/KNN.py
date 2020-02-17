import math
import random
import operator

f = open('iris.data', 'r')
data = []
if f.mode == 'r':
    data = f.readlines()


def maybe_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return s


def manhattanDistance(test2, train2, length2):
    manhattan = 0
    for c in range(length2):
        manhattan += abs(test2[c + 1] - train2[c + 1])
    return manhattan


def uclideanDistance(test, train2, length2):
    ucliDistance = 0

    for j in range(length2):
        ucliDistance += pow(abs(test[j + 1] - train2[j + 1]),2)
    return math.sqrt(ucliDistance)


def calcDistance(train, test, randindex, k):
    distance = {0: 0}
    result = {}

    #for abalone.data, range(len(train))
    for i in range(len(train)-1):
        #distance[i] = uclideanDistance(test, train[i], len(test)-1)
        distance[i] = manhattanDistance(test, train[i], len(test) - 1)


    distance = sorted(distance.items(), key=operator.itemgetter(1))

    for count in range(k):
        temp = train[distance[count][0]][0]
        if temp in result.keys():
            result[temp] += distance[count][1]
        else:
            result[temp] = distance[count][1]

    result.update((x, y+0.0000000001) for x, y in result.items())
    result.update((x, 1 / y) for x, y in result.items())
    result = sorted(result, key=result.get, reverse=True)

    if result[0] == test[0]:
        return 1
    else:
        return 0




length = len(data)
tempRandomIndex = random.sample(range(0, length), length)
randomIndex = []

for i in range(10):
    randomIndex.append([])

counter = 0
for i in range(10):
    for j in range(math.ceil(length / 10)):
        randomIndex[i].append(tempRandomIndex[counter])
        counter += 1
        if counter == length:
            break

tempData = [maybe_float(item) for item in data[0].split(',')]
content = {0: tempData}
for i in range(length - 1):
    tempData = [maybe_float(item) for item in data[i + 1].split(',')]
    content[i + 1] = tempData

#this is only for iris dataset
for i in range(len(data)-1):
    content[i][0], content[i][4] = content[i][4], content[i][0]

avg = 0
for i in range(10):
    tempTrainData = content
    testData = {0: []}
    trainData = []

    for j in range(len(content)):
        if j in randomIndex[i]:
            continue
        trainData.append(tempTrainData[j])

    for j in range(len(randomIndex[i])):
        testData[j] = content[randomIndex[i][j]]

    right = 0
    for j in range(len(randomIndex[i])):
        right += calcDistance(trainData, testData[j], randomIndex[i], 5)

    accuracy = (right / len(randomIndex[i]))*100
    #print('accuracy : ',i,' ', accuracy, '%')
    avg += accuracy
print('Final Accuracy: ',avg/10,'%')
