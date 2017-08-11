# Make unweighted meantime graph
library(scales)
library(ggplot2)
library(dplyr)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

sfpace <- read.csv('../plotdata/paceofchangeinSF.tsv', sep = '\t')
detectpace <- read.csv('../plotdata/paceofchangeinDetective.tsv', sep = '\t')
sfpace$genre <- 'SF'
detectpace$genre <- 'detective'
allpace <- rbind(sfpace, detectpace)
allpace$iteration <- as.factor(allpace$iteration)

p <- ggplot(allpace, aes(x = date, y = difference, shape = iteration, color = genre, linetype = genre)) + 
  scale_color_manual(values = c('gray50', 'black')) +
  geom_line(size = 1) +
  theme_bw() + scale_y_continuous('', labels = percent) +
  scale_x_continuous('', breaks = c(1890, 1910, 1930, 1950, 1970)) +
  ggtitle('Accuracy a model loses in 30 years') +
  theme(plot.title = element_text(hjust = -0.12, size = 18, vjust = 1.5)) +
  theme(text = element_text(size = 18, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        axis.title.x = element_text(margin = margin(t = 14), size = 16)) +
  scale_color_manual(name = 'genre\n', values = c('gray60', 'black'),
                     guide = guide_legend(keyheight = 3,  label.vjust = 0.55, 
                                          override.aes = list(fill = NA, size = 1))) +
  scale_shape_discrete(name = 'genre\n') +
  scale_linetype_discrete(name = 'genre\n')

tiff("../images/C2Fig3paceofchange.tiff", height = 5.5, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)

plot(p)