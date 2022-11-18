import PicoBotF_v02 as PicoBotF

this_volts = PicoBotF.ThisVolts()
if not this_volts.valid:
    print ('volts object creation failed')
else:
    print (this_volts.name, this_volts.read())
