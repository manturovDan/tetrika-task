import sys


def get_sort_lst_from_file(filename):
    with open(filename, "r") as f:
        lst = f.readline().replace("\"", "").split(",")
    lst.sort()
    return lst


def get_sum(names_lst):
    esum = 0
    for ina, na in enumerate(names_lst):
        ksum = 0
        for let in na:
            ksum += ord(let) - 64
        esum += ksum * (ina + 1)
        print(na, ksum * (ina + 1), esum)
    return esum


if __name__ == "__main__":
    print(get_sum(get_sort_lst_from_file(sys.argv[1])))