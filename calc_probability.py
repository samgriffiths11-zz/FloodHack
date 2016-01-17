import numpy
import arcpy
import pickle
import linecache
import sys
import matplotlib.pyplot as plt

## Set up arrays
def gen_ens_count(arr,q2, y):
    """ 
    Function to genrerate probabilities from array
    args:
    arr - Numpy array
    """

    inds = numpy.where(arr >q2 )
    #y+=1 in y
    y[inds]=y[inds]+1

    return y


# set up q2 vals


q2_data  = r"C:\temp\paul\data\q2\yr2.txt"
q2_array = numpy.loadtxt(q2_data).astype(float)
q2_flipped = numpy.flipud(q2_array)
q2_mask = numpy.isnan(q2_flipped)


q2_flipped[numpy.isnan(q2_flipped)] = -9999.00

text_base = r"C:\temp\paul\data\Input_data_for_probabilities\day_XXX.txt"
ensemble_template_name = "2015_26_12_00_00_00_XXX"



# Calculate the probability for the 51 ensembles  for one day
day_array = numpy.zeros([111,141],int)
day_array.fill(100)

# Loop through days here
for x in xrange(0,384,24):
    text_file_name = text_base.replace("XXX", str(x))
    blank_test = numpy.zeros([111,141],float)
    for y in range(1,51,1):
        line = linecache.getline(text_file_name, y)
        row_vals = line.split(",")
        array_line = numpy.array(row_vals).reshape(141,111).astype(float)
        arr_rot = numpy.rot90(array_line,1)
        m2_arr_name = gen_ens_count(arr_rot,q2_flipped,blank_test)
        ens_min = numpy.amax(m2_arr_name)

    # Do numpy divide
    divided_array = m2_arr_name / 51
    inds = (numpy.where(numpy.logical_and(divided_array > 0.7, day_array == 100)))
    day_array[inds] = x/24

    
min_val = numpy.amin(day_array)
mean_val = numpy.ndarray.mean(day_array)
max_val = numpy.amax(day_array)

day_array[q2_mask] = -9999.00
day_array_flipped = numpy.flipud(day_array)

f = open(r"C:\temp\paul\data\day_test_07.pkl","wb")
pickle.dump(day_array_flipped, f)
f.close()

exit()
point_coords = arcpy.Point(-11.0,49.0)
arcpy.env.outputCoordinateSystem = r"C:\Users\paulbarnard\Downloads\England_ct_2001_area_WGS84.prj"
myRaster = arcpy.NumPyArrayToRaster(day_array_flipped,point_coords,10000,10000,-9999)
myRaster.save(r"C:\temp\paul\data\day_test_07.tif")






    
    
    

    





