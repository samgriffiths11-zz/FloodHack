import numpy
from osgeo import gdal


myarray = numpy.array(ds.GetRasterBand(1).ReadAsArray())
ds = gdal.Open("C:\Users\Sam\Downloads\rl_20.tif") 
with open(r"C:\Users\Sam\Downloads\q20.txt", 'a+') as out_file:
    for row in myarray:
        out_file.write(str(row))