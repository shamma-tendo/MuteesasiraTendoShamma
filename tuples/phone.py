x = ("samsung", "iphone", "tecno", "redmi")
#print my favourite phone
print(x[-1])
#print 2nd last item from the tuple
print(x[-2])
#update an item in a tuple
phonelist = list(x)
phonelist[1] = "itel" 
x = tuple(phonelist)
print(x)