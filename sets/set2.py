mySet = {"oven", "kettle", "microwave", "refrigerator"}
if "microwave" in mySet:
    print("microwave present")
else:
    print("microwave not present")

#method 2
print("microwave" in mySet)

#remove item
mySet.remove("kettle")
print(mySet)

#loop through the set
mySet = {"oven", "kettle", "microwave" ,"refrigerator"}
for item in mySet:
    print(item)
