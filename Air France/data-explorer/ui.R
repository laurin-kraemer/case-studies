#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(readxl)
library(tidyverse)

# Inspect sheets of excel-file
excel_sheets('C:/Users/LK/Nextcloud7/Personal/Docs/case-studies/Air France/assets/Air France Case Spreadsheet Supplement.xls')

# Import data
kayak <- read_excel("C:/Users/LK/Nextcloud7/Personal/Docs/case-studies/Air France/assets/Air France Case Spreadsheet Supplement.xls", 
                                                     sheet = "Kayak")

doubleclick <- read_excel("C:/Users/LK/Nextcloud7/Personal/Docs/case-studies/Air France/assets/Air France Case Spreadsheet Supplement.xls", 
                         sheet = "DoubleClick")


# Define UI for application that draws a histogram
shinyUI(fluidPage(

    # Application title
    titlePanel("Old Faithful Geyser Data"),

    # Sidebar with a slider input for number of bins
    sidebarLayout(
        sidebarPanel(
            sliderInput("bins",
                        "Number of bins:",
                        min = 1,
                        max = 50,
                        value = 30)
        ),

        # Show a plot of the generated distribution
        mainPanel(
            plotOutput("distPlot")
        )
    )
))
