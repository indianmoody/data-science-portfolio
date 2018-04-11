
library(shiny)
library(plotly)

company = c("Alphabet", "Apple", "Amazon")
company_value = c(745.1, 849.2, 702.5)
ceo = c("Larry Page", "Tim Cook", "Jeff Bezos")
ceo_net_worth = c(47.8, 0.625, 117)

df = data.frame(company, company_value, ceo, ceo_net_worth)

df$hover = with(df, paste("CEO: ", ceo, "<br>", "CEO Net Worth: $", ceo_net_worth, "B"))


ui <- fluidPage(
   
   # Application title
   titlePanel("Sample Shiny app"),
   
   fluidRow(
       column(3),
       column(6, plotOutput("basicBarPlot"))
   ),
   
   hr(),
   
   fluidRow(
       column(3),
       column(6, plotlyOutput("basicPlotly"))
   )
   
)


server <- function(input, output) {
   
   output$basicBarPlot <- renderPlot({
      barplot(df$company_value, names.arg = df$company) %>%
           title(main = "Most Valuable Comapnies (Billion USD)")
   })
   
   output$basicPlotly <- renderPlotly({
       
       plot_ly(df, x = ~company, y = ~company_value, type = 'bar', text = ~hover, color = I("#58F1C3")) %>%
           layout(title = "Most Valuable Companies (Billion USD)") %>%
           config(displayModeBar = F)
       
   })
   
}

# Run the application 
shinyApp(ui = ui, server = server)

