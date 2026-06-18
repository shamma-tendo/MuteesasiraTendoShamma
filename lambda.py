
# List of strings
fruits = ["cherry", "banana",  "date", "apple","mango","dragonfruit"]

# Sort by length of each word (ascending order)
sorted_fruits = sorted(fruits, key=lambda x: len(x))
print(sorted_fruits)  

#sorted by length in descending order
sorted_fruits = sorted(fruits, key=lambda x: len(x), reverse= True)
print(sorted_fruits)  