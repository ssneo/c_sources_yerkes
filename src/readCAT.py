

def readCAT(file):

    file = open(file,'r')
    f = file.readlines()
    file.close()


    itemCounter=0
    fieldNames = []
    fieldDescp = []
    fieldUnits = []

    catFile = {}
    for i in range(0,len(f)):
        if f[i][0]=='#':
            
            fieldNames.append(f[i][6:29].replace(' ', '')) #remove the extra spaces
            fieldDescp.append(f[i][29:88].replace('  ', '')) #Remove every two spaces, this keeps the spaces between words
            fieldUnits.append(f[i][89: len(f[i])-2 ])

            #currently the above values are not included into the dic file

            #print (fieldNames)
            #print (fieldDescp)
            #print (fieldUnits)
            

        else:
            catFile['s%s'%(itemCounter)] = {}
            start=0
            count=0
            previous=0
            for j in range(1,len(f[i])): #start at 1 not 0, there is a space when ins-mag is single digital
                ssp = f[i].split(' ')

                #print (ssp)
                #stop
                #print ('')
                fieldCount = 0
                for k in range(0, len(ssp)):

                    if len(ssp[k]) > 1 or ssp[k] != '':
                        #print (ssp)
                        #print (catFile)
                        if k == len(ssp) -1 :
                            catFile[ 's%s'%(itemCounter) ][fieldNames[fieldCount]] = ssp[k][:-1]
                        else:
                            catFile[ 's%s'%(itemCounter) ][fieldNames[fieldCount]] = ssp[k]
                        fieldCount += 1
                        #print (ssp[k])


            itemCounter += 1


    return catFile
