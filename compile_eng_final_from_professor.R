setwd("C:/Users/USER/Documents/Intl Finance F22/Word Cloud Exercise Files")

install.packages("dplyr")
install.packages("rvest")
install.packages("stringr")
install.packages("tm")
install.packages('readtext')
install.packages("wordcloud")

library(dplyr)
library(rvest) 
library(stringr) 
library(readtext)
library(wordcloud)
library(tm)

#creating url
url_0 = "https://news.google.com/search?q="
keyword = "fed" #if keywords contain multiple words, "%20" must go in between the words, ex. china%20usa
url_1 = "&hl=en-US&gl=US&ceid=US%3Aen"
url <- paste0(url_0, keyword, url_1)
print(url)

#extracting headlines
google_news <- read_html(url)
articles <- google_news %>% html_nodes("article")
#due to search settings of Google News, the maximum number of articles  that can be used = 101

headlines <- articles %>%
  html_nodes("a.DY5T1d") %>%
  html_text()

#saving headlines into txt file
print(headlines)
writeLines(headlines, "headlines_eng.txt") 

#finding frequent words in headlines and their frequencies
set <- Corpus(VectorSource(headlines))
set <- set %>%
  tm_map(removeNumbers) %>%
  tm_map(removePunctuation) %>%
  tm_map(stripWhitespace)
set <- tm_map(set, content_transformer(tolower))
set <- tm_map(set, removeWords, stopwords("english"))

term <- TermDocumentMatrix(set) 
matrix <- as.matrix(term) 

words <- sort(rowSums(matrix),decreasing=TRUE) 
df_words <- data.frame(word = names(words),freq=words)
View(df_words)

#creating word clouds
pal<-brewer.pal(8, "Set1")
wordcloud(words = df_words$word, 
          freq = df_words$freq, 
          min.freq = 1,
          max.words=500, 
          random.order=FALSE, 
          rot.per=0.35,
          scale = c(5, 0.3),
          colors = pal)
