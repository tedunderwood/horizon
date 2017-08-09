# boxplot

d2 <- read.csv('/Users/tunder/Dropbox/python/results/biopredictsII.csv')
library(ggplot2)
library(scales)

p <- ggplot(d2, aes(x = as.factor(floor), y = accuracy)) + theme_bw() +
  geom_boxplot(fill = 'gray85') +
  scale_y_continuous('', labels = percent) +
  scale_x_discrete('first year in a 30-year span', breaks = c('1700', '1730', '1760', '1790', '1820', '1850', '1880', '1910',
                                  '1940', '1970')) +
  theme_bw() +
  annotate('text', x = '1700', y = 0.99, label = 'Predictive\naccuracy', 
           hjust = 0, family = 'Baskerville', size = 6.8) +
  theme(text = element_text(size = 24, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        axis.title.x = element_text(margin = margin(t = 14)))
tiff("/Users/tunder/Dropbox/book/chapter1/images/C1Fig3boxplot.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)