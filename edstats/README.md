## Unemployment, Gender Equality and Foreign Education

A country's growth can be measured by how it's faring in some important sectors over the years. Some of them are male and
female unemployment, female share of labor force and students studying outside of their country. The relevant information was
extracted from [data released by World Bank](https://data.worldbank.org/data-catalog/ed-stats).

### Files/Folders
* **csv_to_db.R :** R Script containing functions to read raw data from csv, clean and load it into PostgreSQL.
* **clean_load.Rmd :** RStudio file that implements csv_to_db.R script functions.
* **quick_analysis.Rmd :** RStudio file for exploratory analysis
* **edstats_visualization.Rmd :** RStudio file to create plots out of relevant data
* **edstats_app:** Folder containing Shiny app for visualization of all these features for 172 countries.

### Tools Used
* R, RStudio
* Shiny
* PostgreSQL

### Acknowledgements
* [World Bank](https://data.worldbank.org/data-catalog/ed-stats) for data
* Stackoverflow Community
* Open Source Community for wonderful free softwares
