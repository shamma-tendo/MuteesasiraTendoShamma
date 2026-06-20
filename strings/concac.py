age = 4
name = "bob"
# Concatenate using f-string (recommended)
result = f"{name} is {age} years old"
print(result)

# Alternative using str() conversion
result2 = name + " is " + str(age) + " years old"
print(result2)