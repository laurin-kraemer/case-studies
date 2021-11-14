#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(

    # Application title
    titlePanel("Marketing Campaign"),

    # Sidebar with a slider input for number of bins
    sidebarLayout(
        sidebarPanel(
            sliderInput("bins",
                        "Number of bins:",
                        min = 1,
                        max = 50,
                        value = 30),
            selectInput('num_col',"Select Variable to plot",colnames(num_cols))
            
        ),
        # Show a plot of the generated distribution
        mainPanel(
            plotOutput("age_hist"),
            verbatimTextOutput('age_dist'),
            textOutput("age_min"),
            dataTableOutput('data')

        )
    )
))
