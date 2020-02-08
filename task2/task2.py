import sys
import re


def get_min(ips, frequent):
    minv = 0
    for m in range(1, 5):
        if ips[frequent[m]] and ips[frequent[m]] < ips[frequent[minv]]:
            minv = m

    return minv


def get_top(filename):
    ips = {}
    frequent = []

    with open(filename, "r") as hf:
        for hit in hf:
            ip = re.match(r".*(\t)(([0-9]{1,3}.){3}[0-9]{1,3})(\t).*", hit).group(2)
            if ip not in ips:
                ips[ip] = 1
                if len(frequent) < 5:
                    frequent.append(ip)
            else:
                ips[ip] += 1

            if len(frequent) == 5:
                cur_min = get_min(ips, frequent)
                if ip not in frequent and ips[frequent[cur_min]] < ips[ip]:
                    frequent[cur_min] = ip

    print(ips)
    print(frequent)
    min_top = get_min(ips, frequent)
    for i in ips:
        if ips[i] == ips[frequent[min_top]] and i != frequent[min_top]:
            frequent.append(i)


if __name__ == "__main__":
    get_top(sys.argv[1])