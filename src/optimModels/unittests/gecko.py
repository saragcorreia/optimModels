from geckopy import GeckoModel
from optimModels.unittests.kinetic_optim import ko_jahan
import pandas

if __name__ =="__main__":
    import time
    some_measurements = pandas.Series({'P00549': 0.1, 'P31373': 0.1, 'P31382': 0.1})
    model = GeckoModel('multi-pool')
    a = model.proteins
    print(a)
    t1 = time.time()
    model.limit_proteins(some_measurements)
    res = model.optimize()
    t2 = time.time()

    print("tempo " + str(t2-t1))
    print("res")