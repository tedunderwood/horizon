# Make unweighted meantime graph
library(ggplot2)
library(dplyr)
times <- read.csv('../plotdata/averagetimes.csv')

timebreaks = c(-4.82, -2.81, -1.43, 0.365, 1.75, 3.7, 5.08, 7.650835)
timelabels = c('2 min', '15 min', 'an hour', '6 hours', 'a day', 'a week', 'a month', 'a year')
times$col <- as.character(times$col)
times$col[times$col != 'red'] <- '\nfiction\n'
times$col[times$col == 'red'] <- '\nbiography and\nautobiography\n'

p <- ggplot(times, aes(x = date, y = meantime, shape = col, linetype = col)) + geom_point() + 
  geom_smooth(color = 'black', show.guides = FALSE) +
  theme_bw() + scale_linetype_manual(guide = 'none', values = c('dashed', 'solid')) +
  scale_y_continuous('', breaks = timebreaks, labels = timelabels) +
  scale_x_continuous('', breaks = c(1719, 1800, 1900, 2000)) +
  scale_shape_manual(name = 'genre\n', values = c(1, 17)) +
  theme(text = element_text(size = 20, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black')) +
  annotate('text', x = 1715, y = 9.55, label = 'mean time narrated\nin 250 words', 
           hjust = 0, family = "Avenir Next Medium", size = 5)
tiff("../images/C1Fig5pace.tiff", height = 5.5, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)
