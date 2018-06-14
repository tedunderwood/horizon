# Predictive accuracy by decade

library(scales)
library(ggplot2)
library(dplyr)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

d2 <- read.csv('../dataforR/decade_optimums.tsv', sep = '\t')
library(ggplot2)
library(scales)

p <- ggplot(d2, aes(x = decade, y = accuracy)) + 
  geom_point(color = 'black', alpha = 0.6, shape = 23, fill = 'gray70', size = 2.5) +
  scale_y_continuous('accuracy', labels = percent) +
  xlab('') + 
  theme_bw() + 
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'))

tiff("../images/C4Fig1accuracy.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)