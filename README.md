# Golf Stats
##  

Flask application based on the megatutorial series by Miguel Grinberg. This app allows users to input common golf stats such as score, fairways, greens in regulation and putts on the rounds that they've played. Their stats are kept for the single round along with all the rounds that they have played in the past.

### Filtering Data
The goal will be to have the option to filter total stats by the attributes of the round that they've played. For example they can look at the rounds based on course, or by whether the rounds were a tournament or not and see cumulative stats on these rounds such as greens in regulation percentage or par 5 scoring average.

### Packages
This app uses _pandas_ for calculating the statistics and relies on common flask extensions for the handling forms, databases and user sessions. Styling will be done using Bootstrap 4
