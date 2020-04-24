from glob import glob

def get_all_csv(path: str)->list:
    return glob("./stats/*.csv")
