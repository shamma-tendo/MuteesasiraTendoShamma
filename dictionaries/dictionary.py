shoes={
    "brand" : "nick",
    "color" : "black",
    "size" : 40
}

#print value of shoe size
print(shoes["size"])
#change value of nick to adidas
shoes["brand"] = "adidas"
print(shoes)
#add value type"sneakers"
shoes["type"] = "sneakers"
print(shoes)
#return list of all keys in the dictionary
list(shoes.keys())
print(shoes)
#return a list of all values in the dictionary
list(shoes.values())
print(shoes)
#check if size exists
print("size" in shoes)
#loop through the dictionary
for key, value in shoes.items():
    print(key, value)

#remove "color"
del shoes["color"]
#empty dictionary
shoes.clear()
