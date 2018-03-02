with open("input_file.txt","r") as f:
    a = f.readlines()
    for line in a:
        [x,y] = line.split()
        print x
        print y