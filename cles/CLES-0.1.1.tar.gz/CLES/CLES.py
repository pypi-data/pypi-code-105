def CLES_2independent(data1, data2):
    '''
    Calculate common language effect size (2 samples)

    INPUTS:
    data1/2: data set, np.array

    OUTPUT:
    thetaHat: common language effect size (50 - 100)
    '''
    import numpy 
    total = 0
    for d1 in data1:
        for d2 in data2:
            if d1 > d2: 
                total += 1
            elif d1 == d2: 
                total += 0.5
    thetaHat = (numpy.abs(total / (len(data1) * len(data2)) - 0.5) + 0.5) * 100
    return thetaHat 

def CLES_2paired(data1, data2):
    '''
    Calculate common language effect size (paired samples)

    INPUTS:
    data1/2: data set, np.array

    OUTPUT:
    thetaHat: common language effect size (50 - 100)
    '''
    import numpy 
    D = data1 - data2
    comp = numpy.zeros((len(D)-1))
    total = 0
    for d1 in D:
        for d2 in comp:
            if d1 > d2: 
                total += 1
            elif d1 == d2: 
                total += 0.5
    thetaHat = (numpy.abs(total / (len(data1) * len(data2)) - 0.5) + 0.5) * 100
    return thetaHat 

def CLES_1samp(data, mu=0):
    '''
    Calculate common language effect size (1 sample)

    INPUTS:
    data: data vector 
    mu: mean to compare, default=0

    OUTPUT:
    thetaHat: common language effect size (50 - 100)
    '''
    import numpy 
    comp = numpy.repeat(mu, len(data)) # mean value to compare 
    total = 0
    for d1 in data:
        for d2 in comp:
            if d1 > d2: 
                total += 1
            elif d1 == d2: 
                total += 0.5
    thetaHat = (numpy.abs(total / (len(data) * len(comp)) - 0.5) + 0.5) * 100
    return thetaHat