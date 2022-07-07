path1 = "/Users/mac/Documents/transformer_tape_dnabert/inspect_NPInter/rnaperprotein_rpi7317.csv"

import pandas as pd
import matplotlib.pyplot as plt

def main():
    count = 0
    arr1 = pd.read_csv(path1)
    for item in arr1.values:
        if item[0] == 1:
            count += 1
    print(count/len(arr1.values))
    count = 0
    for item in arr1.values:
        if item[0] <= 20:
            count += 1
    print(count/len(arr1.values))
    count = 0
    for item in arr1.values:
        if item[0] <= 30:
            count += 1
    print(count/len(arr1.values))
    plt.figure()
    plt.hist(arr1, rwidth=0.9)
    plt.ylim(0,6)
    # arr1.hist(bins=14)
    plt.show()


if __name__ == "__main__":
    main()