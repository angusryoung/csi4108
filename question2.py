
import numpy as np

#use this to create the dictionary
#arr = np.arange(10)
#np.random.shuffle(arr)'

#use this when appending arrays
#res = np.append(x, y)

class SBox:
    def __init__(self,setting):
        #assuming same permutation each time
        self.setting = setting #setting is a dictionary

    def sboxEncypt (self,input):
        #input is a list size 4 of 0s or 1s
        #setting is a dictonary
        #input as hex
        hexValue = SBox.binArrToHex(input)
        newHexValue = self.setting[hexValue]
        
        return SBox.hexToBinaryArr(newHexValue)
    


    def hexToBinaryArr(input):
        if (input == 0):
            return [0,0,0,0]
        if (input == 1):
            return [0,0,0,1]
        if (input == 2):
            return [0,0,1,0]
        if (input == 3):
            return [0,0,1,1]
        if (input == 4):
            return [0,1,0,0]
        if (input == 5):
            return [0,1,0,1]
        if (input == 6):
            return [0,1,1,0]
        if (input == 7):
            return [0,1,1,1]
        if (input == 8):
            return [1,0,0,0]
        if (input == 9):
            return [1,0,0,1]
        if (input == 10):
            return [1,0,1,0]
        if (input == 11):
            return [1,0,1,1]
        if (input == 12):
            return [1,1,0,0]
        if (input == 13):
            return [1,1,0,1]
        if (input == 14):
            return [1,1,1,0]
        if (input == 15):
            return [1,1,1,1]
        else:
            print ("something went wrong when converting"+str(input))
            return -1

    def binArrToHex(input):
        sum = 0;
        sum += input[0] * pow(2,3)
        sum += input[1] * pow(2,2)
        sum += input[2] * pow(2,1)
        sum += input[3]
        return sum

class Permutation:
    def __init__(self,per_map):
        self.permap = per_map #permap is an array size 16

    def permute(self,input):
        newArray = np.array([-1]*16)
        for i in range(16):
            newArray[i] = input[self.permap[i]]
        return newArray

class Key:
    def __init__(self,roundKeys):
        #an array of 5 16 bit keys
        self.roundKeys = roundKeys
    
    def xor_using_key(self,input,round):
        currentRound = self.roundKeys[round]
        newArray = np.array([-1]*16)
        for i in range(16):
            newArray[i] = Key.xor(input[i],currentRound[i])
        return newArray

    def xor(num1,num2):
        if (num1 == num2):
            return 0
        else:
            return 1
    
def convert16x4(input):
    return input[0:4],input[4:8],input[8:12],input[12:16]
    
def convert4x16(input):
    return np.append(input[0],input[1],input[2],input[3])

def round (input,keyobj,sboxobj,permuteobj, round_number):
    xorResult = keyobj.xor_using_key(input,round_number)
    s1,s2,s3,s4 = convert16x4(xorResult)

    subResult = np.append(sboxobj.sboxEncypt(s1),np.append(sboxobj.sboxEncypt(s2),np.append(sboxobj.sboxEncypt(s3),sboxobj.sboxEncypt(s4))))
    permuteResult = permuteobj.permute(subResult)

    return permuteResult

def decimalToBinary(n):
    # converting decimal to binary
    # and removing the prefix(0b)
    return list(map(int,bin(n).replace("0b", "")))

def make10000inputs():
    inputList = []
    for i in range(10000):
        inputList.append(decimalToBinary(i))
    return inputList



def main():
    '''
    input = [1,0,1,1]
    sBoxDictionary = {}
    randomArray = np.arange(16)
    np.random.shuffle(randomArray)
    print("sBox mapping:")
    print(randomArray)

    for i in range(16):
        sBoxDictionary[i]= randomArray[i]
    
    sbox1 = SBox(randomArray,randomArray)

    result = sbox1.sboxEncypt(input)
    print(result)
    '''
    input = [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1]
    sBoxDictionary = {}
    randomArray = np.arange(16)
    np.random.shuffle(randomArray)
    print("sBox mapping:"+str(randomArray))

    for i in range(16):
        sBoxDictionary[i]= randomArray[i]
    
    #declare all the objects here
    sbox1 = SBox(randomArray)
    key1 = Key([np.array([1]*16),np.array([-1]*16),np.array([-1]*16)])
    Perm1 = Permutation(np.arange(16))


    


    roundResult = round(input, key1,sbox1,Perm1,0)
    print("result after round 1" + str(roundResult))

    

if __name__ == "__main__":
    main()



