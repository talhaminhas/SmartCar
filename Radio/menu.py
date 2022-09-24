ans = True
print ("You pressed ",ans)
while ans:
    print ("f) Go to 101.1 The Fox")
    print ("+) Increase Volume")
    print ("-) Decrease Volume")
    print ("=) Channel Number (=101.1)")
    print ("w) Tune Up")
    print ("s) Tune Down")
    print ("c) Print Current Channel")
    print ("4) Seek Down")
    print ("5) Seek Up")
    print ("")
   
    ans = input(">")
    if ans == "5":
        print ("You pressed ",ans)
        #seek (1) #1=up\
    if ans == "4":
        #seek (0)
        print ("You pressed ",ans)
    if ans == "f":
        print ("You pressed ",ans)
        #changechannel(1011)
    if ans == "+":
        #currvol += 1
        #setvolume (currvol)
        print ("You pressed ",ans)
    if ans == "c":
        #print
        #print "Curr Chan=", float(float(getchannel())/float(10))
        #print
        print ("You pressed ",ans)
    if ans == "-":
        #currvol -= 1
        #setvolume (currvol)
        print ("You pressed ",ans)
    if ans == "w":
        #currchan = getchannel()
        #wc = currchan + 2
        #if wc >= 878 and wc <= 1080:
         #   currchan = wc
         #   changechannel(currchan)
        print ("You pressed ",ans) 
    if ans == "s":
        #currchan = getchannel()
        #wc = currchan - 2
        #if wc >= 878 and wc <= 1080:
         #   currchan = wc
         #   changechannel(currchan)
        print ("You pressed ",ans)
    if ans != "" and ans[0] == "=":
        print ("You pressed ",ans)
