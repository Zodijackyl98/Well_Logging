# Well_Logging

First, read_las.py is focused on reading LAS files which are created by mud logging companies like GEOLOG and creating different kind of plots with already existing parameters and new parameters then creates another files which you can find details below. Second, Python file "drilling_calculations" figures basic values that are used in drilling operations, details are located below.

After giving your path to your las file inside read_las.py;
-  Users need to define which time period they want to check by adjusting st_time(start time) and ed_time(end time) in 'yyyy-mm-dd hh:mm:ss' format. Default is already set, defining incorrect time will lead to no data condition. Note that mentioned statistics about parameters include this interval not the interval of all data as well as graphs for given couples in df_graphs. [['TOTACTIVEPITS','ACT_VOL'], ['PRESSURE_IN','FLOWPADDLE'], ['HOOK POS','WOB3']]
-  Program will create a directory inside the directory where you executed this code called 'wells'. You can find every file inside ./wells directory(.html, .txt, .xlsx, .png).
-  All graphs are converted to png files in case users might want to save them automatically eventhough after execution of the code, all plots appear at the same time on your screen. 
-  Some graphs can also be found in interactive html format for example; ROP,SPP,RPM,TQ, WOB, BIT_POS all together inside one html file. One side effect is that values are not scaled in html files but they are in png files and of course in matplotlib graphs because they don't share one x line that stores all the values inside instead they share        different x axis but shares common y axis. Users are advised to use matplotlib windows to check the data they are after because mostly interactivity is enough with matplotlib plot screens. Size of labels and tick marks often too big. 
-  Mininum, maximum and median values for all parameters are written in a txt file.
-  Lastly, .xlsx file is created with all the parameters inside las file including new ones.

![drilling_params](https://github.com/Zodijackyl98/Well_Logging/assets/63348489/6c9ff198-45c3-430f-9d1d-b14795a6d874)

![drilling_params_2](https://github.com/Zodijackyl98/Well_Logging/assets/63348489/94ac2920-a7da-4cf6-ab43-7cbc26269150)

![drilling_params_3](https://github.com/Zodijackyl98/Well_Logging/assets/63348489/ccc2da37-26b2-4cb5-afab-662d73552a7a)

![drilling_params_html](https://github.com/Zodijackyl98/Well_Logging/assets/63348489/d45bf6cb-a1c9-4692-ac78-364266d6f164)

Users can use well_calculations.py file for drilling parameters to calculate; String weight in mud-air, Bottom Hole Pressure(BHP), Capacity of the well, drill string, steel volume, annular volume, FLow rate, lag time, down time, cycle time, pressure losses etc.
-  After execution, a txt file consists of all variables is created inside the directory where you execute the file.
