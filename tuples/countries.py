#using tuple constructor
c= ["Kampala", "Gulu", "Mukono", "Mbarara", "Lira"]
x = tuple(c)
print(x)

# Unpacking in for loops
students = [("Jane", 25), ("Daniel", 30), ("Charlie", 35)]

for name, age in students:
    print(f"{name} is {age} years old")

#using range of indexes to print 2nd, 3rd, and 4th cities
y= x[1:4]
print(y)