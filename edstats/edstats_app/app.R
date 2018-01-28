
library(shiny)

#un_fm_df_app = read.csv(file = "https://raw.githubusercontent.com/indianmoody/data-science-portfolio/master/edstats/plot_data/female_unemployment.csv", stringsAsFactors = FALSE)
#un_ma_df_app = read.csv(file = "https://raw.githubusercontent.com/indianmoody/data-science-portfolio/master/edstats/plot_data/male_unemployment.csv", stringsAsFactors = FALSE)
#labor_share_fm_df_app = read.csv(file = "https://raw.githubusercontent.com/indianmoody/data-science-portfolio/master/edstats/plot_data/female_labor_share.csv", stringsAsFactors = FALSE)
#abroad_ed_df_app = read.csv(file = "https://raw.githubusercontent.com/indianmoody/data-science-portfolio/master/edstats/plot_data/foreign_education.csv", stringsAsFactors = FALSE)

un_fm_df_app = read.csv(file = "www/female_unemployment.csv", stringsAsFactors = FALSE)
un_ma_df_app = read.csv(file = "www/male_unemployment.csv", stringsAsFactors = FALSE)
labor_share_fm_df_app = read.csv(file = "www/female_labor_share.csv", stringsAsFactors = FALSE)
abroad_ed_df_app = read.csv(file = "www/foreign_education.csv", stringsAsFactors = FALSE)


countries = un_fm_df_app[,1]

plot_un_fm_app = function(country = "India") {
  
  # select row with 'country' details as dataframe
  temp_df = un_fm_df_app[un_fm_df_app$country_name == country, 3:ncol(un_fm_df_app)]
  # get transposed matrix of dataframe with years as rows
  temp_mat = t(temp_df)
  # clean row by removing 'x' from years and converting into numeric
  rownames(temp_mat) = sapply(rownames(temp_mat), function(x) as.numeric(gsub("x", "", x)))
  
  # plot
  plot(rownames(temp_mat), temp_mat[,1], type='o', xlab = 'Year', ylab = '% Unemployed Female')
  title(
    main = paste("Unemployed % of Female Labor Force: ", country, sep = ""),
    sub = "Unemployment is share of the labor force without work but available for and seeking employment."
  )
}

plot_un_ma_app = function(country = "India") {
  
  # select row with 'country' details as dataframe
  temp_df = un_ma_df_app[un_ma_df_app$country_name == country, 3:ncol(un_ma_df_app)]
  # get transposed matrix of dataframe with years as rows
  temp_mat = t(temp_df)
  # clean row by removing 'x' from years and converting into numeric
  rownames(temp_mat) = sapply(rownames(temp_mat), function(x) as.numeric(gsub("x", "", x)))
  
  # plot
  plot(rownames(temp_mat), temp_mat[,1], type='o', xlab = 'Year', ylab = '% Unemployed Male')
  title(
    main = paste("Unemployed % of Male Labor Force: ", country, sep = ""),
    sub = "Unemployment is share of the labor force without work but available for and seeking employment."
  )
}

plot_fm_labor_share_app = function(country = "India") {
  
  # select row with 'country' details as dataframe
  temp_df = labor_share_fm_df_app[labor_share_fm_df_app$country_name == country, 3:ncol(labor_share_fm_df_app)]
  # get transposed matrix of dataframe with years as rows
  temp_mat = t(temp_df)
  # clean row by removing 'x' from years and converting into numeric
  rownames(temp_mat) = sapply(rownames(temp_mat), function(x) as.numeric(gsub("x", "", x)))
  
  # plot
  plot(rownames(temp_mat), temp_mat[,1], type='o', xlab = 'Year', ylab = 'Female Share in %')
  title(
    main = paste("Female Labor Share in %: ", country, sep = ""),
    sub = "Female labor force as a percentage of the total labor force."
    )
}

plot_abroad_ed_app = function(country = "India") {
  
  # select row with 'country' details as dataframe
  temp_df = abroad_ed_df_app[abroad_ed_df_app$country_name == country, 3:ncol(abroad_ed_df_app)]
  # get transposed matrix of dataframe with years as rows
  temp_mat = t(temp_df)
  # clean row by removing 'x' from years and converting into numeric
  rownames(temp_mat) = sapply(rownames(temp_mat), function(x) as.numeric(gsub("x", "", x)))
  
  # plot
  plot(rownames(temp_mat), temp_mat[,1], type='o', xlab = 'Year', ylab = 'Students')
  title(
    main = paste("No. of Students Abroad: ", country, sep = ""),
    sub = "Students who crossed national border for education and are now enrolled outside their country of origin."
    )
}


intro_para = "This app plots stats for 172 countries over the years. The stats are related to male and female unemployment, female share of labor force and students studying outside of their country. Choose a country from drop-down menu below and explore its stats."


# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Unemployment, Gender Equality and Foreign Education"),
   
   tags$hr(),
   
   tags$p(intro_para),
   
   tags$br(),
   
   # Select Box
   selectInput(
     inputId = "country_selection", 
     label = "Choose a Country:", 
     choices = countries,
     selected = "India"
   ),
   
   tags$br(),
   
   
   fluidRow(
     column(6, plotOutput("plot1")),
     #column(2),
     column(6, plotOutput("plot2"))
   ),
   
   tags$br(),
   
   fluidRow(
     column(6, plotOutput("plot3")),
     #column(2),
     column(6, plotOutput("plot4"))
   ),
   
   tags$br(),
   
   tags$p("Labor force comprises people ages 15 and older who meet the International Labour Organization's definition of the economically active population."),
   
   tags$br(),
   tags$br()
   
   
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  #output$namess = renderPrint({input$country_selection})
  
  output$plot1 = renderPlot({plot_un_fm_app(input$country_selection)})
  output$plot2 = renderPlot({plot_un_ma_app(input$country_selection)})
  output$plot3 = renderPlot({plot_fm_labor_share_app(input$country_selection)})
  output$plot4 = renderPlot({plot_abroad_ed_app(input$country_selection)})
  
}

# Run the application 
shinyApp(ui = ui, server = server)

