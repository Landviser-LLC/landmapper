About iVEZ

This software is written and compiled in VisualBasic and installs into IVEZ folder. Executable file is ivez.exe. 
Coefficients g(i) for calculation of R-function (Eitkin) has been hardcoded into software.

Data input

Standard AB/2 distances (in cm) has been populated on program initiation, but those can be replaced by values for the used array.
Data of electrical resistivity (in Ohm m) for those AB/2 distances, measured in the field has to be typed in respective cells in the initial screen of the program. 
Several VES logs can be entered and then saved in the data files (example.txt is provided) and later used for interpretation.

Input from file

Create data input file either by using process above or by using Notepad or other text editor and creating file with formatting similar to example.txt file.
To open data file go File\Open.

Interpretation starts by pressing Run\Start
In iterative interpretation user need to list how many points fall on the strait line counting from right to left. This continues for several iterations. The end result - layer thicknesses and interpolated electrical resisitivities has shown in the window next to graph after return to initial screen and also saved in file protocol.txt. 

