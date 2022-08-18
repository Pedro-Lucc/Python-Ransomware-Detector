def calcP(directory_count, counter, porcentage):
    v1 = directory_count  # 500
    v2 = 100  # 100%
    v3 = counter  # ?
    v4 = porcentage * 100  # 20%
    return v3 * v2 / v1


counter = 0
directory_count = 7
porcentage = 0.1
while counter < directory_count:
    for i in range(directory_count):
        if counter == directory_count:
            break
        counter = round(counter + 0.01, 2)
        print(counter)
        print(round(directory_count * porcentage, 2))
        if counter == round(directory_count * porcentage, 2):
            print(f"{calcP(directory_count, counter, porcentage)}%")
            porcentage = porcentage + 0.1
