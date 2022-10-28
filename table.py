from re import A
import numpy as np


def xor(num1,num2):
    if (num1 == num2):
        return 0
    else:
        return 1
        
def xor4x4(num1, num2):
    '''both inputs are array len of 4 containing 1s or 0s
    return the xor of the array'''
    return [xor(num1[0],num2[0]),xor(num1[1],num2[1]),xor(num1[2],num2[2]),xor(num1[3],num2[3])]

def decimalToBinary(n):
    # converting decimal to binary
    # and removing the prefix(0b)
    bArray = list(map(int,bin(n).replace("0b", "")))
    while (len(bArray) <4):
        bArray.insert(0,0)
    return bArray

def binArrToHex(input):#should be called binArrToDec but whatever
        sum = 0;
        sum += input[0] * pow(2,3)
        sum += input[1] * pow(2,2)
        sum += input[2] * pow(2,1)
        sum += input[3]
        return sum

#table 6

def table6columns(sbox,xdelta):
    '''given S box dictionary and x delta find y delta'''
    xDeltaArray = decimalToBinary(xdelta)
    yDeltaArray = []
    for i in range(16):
        input1 = decimalToBinary(i)
        input2 = xor4x4(input1,xDeltaArray)
        output1 = decimalToBinary(sbox[i])
        output2 =decimalToBinary(sbox[binArrToHex(input2)])
        outputDelta = binArrToHex( xor4x4(output1,output2))
        yDeltaArray.append(outputDelta)
        
    return yDeltaArray

def table7rows(yDeltaArray):
    newArray = np.array([0]*16)
    for i in yDeltaArray:
        newArray[i] += 1
    return newArray

def table7(sbox):
    tableArray = [] #going to be a 2d array
    for x in range(16):
        #go through x delta
        #xBinArray = decimalToBinary(x)
        yDeltaArray = table6columns(sbox,x)
        tableArray.append(table7rows(yDeltaArray))
    return tableArray


def printTable7(table7):
    for i in table7:
        print(i)



sBoxDictionary = {}
randomArray = np.arange(16)#instead of random array we will have s-boc mapping
np.random.shuffle(randomArray)
for i in range(16):
    sBoxDictionary[i]= randomArray[i]
    

def main():
    a = np.arange(16)
    np.random.shuffle(a)
    sArray = a
    print(a)
    #[12 11  4  7  9  6  8 13 14  1 10  2  3  5 15  0]
    #sArray = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
    #sArray = [12, 6, 4, 9, 13, 14, 1, 2, 0, 10, 3, 8, 7, 11, 5, 15]
    #sArray = [ 1,  4, 10,  8, 14,  0,  2,  9,  5, 15,  3, 11, 12,  6,  7, 13]
    sDict = {}
    for i in range(16):
        sDict[i]= sArray[i]
    
    table = table7(sDict)
    printTable7(table)
    
    

if __name__ == "__main__":
    main()