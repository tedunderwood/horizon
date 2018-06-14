library(ggplot2)
library(scales)
library(dplyr)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

errors <- read.csv('../dataforR/pubweeklyerrorbars.csv')
hathi <- read.csv('../dataforR/authorratios_nojuv.csv')

p <- ggplot() + 
  geom_errorbar(data=errors, mapping=aes(x=year, ymin=low, ymax=high), width=5, size=1, color="black") + 
  geom_point(data=errors, mapping=aes(x=year, y=mean), size=4, shape=21, fill="white") +
  geom_point(data = hathi, mapping = aes(x = year, y = authratio), shape = 18, size = 2, alpha = 0.5) + 
  ylab('') +
  scale_y_continuous(labels = percent, limits = c(0, 0.8)) +
  xlab('') +
  xlim(1800, 2007) + 
  theme_bw() +
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'))

tiff("../images/C4Fig9pubweekly_nojuv.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)