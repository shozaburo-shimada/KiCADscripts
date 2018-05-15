import pcbnew

board = pcbnew.GetBoard()
c = board.GetModules()
for x in c:
    ##print x.GetReference()
    ref = x.GetReference()
    j = 0
    for p in range(len(ref)):
        if(ref[p].isalpha()!=True):
            if(ref[p]=="*"):
                break
            else:
                i = ref[0:p]
                j = int(ref[p:])
    if(j>0):
        k = i + '{0:04d}'.format(j)
        # k=i+‘{:d}’.format(j+100)
        print ref, "->", k
        ## remove next comment and run!
        ##x.SetReference(k)
