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
#addint item to tuple
x = x + ("huawei",)
print(x)
#delete 1st item from tuple
x = x[:1] + x[2:5]
print(x)
