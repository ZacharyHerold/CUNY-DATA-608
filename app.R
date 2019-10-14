#Question 1:
#  As a researcher, you frequently compare mortality rates from particular causes across
#different States. You need a visualization that will let you see (for 2010 only) the crude
#mortality rate, across all States, from one cause (for example, Neoplasms, which are effectively cancers). 
#Create a visualization that allows you to rank States by crude mortality for each cause of death.


# Loading package
#install.packages("plotly")
#install.packages("state")
library(plotly)
library(ggplot2)
library(shiny)
library(datasets)
library(shinythemes)

#Loading a built-in dataset that will map State to Region
data(state)
state <- as.data.frame(cbind(state.abb, state.region))
colnames(state)[1] <- "State"
levels(state$state.region) <- c("Northeast", "South", "Midwest","West") #Renaming the factor levels

#Loading the raw data from Github
url = 'https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv'
df = read.csv(url)
df2 <- merge(df, state)
df2$state.region[df2$State == "DC"] <- "South"  #Setting DC
summary(df2)


ui <- fluidPage(theme = shinytheme("yeti"),
  sidebarLayout(
    sidebarPanel(
      selectInput("disease", "Disease Type",
                  choices = levels(df2$ICD.Chapter),
                  multiple = FALSE,
                  selected = "Neoplasms"),
      selectInput("year", "Year",
                  choices = levels(factor(df2$Year)),
                  selected = 2010),
      radioButtons("sort_type", "Sort Type",
                   choices = c("sort nation-wide", "sort by region"),
                  selected = "sort nation-wide")
    ),
    mainPanel(
      plotlyOutput("plot")
    )
  )
)

server <- function(input, output) {
  output$plot <- renderPlotly({
    ggplotly({
      
      data <- subset(df2,
                     ICD.Chapter == input$disease & Year == input$year)
      
      if (input$sort_type == "sort nation-wide"){
        p <- ggplot(data) +
          geom_linerange(aes(x = reorder(State, Crude.Rate), ymin = 0, ymax = Crude.Rate, color = state.region)) +
          geom_point(aes(x = reorder(State, Crude.Rate), y = Crude.Rate, color = state.region)) 

      } else {
        data2 <- data.frame(data[order(data$state.region, data$Crude.Rate),]) #Ordering first by region, then mortality rate
        data2$State <- factor(data2$State, levels = data2$State) #Lock in order of states
        p <- ggplot(data2) +
          geom_linerange(aes(x = State, ymin = 0, ymax = Crude.Rate, color = state.region)) +
          geom_point(aes(x = State, y = Crude.Rate, color = state.region)) 
      }
      
      p + 
        ggtitle("State Mortality by Disease") +
        xlab("State") +
        ylab("Crude Rate (per 100K population)") +
        coord_flip() +
        theme_light() + 
        scale_color_brewer(palette = "RdYlBu")
        }, height = 600, width = 600)
  })
}

shinyApp(ui = ui, server = server)

#rsconnect::deployApp('C:\\Users\\zhero\\Desktop\\CUNY\\DATA608\\module3')



