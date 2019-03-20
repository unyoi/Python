import sys

#print(sys.path)

# a = sys.path
# print(a)

# print(sys)

#print(path)

# list=[]
#
# for idx in sys.path:
#     list.append(idx)


#print("{0:-^10}".format("hello"))

#### Test find index of string value ####
a = "chulchul"
value = "ung"

def findString():
    return a.find(value)

if findString() > -1:
    print("We found {value} in {chul}".format(value=value,chul=a))
else:
    print("We can't found {value} in {chul} ".format(value=value,chul=a))

#print(findString())




