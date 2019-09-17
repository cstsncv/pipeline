
a = [1,2,3,4,5,6]
b = [2,4,6,9]

# while True:
for i, v in enumerate(a):
    for h in b:
        if v == h:
            print("break   ===={}".format(h))
            break
    else:
        print(v)
















