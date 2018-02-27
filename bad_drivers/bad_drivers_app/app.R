#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(plotly)

# load data into csv
df = read.csv(file = "www/bad_drivers_data.csv", stringsAsFactors = FALSE)

#change column names, originals are too long
colnames(df) = c("state", "drivers_per_billion", "perc_drivers_speeding", "perc_drivers_alcohol", "perc_drivers_not_distracted", "perc_drivers_first_time", "car_ins_premium", "loss_ins_company")

# drop District of Columbia because of map limitations
df = df[-9,]

# ---------- functions for State tabPanel ----------------------------

# function to plot drivers per billion in state
plot_drivers_per_billion_state = function(state = "Colorado") {
  
  avg = mean(df$drivers_per_billion)
  curr = df[df$state == state, "drivers_per_billion"]
  curr_vec = c(curr, avg)
  names(curr_vec) = c(state, "Country Average")
  
  barplot(
    curr_vec,
    main = "No. of drivers involved in fatal collisions per billion miles",
    ylab = "No. of Drivers",
    col=c("#EFB8F4", "#B8CEF4")
  )
  
}

# function to plot pie chart for perc driver speeding in state
plot_drivers_speeding_state = function(state = "Colorado") {
  
  curr = df[df$state == state, "perc_drivers_speeding"]
  complement = 100 - curr
  
  pie(
    c(curr, complement),
    labels = c("Speeding", "Not Speeding"),
    main = "% of Drivers Involved In Fatal Collisions Who Were Speeding",
    col = c('#C6EEA2', '#FFFFFF')
  )
  
}

# function to plot pie chart for perc driver alcohol in state
plot_drivers_alcohol_state = function(state = "Colorado") {
  
  curr = df[df$state == state, "perc_drivers_alcohol"]
  complement = 100 - curr
  
  pie(
    c(curr, complement),
    labels = c("Alcohol-Impaired", "Not Alcohol-Impaired"),
    main = "% Of Drivers Involved In Fatal Collisions Who Were Alcohol-Impaired",
    col = c('#C6EEA2', '#FFFFFF')
  )
  
}

# funtion to plot perc driver not distracted in state
plot_drivers_not_distracted_state = function(state = "Colorado") {
  
  curr = df[df$state == state, "perc_drivers_not_distracted"]
  complement = 100 - curr
  
  pie(
    c(curr, complement),
    labels = c("Not Distracted", "Distracted"),
    main = "% Of Drivers Involved In Fatal Collisions Who Were Not Distracted",
    col = c('#C6EEA2', '#FFFFFF')
  )
  
}

# function to plot perc drivers first time in state
plot_drivers_first_time_state = function(state = "Colorado") {
  
  curr = df[df$state == state, "perc_drivers_first_time"]
  complement = 100 - curr
  
  pie(
    c(curr, complement),
    labels = c("No History", "History"),
    main = "% Of Drivers Involved In Fatal Collisions With No History of Accidents",
    col = c('#C6EEA2', '#FFFFFF')
  )
  
}
# ------------------------------------------------------------------

# ----------------- functions for Insurance tabPanel -------------------

# function to plot car insurance premium in state
car_insurance_premium = function(state = "Colorado") {
  
  avg = mean(df$car_ins_premium)
  curr = df[df$state == state, "car_ins_premium"]
  curr_vec = c(curr, avg)
  names(curr_vec) = c(state, "Country Average")
  
  barplot(
    curr_vec,
    main = "Car Insurance Premiums ($)",
    ylab = "Insurance Premium",
    col=c("#EFB8F4", "#B8CEF4")
    
  )
  
}


# function to plot loss by insurance companies per insured driver

loss_insurance_company = function(state = "Colorado") {
  
  avg = mean(df$loss_ins_company)
  curr = df[df$state == state, "loss_ins_company"]
  curr_vec = c(curr, avg)
  names(curr_vec) = c(state, "Country Average")
  
  barplot(
    curr_vec,
    main = "Loss to insurance companies for collisions per insured driver ($)",
    ylab = "Loss Per Driver",
    col=c("#EFB8F4", "#B8CEF4")
    
  )
  
}

# -----------------------------------------------------------------

# ----------------------- UI ----------------------------------

