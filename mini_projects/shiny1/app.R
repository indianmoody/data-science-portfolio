#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Random Plots with Shiny"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
         sliderInput("squares",
                     "Number of squares:",
                     min = 10,
                     max = 50,
                     value = 30)
      ),
      
      # Show a plot of the generated distribution
      mainPanel(
         plotOutput("simplePlot")
      )
   )
)

foo = function(x) {
  return (x^3)
}

# Define server logic required to draw a histogram
server <- function(input, output) {
   
   output$simplePlot <- renderPlot({
      # generate bins based on input$bins from ui.R
      x <- 1:input$squares
      y <- foo(x)   
      
      
      # draw the histogram with the specified number of bins
      plot(x, y, type = 'b')
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

