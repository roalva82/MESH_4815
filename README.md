# MESH_4815
MESH model for Alberta Census Division No. 15 (shapefile ID 4815)

Division No. 15 corresponds to the uppermost part of catchments in Alberta starting from the Rocky Mountains. It encompass an area roughly between Canmore and Jasper. For details about this area see maps in: https://open.alberta.ca/dataset/2c4ab1d1-46a7-49f6-a1b0-a19182a0a636/resource/56f83c81-221c-412e-b008-a8130fded49b/download/map-series-alberta-census-divisions.pdf

![image](https://github.com/roalva82/MESH_4815/assets/38491952/a439ee2a-a555-4129-a431-05a67d44a148)

The model is a subdivision of the Alberta provincial territory. It will be used as a testbed for model calibration. We will start by calibrating the subbasin with ID 71037856 extracted from the Merit Hydro Basins. This subbasin is located upstream of the city of Longview, about 70 km southwest of Calgary. The subbasin is particularly suitable due to the presence of the station from the Water Survey of Canada (WSC) with ID 05BL027. 

![image](https://github.com/roalva82/MESH_4815/assets/38491952/3d3e4e47-26ba-49a5-9ebf-00c8056e176b)

The repository contains the forcing files for year 1980. The model is configured to run the month of May 1980 to assess the configuration setup of Ostrich. The configuration in Ostrich currently picks up the performance metric created by MESH in order to optimize the calibration. The calibration is tested on a single parameter for hydraulic conductivity in the Group Response Unit (GRU) corresponding to "Needleleaf Forest-SW (temporate)". 

OPEN QUESTIONS:
- the outputs_balance.txt file was needed to be able to run the model. I created an empty file to be able to run the model. 
- is the metric obtained in MESH appropiate for the calibration? AUTOCALIBRATIONFLAG is set to 4 to obtain the negative Nash-Sutcliffe Efficiency.
- why is the calibration not sensitive to the change of the parameter ___x1.