# Define UI for application that draws a histogram
ui <- navbarPage(
   
  # Application title
  "Bad Drivers in US",
  
  fluid = TRUE,
  
  #------------------ TAB PANEL 1 STARTS ---------------------------#
  tabPanel(
    "Country Data",
    
    navlistPanel(
      "Accident Statistics",
      
      tabPanel(
        "Drives in Accident per billion",
        plotlyOutput("driver_billion_map")
      ),
      
      tabPanel(
        "Drivers with Speeding",
        plotlyOutput("driver_speeding_map")
      ),
      
      tabPanel(
        "Drivers with Alchol",
        plotlyOutput("driver_alcohol_map")
      ),
      
      tabPanel(
        "Drivers Not Distracted",
        plotlyOutput("driver_not_distracted_map")
      ),
      
      tabPanel(
        "Drivers First Time Accident",
        plotlyOutput("driver_first_time_map")
      )
      
    )
    
  ),
  
  #------------------ TAB PANEL 1 ENDS ---------------------------#
  
  
  #------------------ TAB PANEL 2 STARTS ---------------------------#
  tabPanel(
    "State Data",
    
    tags$hr(),
    
    selectInput(
      inputId = "state_selection", 
      label = "Choose a State:", 
      choices = df$state,
      selected = "Colorado"
    ),
    
    tags$hr(),
    
    fluidRow(
      column(3),
      column(5, plotOutput("driver_billion_state"))
    ),
    
    
    tags$hr(),
    
    fluidRow(
      column(1),
      column(5, plotOutput("perc_drivers_speeding")),
      column(5, plotOutput("perc_drivers_alcohol")),
      column(1)
    ),
    
    tags$hr(),
    
    fluidRow(
      column(1),
      column(5, plotOutput("perc_drivers_not_distracted")),
      column(5, plotOutput("perc_drivers_first_time")),
      column(1)
    )
    
  ),
  
  #------------------ TAB PANEL 2 ENDS ---------------------------#
  
  
  #------------------ TAB PANEL 3 STARTS ---------------------------#
  tabPanel(
    "Insurance Data",
    
    selectInput(
      inputId = "state_selection2", 
      label = "Choose a State:", 
      choices = df$state,
      selected = "Colorado"
    ),
    
    tags$hr(),
    
    tags$hr(),
    
    fluidRow(
      column(1),
      column(5, plotOutput("car_ins_premium")),
      column(5, plotOutput("loss_ins_company")),
      column(1)
    )
    
  )
  #------------------ TAB PANEL 3 ENDS ---------------------------# 
   
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  output$driver_billion_map = renderPlotly({
    g <- list(
      scope = 'usa',
      projection = list(type = 'albers usa'),
      showlakes = TRUE,
      lakecolor = toRGB('white')
    )
    
    plot_geo(df, locationmode = 'USA-states') %>%
      add_trace(
        z = ~drivers_per_billion, text = ~state.name, locations = ~state.abb,
        color = ~drivers_per_billion, colors = 'GnBu'
      ) %>% 
      colorbar(title = "No. of Drivers") %>%
      layout(
        title = 'Number of drivers involved in fatal collisions per billion miles',
        geo = g
      )
  })
  
  
  output$driver_speeding_map = renderPlotly({
    g <- list(
      scope = 'usa',
      projection = list(type = 'albers usa'),
      showlakes = TRUE,
      lakecolor = toRGB('white')
    )
    
    plot_geo(df, locationmode = 'USA-states') %>%
      add_trace(
        z = ~perc_drivers_speeding, text = ~state.name, locations = ~state.abb,
        color = ~perc_drivers_speeding, colors = 'GnBu'
      ) %>% 
      colorbar(title = "% of Drivers") %>%
      layout(
        title = 'Percentage Of Drivers Involved In Fatal Collisions Who Were Speeding',
        geo = g
      )
  })
  
  
  output$driver_alcohol_map = renderPlotly({
    g <- list(
      scope = 'usa',
      projection = list(type = 'albers usa'),
      showlakes = TRUE,
      lakecolor = toRGB('white')
    )
    
    plot_geo(df, locationmode = 'USA-states') %>%
      add_trace(
        z = ~perc_drivers_alcohol, text = ~state.name, locations = ~state.abb,
        color = ~perc_drivers_alcohol, colors = 'GnBu'
      ) %>% 
      colorbar(title = "% of Drivers") %>%
      layout(
        title = 'Percentage Of Drivers Involved In Fatal Collisions Who Were Alcohol-Impaired',
        geo = g
      )
  })
  
  
  output$driver_not_distracted_map = renderPlotly({
    g <- list(
      scope = 'usa',
      projection = list(type = 'albers usa'),
      showlakes = TRUE,
      lakecolor = toRGB('white')
    )
    
    plot_geo(df, locationmode = 'USA-states') %>%
      add_trace(
        z = ~perc_drivers_not_distracted, text = ~state.name, locations = ~state.abb,
        color = ~perc_drivers_not_distracted, colors = 'GnBu'
      ) %>% 
      colorbar(title = "% of Drivers") %>%
      layout(
        title = 'Percentage Of Drivers Involved In Fatal Collisions Who Were Not Distracted',
        geo = g
      )
  })
  
  
  output$driver_first_time_map = renderPlotly({
    g <- list(
      scope = 'usa',
      projection = list(type = 'albers usa'),
      showlakes = TRUE,
      lakecolor = toRGB('white')
    )
    
    plot_geo(df, locationmode = 'USA-states') %>%
      add_trace(
        z = ~perc_drivers_first_time, text = ~state.name, locations = ~state.abb,
        color = ~perc_drivers_first_time, colors = 'GnBu'
      ) %>% 
      colorbar(title = "% of Drivers") %>%
      layout(
        title = 'Percentage Of Drivers Involved In Fatal Collisions Who Had Not Been Involved In Any Previous Accidents',
        geo = g
      )
  })
  
  
  output$driver_billion_state = renderPlot({plot_drivers_per_billion_state(input$state_selection)})
  output$perc_drivers_speeding = renderPlot({plot_drivers_speeding_state(input$state_selection)})
  output$perc_drivers_alcohol = renderPlot({plot_drivers_alcohol_state(input$state_selection)})
  output$perc_drivers_not_distracted = renderPlot({plot_drivers_not_distracted_state(input$state_selection)})
  output$perc_drivers_first_time = renderPlot({plot_drivers_first_time_state(input$state_selection)})
  
  
  output$car_ins_premium = renderPlot({car_insurance_premium(input$state_selection2)})
  output$loss_ins_company = renderPlot({loss_insurance_company(input$state_selection2)})
  
}

# Run the application 
shinyApp(ui = ui, server = server)

