# Plotting words

library(scales)
library(ggplot2)
library(reshape2)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

df <- read.csv('../dataforR/diff_matrix.csv')
df <- df[df$thedate > 1799, ]

subset <- select(df, thedate, eyes, hair, chest, pocket)

longform <- melt(subset, id.vars = c('thedate'))

p <- ggplot(longform, aes(x = thedate, y = value, color = variable, shape = variable, linetype = variable)) + 
  geom_point() + geom_smooth(span = 0.4, se = FALSE, show.legend = FALSE) +
  scale_linetype_manual(guide = 'none', values = c('solid', 'solid', 'dashed', 'dashed')) +
  scale_color_manual(name = 'word\n', values = c('black', 'gray60', 'black', 'gray40')) +
  scale_shape_manual(name = 'word\n', values = c(16, 15, 2, 3)) +
  theme(text = element_text(size = 17)) + 
  scale_y_continuous('m  <==  frequency difference  ==>  f') +
  scale_x_continuous("", breaks = c(1800,1850,1900,1950,2000)) +
  theme_bw() + 
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        legend.position = 'none') +
  annotate('text', x = 1980, y = 19.5, label = 'hair', 
           hjust = 0, family = "Avenir Next Medium", size = 7, color = 'gray50') +
  annotate('text', x = 1855, y = 33, label = 'eyes', 
           hjust = 0, family = "Avenir Next Medium", size = 7, color = 'black') +
  annotate('text', x = 1964, y = -0.4, label = 'chest', 
           hjust = 0, family = "Avenir Next Medium", size = 7, color = 'black') +
  annotate('text', x = 1876, y = -7, label = 'pocket', 
           hjust = 0, family = "Avenir Next Medium", size = 7, color = 'gray30')

tiff("../images/C4Fig6eyeshairchest.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)