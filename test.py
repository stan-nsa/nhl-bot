list1 = [1, 2, 3, 4, 5]
string1 = "My name is AskPython"
tuple1 = (11, 22, 33, 44)
list_tuple = [('1',), ('22',), ('30',), ('4',), ('53',), ('54',), ('55',)]
tst = {'id' : '51'}

print(5 in list1)  # True
print("is" in string1)  # True
print(11 in tuple1)  # False
print((tst['id'],) in list_tuple)  # False

