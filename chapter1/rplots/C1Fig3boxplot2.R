# boxplot

d2 <- read.csv('/Users/tunder/Dropbox/book/chapter1/modeloutput/finalbiopredicts.csv')
library(ggplot2)
library(scales)

p <- ggplot(d2, aes(x = as.numeric(center), y = accuracy)) + theme_bw() +
  geom_point(fill = 'gray85', position = position_jitter(height = 0, width = 7), shape = 23, size =2) +
  scale_y_continuous('', labels = percent) +
  scale_x_continuous('mean date of volumes modeled', breaks = c(1700, 1750, 1800, 1850, 1900,
                                                  1950, 2000), limits = c(1700, 2000)) +
  theme_bw() +
  annotate('text', x = 1700, y = 0.99, label = 'Predictive\naccuracy', 
           hjust = 0, family = "Avenir Next Medium", size = 6) +
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        axis.title.x = element_text(margin = margin(t = 14)))
tiff("/Users/tunder/Dropbox/book/chapter1/images/C1Fig3boxplot.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)