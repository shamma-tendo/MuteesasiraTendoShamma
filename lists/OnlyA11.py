animals = ['cow','pig','sheep','monkey','hen','dog','lion','zebra','duck','giraffe','koala']
#print only those with 'a' in them
#option1
with_a = [animal for animal in animals if 'a' in animal]
print(with_a)

#option2
with_a =list(filter(lambda animal: 'a'  in animal, animals))
print(with_a)