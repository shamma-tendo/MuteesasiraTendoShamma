# Set of 4 items and list of 2 items, add list elements to set
my_set = {"apple", "banana", "cherry", "date"}
my_list = ["grape", "kiwi"]

# Add elements from list to set
my_set.update(my_list)
print(my_set)  # {'apple', 'banana', 'cherry', 'date', 'grape', 'kiwi'}




# Two sets - ages and first names, join them
ages = {25, 30, 22, 28}
first_names = {"John", "Emma", "Michael", "Sophia"}

# Join the two sets using union()
combined = ages.union(first_names)
# OR using | operator
# combined = ages | first_names
print(combined)  # {25, 30, 22, 28, 'John', 'Emma', 'Michael', 'Sophia'}

