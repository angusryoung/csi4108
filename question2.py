
import numpy as np
from numpy import random

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
        #print(input)
        newHexValue = self.setting[hexValue]
        #print(newHexValue)
        return SBox.hexToBinaryArr(newHexValue)
    
    def sboxEncypt16 (self, input):
        '''input array size 16'''
        newHexValue = []
        partHexValue =[0,0,0,0]
        sum = 0
        for i in range(4):
            for j in range(4):
                partHexValue[j] = input[i*4 + j]
            #sum = SBox.binArrToHex(partHexValue)
            partHexValue = SBox.sboxEncypt(self,partHexValue)
            for k in partHexValue:
                newHexValue.append(k)
                
        return newHexValue
    


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
        sum = 0
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
    #print ("after key xor at round "+str(round_number)+" :" + str(xorResult))
    s1,s2,s3,s4 = convert16x4(xorResult)

    subResult = np.append(sboxobj.sboxEncypt(s1),np.append(sboxobj.sboxEncypt(s2),np.append(sboxobj.sboxEncypt(s3),sboxobj.sboxEncypt(s4))))
    #print ("after sub at round "+str(round_number)+" :" + str(subResult))
    permuteResult = permuteobj.permute(subResult)

    return permuteResult

def lastRound(input,keyobj,sboxobj, round_number):
    xorResult = keyobj.xor_using_key(input,round_number)
    #print ("after key xor at round "+str(round_number)+" :" + str(xorResult))
    s1,s2,s3,s4 = convert16x4(xorResult)
    subResult = np.append(sboxobj.sboxEncypt(s1),np.append(sboxobj.sboxEncypt(s2),np.append(sboxobj.sboxEncypt(s3),sboxobj.sboxEncypt(s4))))
    #print ("after sub at round "+str(round_number)+" :" + str(subResult))
    return subResult


def decimalToBinary(n):
    # converting decimal to binary
    # and removing the prefix(0b)
    return list(map(int,bin(n).replace("0b", "")))

def make10000inputs(deltaP):
    inputList = []
    plaintText1 = []
    plaintText2 = []
    b = 0
    for i in range(5000):#TODO change back to 10 000
        b = random.randint(131071)
        plaintText1 = decimalToBinary(b )
        if (len(plaintText1) < 16):
            plaintText1 = np.concatenate((np.array([0]*(16-len(plaintText1))),np.array(plaintText1)))
        plaintText2 = xor16(deltaP, plaintText1)
        inputList.append((plaintText1,plaintText2))
    
    return inputList

def xor2(num1,num2):
        if (num1 == num2):
            return 0
        else:
            return 1

def xor16(num1,num2):
    a = []
    for i in range(16):
        a.append(xor2(int(num1[i]),int(num2[i])))
    return a

                
            

def mask(m16,input):
    '''input and mask is a 16 digit return the and of the two'''
    maskResult = []
    for i in range(16):
        maskResult.append( m16[i] and input[i])
    return maskResult

def keyCreate(start1,start2):
    '''the 2 starting index of where you can about the 4 bits of key parts
    for example 4,12'''
    keyDict = {}
    base = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(16):
        for j in range(16):
            insertArray1 = SBox.hexToBinaryArr(i)
            insertArray2 = SBox.hexToBinaryArr(j)
            for k in range(4):
                base[start1 +k] = insertArray1[k]
                base[start2 +k] = insertArray2[k]
            keyDict[''.join(str(e) for e in base)] = 0
            # print(str(i) + " "+ str(j))
    #print (keyDict)
    return keyDict



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
    sBoxDictionary = {}
    randomArray = [ 1,  3, 13, 14,  6, 10,  2, 15,  8, 11,  4,  7,  9,  0,  5, 12]#[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]#np.arange(16)
    #np.random.shuffle(randomArray)
    print("sBox mapping: "+str(randomArray))

    for i in range(16):
        sBoxDictionary[i]= randomArray[i]
    
    #declare all the objects here
    sbox1 = SBox(randomArray)
    changingKey = np.arange(16)
    listOfKeys = [[0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],[1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0],
                  [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0],[1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0]]

    lastRoundKey = [1,1,1,1,0,0,1,0,1,1,0,0,0,1,0,1]
    listOfKeys.append(lastRoundKey)
    
    key1 = Key(listOfKeys)
    #Perm1 = Permutation(np.arange(16))
    Perm1 = Permutation([0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15])
    #print([np.array([1]*16),np.array([1]*16),np.array([1]*16),np.array([1]*16),np.array([1]*16)])


    
    # tempinput =[0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]

    # round1 = round(tempinput, key1,sbox1,Perm1,0)
    # print('round1 ' +str(round1))
    # round2 = round(round1,key1,sbox1,Perm1,1)
    # print('round2 ' +str(round2))
    # round3 = round(round2,key1,sbox1,Perm1,2)
    # print('round3 ' +str(round3))
    # round4 = lastRound(round3,key1,sbox1,3)
    # print('round4 ' +str(round4))
    # round5 = key1.xor_using_key(round4,4)
    # print('round5 ' +str(round5))
    
    
    deltaP = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
    
    input10000 = make10000inputs(deltaP)
    count = 0
    idealresult = [0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0]
    subkey = keyCreate(8,12)
    for j in range(15):
        for i in input10000:
            
            plainText1 = i[0]
            plainText2 = i[1]
            
            # print('plainText1 : ' + str(plainText1))
            # print('plainText2 : ' + str(plainText2))
            
            round1 = round(plainText1, key1,sbox1,Perm1,0)
            round2 = round(round1,key1,sbox1,Perm1,1)
            round3 = round(round2,key1,sbox1,Perm1,2)
            round4 = lastRound(round3,key1,sbox1,3)
            cipherText1 = key1.xor_using_key(round4,4)
            # print('ctext1 : ' + str(cipherText1))
            
            round1 = round(plainText2, key1,sbox1,Perm1,0)
            round2 = round(round1,key1,sbox1,Perm1,1)
            round3 = round(round2,key1,sbox1,Perm1,2)
            round4 = lastRound(round3,key1,sbox1,3)
            cipherText2 = key1.xor_using_key(round4,4)
            # print('ctext2 : ' + str(cipherText2))
            
            deltaCipher = xor16(cipherText1,cipherText2)
            #print('deltaCipher : ' + str(deltaCipher))
            
            
            
            if (deltaCipher[0:4]==[0,0,0,0] and deltaCipher[4:8]==[0,0,0,0]):


            # maskeddeltaCipher = mask(resultmask,deltaCipher)
            # strmaskedRound5 = ''.join(str(e) for e in maskeddeltaCipher)
            
        
                for j in subkey:
                    # z = xor16(strmaskedRound5 ,j)
                    # if z == idealresult :
                    if xor16(deltaCipher,j) == idealresult :

                    
                        # print("xor results"+str(z))
                        # print("key :" +j)
                        # print("round 5: " + str(maskedRound5))
                        # print("what is should be" +str(idealresult))
                        count +=1
                    
                        subkey[j]+=1
                
        #print("result for input " +str(i)+" is"+ str(round5))
    
    print(count)
    for b in subkey:
        subkey[b]= subkey[b] /count
        print("key: " + b + "  count: " + str(subkey[b]))


    

if __name__ == "__main__":
    main()



