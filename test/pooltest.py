from multiprocessing import*

def doubler(number, gop):
    return [number * gop]


def poolTest(searchTag):
    numbers = [5,10,20]
    gop = [2,3,4]
    arg = [(numbers[0], gop[0]),(numbers[1], gop[1]),(numbers[2], gop[2])]
    pool = Pool(processes=3)
    result = pool.starmap(doubler, arg)
    print(result)
    print(result[0][0])

if __name__ == "__main__":
    poolTest('도둑')