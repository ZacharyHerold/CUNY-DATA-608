#Question 2:
#  Often you are asked whether particular States are improving their mortality rates (per cause)
#faster than, or slower than, the national average. Create a visualization that lets your clients
#see this for themselves for one cause of death at the time. Keep in mind that the national
#average should be weighted by the national population.


# Loading package
#install.packages("plotly")
#install.packages("state")
#install.packages("shinythemes")
library(plotly)
library(ggplot2)
library(shiny)
library(shinythemes)
library(plyr)


#Loading the raw data from Github
url = 'https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv'
df = read.csv(url)

#Compiling nation-wide data grouped by disease and year
groupColumns = c("ICD.Chapter", "Year")
deaths_ttl = ddply(df, groupColumns, summarise, deaths_ttl = sum(Deaths))
pop_ttl = ddply(df, groupColumns, summarise, pop_ttl = sum(Population))
nation_data <- join(deaths_ttl, pop_ttl)
nation_data$nation_crude <- round(nation_data$deaths_ttl/ nation_data$pop_ttl * 100000,2)
#tail(nation_data)

#Merging state and nation-wide data
df2 <- join(df, nation_data)
#head(df2, 100)

ui <- fluidPage(theme = shinytheme("flatly"),
  sidebarLayout(
    sidebarPanel(
      selectInput("state", "State",
                  choices = levels(df2$State),
                  selected = "NY"),
      selectInput("disease", "Disease Type",
                  choices = levels(df2$ICD.Chapter),
                  multiple = FALSE,
                  selected = "Neoplasms")
    ),
    mainPanel(
      plotlyOutput("plot")
    )
  )
)

server <- function(input, output) {
  output$plot <- renderPlotly({
    ggplotly({
      
      data <- subset(df2, ICD.Chapter == input$disease & State == input$state)
      
      p <- ggplot(data, aes(x=Year)) +
        geom_area(aes(y = Crude.Rate), fill = "darkblue", color = "darkblue", alpha = 0.8) + 
        geom_point(aes(y = Crude.Rate), color = "black") + 
        geom_area(aes(y = nation_crude), fill = "#D3D3D3", color = "#999999", linetype="twodash", alpha = 0.5) + 
        ggtitle("Trends in Mortality Rates\n  State (blue) vs. National (grey)") +
        ylim(0,max(data$Crude.Rate,data$nation_crude) *1.2) +
        xlab("Year") +
        ylab("Mortality Rate per 100K population") +
        #guides(fill = guide_legend()) +
        theme_minimal() 
    }, height = 500, width = 800)
  })
}

shinyApp(ui = ui, server = server)

# rsconnect::deployApp('C:\\Users\\zhero\\Desktop\\CUNY\\DATA608\\module3b')



