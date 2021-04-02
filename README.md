# LandMapper IO module development
Working on streamlining data processing from our handheld devices. Updating data processing: CSV files to 
- Mapping (utilizing timestamp to link with lat/long from GPS - ideally for new models, see the process for manual procedure https://landviser.com/map-salinity-farm-fields/) 
- 1D VES (have developed a software, old one, looking for code, was in Basic, but there is opensource available in Python) now process in Excel https://landviser.com/1d-vertical-electrical-sounding/
- 2D imaging (RES2DINV/RES3DINV software is available from our partners, missing piece is streamlining IO from device to .DAT format/layout accepted by RES2DINV - now process in Excel https://landviser.com/2d-dipole-dipole-electrical-tomography/

## ERM01
folder for info and data format for older models - those are still in use by some clients, however the connect for IO is serial port and do not works, just as example. Ideally for those clients can have a mobile app to type measurements from the screen of LandMapper and then output different graphs: mapping, 1D VES, 2D imaging. Mapping part could be done through ESRI platform, that why Geo-App course recommended.

## ERM03 & 04
Info and new models (ERM03-04) manuals available here https://landviser.com/equipment/landmapper/ including compiled helper Win soft for IO from device
