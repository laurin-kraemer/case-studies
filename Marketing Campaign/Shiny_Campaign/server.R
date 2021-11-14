# Import Libraries
library(shiny)
library(readr)

# Import data
data <- read_csv("data.csv")
data <- as.data.frame(data)

# Filter
bool <- sapply(data,is.numeric)
num_cols <- data[,bool]

# Define server logic required to draw a histogram
shinyServer(function(input, output) {

    output$age_hist <- renderPlot({

        # generate bins based on input$bins from ui.R
        col <- as.character(input$num_col)
        x <- num_cols[,col]
        bins <- seq(min(x), max(x), length.out = input$bins + 1)

        # draw the histogram with the specified number of bins
        hist(x, breaks = bins, col = 'darkgray', border = 'white')

    })
    
    output$age_dist <- renderPrint({
      col <- as.character(input$num_col)
      summary(data[,col])
    })
  
    
    output$age_min <- renderText({
      
      c("The oldest customer got born in the year",min(data[,2]))
    })
    
    output$data <- renderDataTable(data, options=list(pageLength=5))


})
