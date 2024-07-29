
import glob
from astropy.io import fits
import os
import shutil
import sys
from astropy.wcs import WCS
from astropy import units as u
#import logging
import time
import socket
#import psycopg2
from datetime import datetime, timezone
from photutil_detection import source_detection
from astropy.stats import sigma_clipped_stats


#from client_queue import client_queue

#try:
#    logging.basicConfig( filename = '/container_c_log.log', level=logging.DEBUG)
#except:
#    logging.basicConfig( filename = '/Users/linder/container_c_log.log', level=logging.DEBUG)


def readInformationFromDatabase(msg): #confirm the psql line is correct
    #image = "1120208_N1.fits"
    #file_location = "/dap_data/DECAM/2022_08_12/1120208/working/"

    config = {
        "host": "192.168.1.21",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    psql = "SELECT file_location, image FROM dap WHERE id=%s"%( msg )
    print ('psql line 71', psql)

    cur.execute(psql)
    output = cur.fetchall()
    folder_loc = output[0][0]
    image_file_name = output[0][1]
    con.close()
    #

    if os.path.basename( folder_loc  ) == 'working' or os.path.basename( folder_loc  ) == 'workin':
        fileName = os.path.join( folder_loc, image_file_name )
    else:
        fileName = os.path.join( folder_loc, 'working', image_file_name)

    return fileName

def updateDB( msg, id ):
    config = {
        "host": "192.168.1.21",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    psql = "UPDATE dap SET source_extract_in_progress=false, source_extract_complete=true WHERE id=%s "%( id )
    print ('psql update command is: ', psql )

    cur.execute(psql)

    con.commit()

    con.close()

def log(value):
    utcTime = datetime.utcnow()
    time = '%s-%s-%s %s:%s:%s'%( utcTime.strftime("%Y"), utcTime.strftime("%m"), utcTime.strftime("%d"), utcTime.strftime("%H"), utcTime.strftime("%m"), utcTime.strftime("%S"))
    logging.info("%s: %s"%(time, value))

def sourceExtract( fileName = None, se_files_loc = None ):

    start = datetime.now(timezone.utc)
    #images = glob.glob( folderOfCompressed + 'working/' + '*.fits')
    #images += glob.glob( folderOfCompressed + 'working/' + '*.fit')
    
    #print (len(images))

    if se_files_loc == None:
        outputFileName = fileName.replace('working', 'sources')
        dirName = os.path.dirname( outputFileName )
        baseName = os.path.basename( outputFileName )
        outputFileName = os.path.join( dirName, 'source_extractor', baseName)

        outputFileName = outputFileName.replace('.fits', '.cat')
        outputFileName = outputFileName.replace('.fit', '.cat')
        outputFileName = outputFileName.replace('.FIT', '.cat')
        #print (outputFileName)
    else:
        baseName = os.path.basename( fileName )
        outputFileName = os.path.join( se_files_loc, baseName)

        outputFileName = outputFileName.replace('.fits', '.cat')
        outputFileName = outputFileName.replace('.fit', '.cat')
        outputFileName = outputFileName.replace('.FIT', '.cat')
        print ('outputFileName', outputFileName)
    #stop

    #this is for dotty
    #command = 'source-extractor -c /mnt/raid/k8s_files/sex/Asteroid_Image_Solving.sex -CATALOG_NAME %s %s'%( outputFileName, fileName ) 

    #this is for mac on testing
    command = 'source-extractor -c /dap/c_sources_yerkes/cfg/Asteroid_Image_Solving.cfg -CATALOG_NAME %s %s'%( outputFileName, fileName )
    #print (command)
    #stop
    os.system( command )
    #stop

    end = datetime.now(timezone.utc)
    print ('total source Extract processing time: ', end-start)

def tphot( fileName, aperture_setting ):
    # aperture_setting is not being used


    start = datetime.now(timezone.utc)
    outputFileName = fileName.replace('working', 'sources')

    dirName = os.path.dirname( outputFileName )
    baseName = os.path.basename( outputFileName )
    outputFileName = os.path.join( dirName, 'tphot_trail', baseName) 

    outputFileName = outputFileName.replace('.fits', '.stars')
    outputFileName = outputFileName.replace('.fit', '.stars')
    outputFileName = outputFileName.replace('.FIT', '.stars')

    command = './tphot/tphot %s -trail -sig 5 -min 10 -snr 5 -out %s'%( fileName, outputFileName  ) #digs into the weeds for sources and performs trailed Waussian #extreme amount of time per object when snr=5 (r730=19mins, 7950x=)
    #command = './tphot/tphot %s -trail -out %s'%( fileName, outputFileName  ) #use default settings
    os.system( command )

    outputFileName = fileName.replace('working', 'sources')

    dirName = os.path.dirname( outputFileName )
    baseName = os.path.basename( outputFileName )
    outputFileName = os.path.join( dirName, 'tphot_non_trail', baseName) 

    outputFileName = outputFileName.replace('.fits', '.stars')
    outputFileName = outputFileName.replace('.fit', '.stars')
    outputFileName = outputFileName.replace('.FIT', '.stars')

    command = './tphot/tphot %s -sig 5 -min 10 -snr 5 -out %s'%( fileName, outputFileName  ) #digs into the weeds for sources and performs trailed Waussian #extreme amount of time per object when snr=5 (r730=19mins, 7950x=)
    os.system( command )

    end = datetime.now(timezone.utc)
    print ('total tphot processing time: ', end-start)

def photutils( fileName, fwhm ):

    #dao starfinder is ran as part of a threshold_values command for PSF. Need to determine if the results are clipped or working correctly.
    #stop
    start_1 = datetime.now(timezone.utc)

    fi = fits.open( fileName )
    data = fi[0].data
    header = fi[0].header
    fi.close()

    mean, median, std = sigma_clipped_stats( data, sigma=5.0) 
    #fwhm = 3.0
    peakmax = 60000
    roundlo = -0.9
    roundhi = 0.9
    threshold = 250
    plotSourcesInDS9 = False

    source_detection( fileName, data, fwhm, threshold, peakmax, roundlo, roundhi, median, False, True )



    end_1 = datetime.now(timezone.utc)
    total_lapse = end_1-start_1
    print ('')
    print ('total source Extract processing time: ', total_lapse.total_seconds() )
    print ('')

def find_local_folder_to_process():

    
    config = {
        "host": "host.docker.internal",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    psql = "SELECT obsid FROM dap WHERE insert_wcs=True and source_extract=False order by id limit 1"
    
    cur.execute(psql)

    obsid = cur.fetchall()

    con.close()

    try:
        obsid = obsid[0][0] #if the response is empty this will error out

    except:
        obsid = 'None'

    return obsid

def update_local_folder_processed(obsid):

    config = {
        "host": "host.docker.internal",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()


    psql = "UPDATE dap SET source_extract=True where obsid=%s"%(obsid)
    
    cur.execute(psql)

    con.commit()

    con.close()

if __name__ == "__main__":

    test_mode = False

    testOnMac = False
    #test_specific_number = 23968
    test_specific_number = 22789
    #test_specific_number = 605

    testImage = '/dap_data/DECAM/2022_08_12/1120208/working/1120208_N1.fits'
    #testFolder = "/dap_data/2023_DZ2/2023_03_20/working/"
    #testFolder = "/dap_data/DECAM/2022_08_12/1120241/working/"
    #testFolder = "/dap_data/ARI/14/working/"

    testFolder = "/dap_data/DECAM/orginal_2022_08_12/1120208/working"

    #testFolders = "/dap_data/DECAM/orginal_2022_08_12/" #this is the base directory


    images = glob.glob( "%s/*.fits"%(testFolder) )
    images += glob.glob( "%s/*.fit"%(testFolder) )
    images += glob.glob( "%s/*.FIT"%(testFolder) )

    runLocalImage = False
    runLocalFolder = False

    local_speed_test = True


    #if runLocalFolder == True:
    #    while(1):
    #        obsid = find_local_folder_to_process()

    #        if obsid != 'None':
                

                #folder_loc = os.path.join( testFolders, str(obsid) )
                #if folder_loc[-1] != "/":
                #    folder_loc += "/"

                #print ('folder_loc', folder_loc)
                #folders = glob.glob('%s*'%(folder_loc) )
                #print ('len(folders)', len(folders))
                #for folder in folders:

                #images = glob.glob( "%s/working/*.fits"%(folder_loc) )
                #images += glob.glob( "%s/working/*.FIT"%(folder_loc) )
                #images += glob.glob( "%s/working/*.fit"%(folder_loc) )
                #print ('len(images)', len(images))
                #for im in images:
                    #print (im)
                #    sourceExtract( im )
                #    photutils( im )

                #update_local_folder_processed( obsid )
                #stop
                
            #else:
            #    print ('Obsid returned none, obsid=%s'%(obsid))
            #    break

    
    #if runLocalFolder == True:
    #    for im in images:
    #        sourceExtract( im )
    #        photutils( im )


    
            
    #elif runLocalImage == True:
    #    sourceExtract( testImage )
    #    photutils( testImage )

    #stop

    while(1):
        sleepTime = 1
        if test_mode == False:
            msg = client_queue('192.168.1.21', 62893)
        else:
            msg = test_specific_number

        if msg == 'NO_DATA':
            log('Got a message of None therefore going to sleep and doing nothing')
            time.sleep( sleepTime )
        else:
            #msg = msg.split('=')[1]
            #print ('msg', msg)
            #stop
            log('Got a message: ' + str(msg) )
            print ('Got Message of: ', msg)

            if test_mode == False:
                fileName = readInformationFromDatabase( msg )
                if local_speed_test == True:
                    fileName = fileName.replace('truenas', 'raid')

            else: #this is only for test mode
                fileName = readInformationFromDatabase( msg )
                if testOnMac == True:
                    fileName = fileName.replace('/mnt/raid/decam/2022_08_12/', '/dap_data/DECAM/orginal_2022_08_12/')

                if os.path.exists( fileName ) == 'False':
                    command = "scp 192.168.1.21:%s %s"%(fileName, fileName)
                    os.system( command )

                

            #print ('file_location', file_location)
            #stop
            log('fileName: ' + fileName)
            print ('Got fileName of: ', fileName)
            #startUp("/dap_data/DECAM/2022_08_12/1120208/working/")

            #lowarcsec = 0.23
            #higharcsec = 0.29

            #if runTestImage == True:
            #    sourceExtract( testImage )
            #    photutils( testImage )
            #    #stop
            #else:
            print ('Source Extract')
            sourceExtract( fileName )

            #print ('Photutils ')
            #photutils( fileName )

            print ('tphot ')
            tphot( fileName )
            
            if test_mode == False:
                updateDB( msg, msg ) #say the work has been done
            log('updateDB function complete')
            print ('updateDB is complete for ', msg )

            time.sleep( sleepTime )

        if test_mode == True:
            break