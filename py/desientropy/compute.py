import numpy as np

def entropy_1d(x):
    n_steps = len(x) - 3
    proba = {}
    for i in range(n_steps):
        d = x[i:i+4]
        l = list(np.argsort(d))
        l = ''.join(str(e) for e in l)
        try:
            proba[l] += 1
        except:
            proba[l] = 1
    p = np.array(list(proba.values()))
    p = p/p.sum()
    h = np.sum(-p*np.log2(p))/np.log2(24)
    return h

def entropy_2d(x):
    n_steps_x = np.shape(x)[0] - 3
    n_steps_y = np.shape(x)[1] - 3
    proba = {}
    for i in range(n_steps_x):
        for j in range(n_steps_y):
            d  = x[i:i+2, j:j+2].flatten()
            l = list(np.argsort(d))
            l = ''.join(str(e) for e in l)
            try:
                proba[l] += 1
            except:
                proba[l] = 1
            p = np.array(list(proba.values()))
            p = p/p.sum()
            h = np.sum(-p*np.log2(p))/np.log2(24)
    return h

