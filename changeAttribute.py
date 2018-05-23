import pcbnew

board = pcbnew.GetBoard()
c = board.GetModules()
for x in c:
    ref = x.GetReference()
    attr = x.GetAttributes()
    print "#Ref: ", ref, " #Attrubute: ", attr
    #x.SetAttributes(1)
