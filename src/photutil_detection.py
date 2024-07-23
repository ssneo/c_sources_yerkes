

from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder
from astropy.io import fits
import json
import os


def source_detection( filename, data, fwhm, threshold, peakmax, roundlo, roundhi, median, plotSourcesInDS9, saveResults ):

    daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold, peakmax=peakmax, roundlo=roundlo, roundhi=roundhi) #roundness is how circular it is. 0 is compeletly circular -1 is extended in x and 1 is extended in y.

    #sources = daofind( data - median)

    sources = daofind( data )

    #print (sources)
    #stop

    #print ("Number of sources found: ", len(sources))

    #stop

    if plotSourcesInDS9 == True:
        import pyds9
        d=pyds9.DS9()
        d.set('file %s'%( filename ))
        d.set('regions delete all')



        for col in sources.colnames:
            sources[col].info.format = '%.5g'

        for i in range( 0, len(sources)):
            #print ('sources[i]', sources[i])
            #stop
            xp = float( sources[i]['xcentroid'] )#
            yp = float( sources[i]['ycentroid'] )
            #print (xp, yp)
            #if xp < 640 and xp > 550:
            #    if yp < 2140 and yp> 2000:
            size = 10
            reg3='regions command "circle %s %s %s #color=red"'%(xp, yp, size )
            d.set('%s'%(reg3))

    #for col in sources.colnames:
    #    print(col)
    
    #print( sources.info )
    #stop
    dic = {}
    for i in range( 0, len( sources ) ):
        dic[i] = {}

        #print (sources[i])

        dic[i]['id'] = int( sources[i]['id'] )
        dic[i]['xcentroid'] = round( float( sources[i]['xcentroid'] ), 6 ) 
        dic[i]['ycentroid'] = round( float( sources[i]['ycentroid'] ), 6 )
        dic[i]['sharpness'] = round( float( sources[i]['sharpness'] ), 6 )
        dic[i]['roundness1'] = round( float( sources[i]['roundness1'] ), 6 )
        dic[i]['roundness2'] = round( float( sources[i]['roundness2'] ), 6 )
        dic[i]['npix'] = int( sources[i]['npix'] )
        dic[i]['sky'] = round( float( sources[i]['sky'] ), 6 )
        dic[i]['peak'] = round( float( sources[i]['peak'] ), 6 )
        dic[i]['flux'] = round( float( sources[i]['flux'] ), 6 )
        dic[i]['mag'] = round( float( sources[i]['mag'] ), 6 )

        #print (dic[i])
        #stop

    outputFileName = filename.replace('working', 'sources')

    dirName = os.path.dirname( outputFileName )
    baseName = os.path.basename( outputFileName )
    outputFileName = os.path.join( dirName, 'dao_starfinder', baseName)

    outputFileName = outputFileName.replace('.fits', '.json')
    outputFileName = outputFileName.replace('.fit', '.json')
    outputFileName = outputFileName.replace('.FIT', '.json')


    if saveResults == True:
        with open(outputFileName, 'w') as f:
            json.dump(dic, f)

    #stop

    return sources, daofind



if __name__ == "__main__":

    z = '/users/linder/research/dap_data/decam/2022_08_12/1120241/working/1120241_n1.fits' #z
    fi = fits.open( z )
    data = fi[0].data
    fi.close()

    #get the mean, median, and std of the image data
    mean, median, std = sigma_clipped_stats( data, sigma=3.0)
    #print (mean, median, std)

    filename = z
    fwhm = 3.0
    threshold = 6.0 * std
    peakmax = 60000
    roundlo = -0.4
    roundhi = 0.4
    plotSourcesInDS9 = True


    sources = source_detection( filename, data, fwhm, threshold, peakmax, roundlo, roundhi, median, plotSourcesInDS9  )



