from preprocessing.preprocessing import getNumberEight, preprocess
from http.request import getData


if __name__ == "__main__":
    data = getData("./data/export.csv")

    filtered = preprocess(data)

    print(filtered)