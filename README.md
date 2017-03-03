# treemap_extensions
## add customizations to treemap d3 graph

The purpose of this repository is to add to base d3 treemap graph https://bl.ocks.org/mbostock/4063582. Instead of processing csv 
file to json on-the-fly in javascript, this is moved back to preprocessing script in python. I simply did this to reduce the complexity 
of the javascript file, given I have added some custom functions there. In addition to this, I have added drop down options, so the 
treemap automatically filters the data on the fly. This is useful if you want to add another dimension to the view e.g. multiple kpi measures. 
There is also functionality which adds npm to it. If you want to update the file with your own data, there are a 
few places to change static text values i.e. "KPI One - Count". I did not add a color legend however it represents action type dimension. Possibility to 
extend the translate function to intoduce a lag like the original. If you want to use this please "star it". Gist for this repo can be found here 
http://bl.ocks.org/DouglasFletcher/30a8b95113f4e0c2f8be72ad30493964
(https://gist.github.com/DouglasFletcher/30a8b95113f4e0c2f8be72ad30493964)

