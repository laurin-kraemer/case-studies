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

# Import data
kayak <- read_excel("Spreadsheet_Data.xls", 
                    sheet = "Kayak")

doubleclick <- read_excel("Spreadsheet_Data.xls", 
                          sheet = "DoubleClick")

#Convert to dataframe
doubleclick <- as.data.frame(doubleclick)

#Look for weird stuff
table(doubleclick$`Match Type`)

# The NAs have to be removed.
doubleclick_clean <- na.omit(doubleclick)

# Notice how the number of rows gets reduced 
print(nrow(doubleclick_clean))

# Look for Spelling mistakes
unique(doubleclick_clean $`Bid Strategy`)

# Replace Typos
doubleclick_clean$`Bid Strategy` <- gsub("Postiion 1-4 Bid Strategy","Position 1-4 Bid Strategy",doubleclick_clean$`Bid Strategy`)

doubleclick_clean$`Bid Strategy` <- gsub("Position 1 -2 Target","Position 1-2 Target",doubleclick_clean$`Bid Strategy`)

# Create data set for analysis
sem <- doubleclick_clean[,c('Campaign','Keyword','Keyword Group','Publisher Name', 'Bid Strategy','Engine Click Thru %','Match Type','Trans. Conv. %','Total Cost/ Trans.','Impressions')]






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
