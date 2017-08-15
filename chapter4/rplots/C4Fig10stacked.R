library(ggplot2)
library(scales)
library(dplyr)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
areas <- read.csv('~/Dropbox/python/character/dataforR/nonfiction_stack_graph.csv')

p = ggplot(areas, aes(x=year, y=fraction, fill=genre)) + 
  scale_y_continuous('', labels = percent) + xlab('') +
  geom_area(colour = 'black', size = .3, alpha = 0.75) + 
  scale_fill_manual(name = 'genre\n', values = c('gray10', 'gray75'),
                    guide = guide_legend(keyheight = 2)) +
  ggtitle('Books by women, as a fraction of all books') +
  theme_bw() +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16))

tiff("../images/C4Fig10stacked.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)