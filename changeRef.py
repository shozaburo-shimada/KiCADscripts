import pcbnew

board = pcbnew.GetBoard()
c = board.GetModules()
for x in c:
    ref = x.GetReference()
    #print "#Ref: ", ref
    j = 0
    for p in range(len(ref)):
        if(ref[p].isalpha()!=True):
            #print "ref[p]: ", ref[p]
            if(ref[p]=="*"):
                break
            else:
                i = ref[0:p]
                j = int(ref[p:])
                break
    if(j>0):
        #print "i: ", i, ", j: ", j
        #k = i + '{0:04d}'.format(j)
        k=i+'{:d}'.format(j+150)
        print ref, "->", k
        ## remove next comment and run!
        ##x.SetReference(k)
