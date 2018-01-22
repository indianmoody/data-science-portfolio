
# packages
library('RPostgreSQL')


# Function to connect to db.
connect_db = function() {
  # Connect to data base
  pg = dbDriver("PostgreSQL")
  con = dbConnect(pg, user="postgres", password="password", host="localhost", port=5432, dbname="edstatsdb")
  return (con)
}


# Function to load EdStatsData.csv and create 'eddetails' table, if not already exists, in db.
create_eddetails_table_db = function() {
  
  # read just few rows to get column details
  tempdf = read.csv(file="/Users/gauravbishnoi/datas/Edstats_csv/EdStatsData.csv", nrows = 10)
  # change first 4 columns from factor to just characters
  tempdf[,c(1,2,3,4)] = apply(tempdf[,c(1,2,3,4)], 2, function(x) as.character(x))
  # drop columns from year 2015 onwards because they are empty
  tempdf[,grep('X2015', colnames(tempdf)):length(colnames(tempdf))] = NULL
  # drop column 'Indicator.Name'
  tempdf[,'Indicator.Name'] = NULL
  # delete rows with at least 30 missing values
  tempdf = tempdf[rowSums(is.na(tempdf)) <= 30, ]
  # modify column names to avoid period and large cap
  colnames(tempdf) = sapply(colnames(tempdf), function(x) tolower(gsub("\\.", "_", x)), USE.NAMES = FALSE)
  
  # make sql stament to create table in db with colnames columns
  
  # col names with types
  col_names = colnames(tempdf)
  
  # string for modified column names and data types. To be used in command to create table.
  sql_col_name_type = ""
  for(name in col_names) {
    
    if (class(tempdf[,name]) == 'character') {
      sql_col_name_type = paste(sql_col_name_type, " ", name, " ", class(tempdf[,name]), " varying,", "\n", sep="")
    }
    else {
      sql_col_name_type = paste(sql_col_name_type, " ", name, " ", class(tempdf[,name]), ",", "\n", sep="")
    }
    
  }
  # removing comma and newline after last column name and data type.
  sql_col_name_type = substr(sql_col_name_type, 1, nchar(sql_col_name_type)-2) 
  
  # command to create table
  create_command = paste("CREATE TABLE IF NOT EXISTS ", "eddetails", "\n(\n", sql_col_name_type, "\n)\nWITH (\nOIDS = FALSE\n);\n", sep="")
  
  #command to change ownership of table
  alter_command = "ALTER TABLE eddetails OWNER TO postgres;"
  
  # complete command to create table and change ownership
  create_table_command = paste(create_command, alter_command, sep="")
  
  # connect to database
  con = connect_db()
  # execute command 
  dbGetQuery(con, create_table_command)
  # close connection to database
  dbDisconnect(con)
}


# Function to clean and load data into 'eddetails' table in db.
fill_db = function() {
  
  con = connect_db() # connection to database
  chunk_size = 25573 # number of lines to be read at a time from csv file
  
  csv_con = file("/Users/gauravbishnoi/datas/Edstats_csv/EdStatsData.csv", "r") # connection to csv file
  
  # get column names from sql db table
  column_names = dbGetQuery(con, "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'eddetails';")
  
  column_line = read.csv(csv_con, nrows = 1, header = FALSE) # row with column details, now the file will be read from second row
  
  
  while (TRUE) {
    
    # read chunk_size lines from csv and store in temp database
    dff = read.csv(file = csv_con, nrows = chunk_size, header = FALSE)
    # save length of rows for later comparison
    dff_lines_original = NROW(dff)
    # change data type of first 4 columns from factor to character
    dff[,c(1,2,3,4)] = apply(dff[,c(1,2,3,4)], 2, function(x) as.character(x))
    # drop columns from year 2015 onwards because they are empty
    dff[,50:length(colnames(dff))] = NULL
    # drop column 'Indicator.Name'
    dff[,3] = NULL
    # drop rows that still contain at least 30 missing values
    dff = dff[rowSums(is.na(dff)) <= 30, ]
    
    
    # assign those names to current data frame
    colnames(dff) = column_names[, 1]
    
    # write current data frame into sql db table
    dbWriteTable(con, "eddetails", value = dff, append = TRUE, row.names = FALSE)
    
    # delete dff for this iteration
    rm(dff)
    
    # if total read lines from csv were less than chunk_size, reading is finished
    if (dff_lines_original < chunk_size) {
      break
    }
    
  }
  
  # close connection to csv file
  close(csv_con)
  
  # close connection to database
  dbDisconnect(con)
  
}


# Function to load EdStatsSeries.csv and create 'statseries' table, if not already exists, in db.
create_statseries_table_db = function() {
  
  stat_create_command = "CREATE TABLE IF NOT EXISTS statseries ( series_code character varying, topic character varying, short_definition character varying ) WITH ( OIDS = FALSE ); ALTER TABLE statseries OWNER TO postgres;"
  
  
  # connect to database
  con = connect_db()
  
  # execute command 
  dbGetQuery(con, stat_create_command)
  
  # close connection to database
  dbDisconnect(con)
  
}


# Function to clean and load data into 'statseries' table in db.
fill_statseries = function() {
  
  # read just few rows to get column details
  tempdf = read.csv(file="/Users/gauravbishnoi/datas/Edstats_csv/EdStatsSeries.csv")
  # drop all columns except 1,2,4
  tempdf = tempdf[,c(1,2,4)]
  # rename columns
  colnames(tempdf) = c('series_code', 'topic', 'short_definition')
  # change data type of all 3 columns from factor to character
  tempdf[,1:3] = apply(tempdf[,1:3], 2, function(x) as.character(x))
  
  # connect to database
  con = connect_db()
  
  # write current data frame into sql db table
  dbWriteTable(con, "statseries", value = tempdf, append = TRUE, row.names = FALSE)
  
  # close connection to database
  dbDisconnect(con)
  
}

