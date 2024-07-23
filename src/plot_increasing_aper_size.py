
import os
import statistics
from readCAT import readCAT
from sources import sourceExtract
import matplotlib.pyplot as plt
import json

def calculte_average_median_fwhm( imageName=None, which_source_file=None ):

    cat_filename = imageName.replace('working', 'sources')
    dirName = os.path.dirname( cat_filename )
    baseName = os.path.basename( cat_filename )

    if which_source_file == 'source_extractor':
        cat_filename = os.path.join( dirName, 'source_extractor', baseName)

        cat_filename = cat_filename.replace('.fits', '.cat')
        cat_filename = cat_filename.replace('.FIT', '.cat')
        cat_filename = cat_filename.replace('.fit', '.cat')

        dic = readCAT( cat_filename )

    fwhm_list = []
    for key in dic:
        fwhm_list.append( float( dic[key]['FWHM_IMAGE'] ) )

    median = statistics.median( fwhm_list )
    mean = statistics.mean( fwhm_list )

    return median, mean

def update_source_extractor_config( aperture_value ):   

    file = open('/dap/c_sources/cfg/Asteroid_Image_solving.cfg', 'w')
    #file.write('DETECT_THRESH = 50\n')
    file.write('DETECT_THRESH = 25\n')
    file.write('THRESH_TYPE = ABSOLUTE\n')
    #file.write('DETECT_MINAREA = 3\n')
    file.write('DETECT_MINAREA = 1\n')
    file.write('PHOT_APERTURES = %s\n'%(aperture_value) )
    file.close()


def main( image, xp, yp ):

    master_dic = {}
    results = {}

    sourceExtract( image ) #run SE for the first time

    #determine the cat name so the correct aperature value can be used
    
    median_fwhm, mean_fwhm = calculte_average_median_fwhm( imageName=image, which_source_file='source_extractor' )

    print (f"median_fwhm: {median_fwhm}, mean_fwhm: {mean_fwhm} ")
    #stop
    for i in range(0, 10):
        aperture_setting = int( (i * mean_fwhm) )
        update_source_extractor_config( aperture_setting )
        print (f"aperture_setting: {aperture_setting}")
        sourceExtract( image ) #run SE for the first time


        cat_filename = image.replace('working', 'sources')
        dirName = os.path.dirname( cat_filename )
        baseName = os.path.basename( cat_filename )

        cat_filename = os.path.join( dirName, 'source_extractor', baseName)

        cat_filename = cat_filename.replace('.fits', '.cat')
        cat_filename = cat_filename.replace('.FIT', '.cat')
        cat_filename = cat_filename.replace('.fit', '.cat')

        dic = readCAT( cat_filename )

        master_dic[i] = {}
        for key in dic:
            
            master_dic[i][key] = {}
            master_dic[i][key]['X_IMAGE'] = dic[key]['X_IMAGE']
            master_dic[i][key]['Y_IMAGE'] = dic[key]['Y_IMAGE']
            master_dic[i][key]['flux'] =  dic[key]['FLUX_APER']
            master_dic[i][key]['aperture_setting'] =  aperture_setting


        for key in dic:
            if abs( float( dic[key]['X_IMAGE'] ) - xp ) < 3:
                if abs( float( dic[key]['Y_IMAGE'] ) - yp ) < 3:

                    flux = dic[key]['FLUX_APER']

                    results[aperture_setting] = flux

    new_image = image.replace('working', '')
    new_image = new_image.replace('.fits', '.json')
    
    with open(new_image, "w") as outfile:
        json.dump( results, outfile)

    new_image = image.replace('working', '')
    new_image = new_image.replace('.fits', '_master.json')
    with open(new_image, "w") as outfile:
        json.dump( master_dic, outfile)
                    

    

def plot( image ):

    new_image = image.replace('working', '')
    new_image = new_image.replace('.fits', '.json')

    with open(new_image, "r") as f:
        results = json.load( f ) 

    aperture_setting = []
    flux = []
    for key in results:
        aperture_setting.append( key )
        flux.append( results[key])
        print (key, results[key] )
        plt.plot(int(key), float( results[key] ), 'ro')

    #plt.plot(aperture_setting, flux)
    plt.title('1120257_N20, xp=675, yp=2591')
    plt.xlabel('0-10 * FWHM (Pixel)')
    plt.ylabel('Flux')
    plt.show()

def plot_master( image ):

    new_image = image.replace('working', '')
    new_image = new_image.replace('.fits', '_master.json')

    with open(new_image, "r") as f:
        master_dic = json.load( f ) 


    dic_link = {}

    count = 0
    for fwhm_factor in master_dic:
        for key in master_dic[fwhm_factor]:
            dic_link[count] = {}
            dic_link[count]['X_IMAGE'] = master_dic[fwhm_factor][key]['X_IMAGE']
            dic_link[count]['Y_IMAGE'] = master_dic[fwhm_factor][key]['Y_IMAGE']
            dic_link[count]['aperture_setting'] = {}
            dic_link[count]['aperture_setting'][] = master_dic[fwhm_factor][key]['Y_IMAGE']

    #need to draw this out...
    #fwhm_setting(i) -> key_from_cat_files -> then values
            count += 1

if __name__ == "__main__":

    image1 = '/Users/linder/research/dap_data/review_files/75775/working/1120257_N20.fits'
    image2 = '/dap_data/review_files/75775/working/1120257_N20.fits'
    #xp = 828
    #yp = 2789

    #xp = 973
    #yp = 2849

    #xp = 932
    #yp = 2691

    xp = 675
    yp = 2591


    plot_results = False

    plot_master_results = False
    
    if plot_master_results == True:
        plot_master( image1 = '/Users/linder/research/dap_data/review_files/75775/working/1120257_N20.fits' )
    else:
        if plot_results == True:
            plot( image1 )
        else:
            main( image2, xp, yp)