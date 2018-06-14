library(ggplot2)
library(scales)
library(dplyr)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

hathi <- read.csv('../data/corrected_hathi_summaries.csv')
hathi <- arrange(hathi, date)
hathi <- filter(hathi, date < 2008, date > 1799)

onlyboys <- filter(hathi, chargender == 'm')
boysbyyear <- group_by(onlyboys, date)
boysperyear <- summarise(boysbyyear, total = sum(total))
onlygirls <- filter(hathi, chargender == 'f')
girlsbyyear <- group_by(onlygirls, date)
girlsperyear <- summarise(girlsbyyear, total = sum(total))

ratioanddates <- function(femwords, mascwords) {
  ratios = c()
  dates = c()
  for (i in seq(1800, 2007)) {
    if (!(i %in% femwords$date) & !(i %in% mascwords$date)) next
    totalwords = femwords$total[femwords$date == i] + mascwords$total[mascwords$date == i]
    if (totalwords < 1) next
    ratio = femwords$total[femwords$date == i] / totalwords
    ratios <- c(ratios, ratio)
    dates <- c(dates, i)
  }
  return(list(first=dates, second=ratios))
}

result <- ratioanddates(girlsperyear, boysperyear)
hathidates <- result$first
hathiratio <- result$second

chicago <-read.csv('../data/chicago_summary.csv')

chic <- arrange(chicago, date)

onlyboys <- filter(chic, chargender == 'm')
boysbyyear <- group_by(onlyboys, date)
boysperyear <- summarise(boysbyyear, total = sum(total))
onlygirls <- filter(chic, chargender == 'f')
girlsbyyear <- group_by(onlygirls, date)
girlsperyear <- summarise(girlsbyyear, total = sum(total))

result <- ratioanddates(girlsperyear, boysperyear)
chidates <- result$first
chicagoratio <- result$second

df <- data.frame(date = c(chidates, hathidates), 
                 womenratio = c(chicagoratio, hathiratio), 
                 source = as.factor(c(rep('Chicago', length(chidates)),
                                    rep('Hathi', length(hathidates)))))
p <- ggplot(df, aes(x = date, y = womenratio, color = source, shape = source, alpha = source)) + 
  geom_point() + scale_x_continuous("") + 
  scale_alpha_manual(name = 'source\n', values = c(1, 0.6),
                     guide = guide_legend(keyheight = 2, label.vjust = 0.6)) +
  scale_colour_manual(name = 'source\n', values = c('red', 'gray40'),
                      guide = guide_legend(keyheight = 2, label.vjust = 0.6)) + 
  scale_shape_manual(name = 'source\n', values = c(17,19), 
                     guide = guide_legend(keyheight = 2, label.vjust = 0.6, 
                                          override.aes = list(size = 2))) +
  scale_y_continuous("", labels=percent, limits = c(0, 0.58)) + theme_bw() +
  ggtitle('Percentage of words used in\ncharacterization that describe women') +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1))

tiff("../images/C4Fig8wordsabtwomenRED.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)