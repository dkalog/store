import json
import numpy as np

def readJson(filename):
    count_objects = 0
    Rg = np.empty([0, 9])
    Tg = np.empty([0, 3])
    imID = np.array([])
    keys = []
    with open(filename, 'r') as file:
        data = json.load(file)
    for i in data:
        count_objects += 1
        keys.append(str(i))

    print("keys: ", keys)

    for obj in keys:
        for nst_obj in data[str(obj)]:
            print(nst_obj['cam_R_m2c'])
            # Rg = np.append(Rg,[nst_obj['cam_R_m2c']]).astype(np.double)

            Rg = np.vstack([Rg, (nst_obj['cam_R_m2c'])]).astype(float)
            Tg = np.vstack([Tg, np.array(nst_obj['cam_t_m2c'])]).astype(float)
            imID = np.append(imID, int(obj)).astype(int)

    print(Rg)
    return Rg, Tg, imID

