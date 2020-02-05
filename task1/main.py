def get_sort_lst_from_file(filename):
    lst = open(filename, "r").readline().replace("\"", "").split(",")
    lst.sort()
    return lst

def get_sum(names_lst):
    esum = 0
    for ina, na in enumerate(names_lst):
        print(na)

if __name__ == "__main__":
    get_sort_lst_from_file("names.txt")