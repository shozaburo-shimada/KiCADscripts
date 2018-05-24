import pcbnew

board = pcbnew.GetBoard()
mlist = board.GetModules()
for m in mlist:
    ref = m.GetReference()
    print "#Ref: ", ref

    plist = m.Pads()
    dip_flag = 1
    for p in plist:
        #print "pad: ", p.GetDrillSize()
        if p.GetDrillSize()[0] == 0:
            dip_flag = 0
            break

    if dip_flag == 0:
        print "    This is SMD module"
        m.SetAttributes(1)
    else:
        print "    This is DIP module"

    attr = m.GetAttributes()
    print  "    Attrubute: ", attr
