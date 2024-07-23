
import os
from readCAT import readCAT
import statistics
from sources import sourceExtract
import glob

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

    file = open('/dap/c_sources_yerkes/cfg/Asteroid_Image_solving.cfg', 'w')
    file.write('DETECT_THRESH = 50\n')
    file.write('THRESH_TYPE = ABSOLUTE\n')
    file.write('DETECT_MINAREA = 3\n')
    file.write('PHOT_APERTURES = %s\n'%(aperture_value) )
    file.close()


def run_c_sources( images=None, aperture_diameter_in_fwhm=None, se_files_loc=None  ):

    for im in images:

        sourceExtract( im ) #run SE for the first time

        #determine the cat name so the correct aperature value can be used
        
        median_fwhm, mean_fwhm = calculte_average_median_fwhm( imageName=im, which_source_file='source_extractor' )

        print (f"median_fwhm: {median_fwhm}, mean_fwhm: {mean_fwhm} ")
        #stop
        aperture_setting = int( (3 * mean_fwhm) )
        update_source_extractor_config( aperture_setting )
        print (f"aperture_setting: {aperture_setting}")
        #stop

        sourceExtract( fileName = im, se_files_loc = se_files_loc ) #run SE again


if __name__ == "__main__":

    

    aperture_diameter_in_fwhm = 3
    folder_of_images = '/dap_data/review_files/75775/working/'

    parent_dir = os.path.dirname( folder_of_images )
    se_files_loc = os.path.join( parent_dir, 'sources')
    #print ('se_files_loc', se_files_loc)
    #stop
    if os.path.exists( se_files_loc ) == False:
        os.mkdir( se_files_loc )

    #get list of images:
    images = glob.glob( folder_of_images + "*.fits")
    images += glob.glob( folder_of_images + "*.fit")
    images += glob.glob( folder_of_images + "*.FIT")


    run_c_sources( images=images, aperture_diameter_in_fwhm=aperture_diameter_in_fwhm, se_files_loc=se_files_loc  )



    