if __name__ == '__main__':


    s = "10"
    count = 0
    while s != "1" and s[:-1]:
        if s[-1] == "1":
            s = s[:-1] + "0"
        else:
            s = "0"+s[:-1]
        count = count +1
    print(count)

