causes <- read.csv('~/Dropbox/book/chapter1/plotdata/hardaverages.csv')
library(ggplot2)
library(dplyr)
library(scales)
levels(causes$genre) <- c('biography\n', 'fiction\n', 'poetry\n')
causes <- filter(causes, genre != 'poetry\n')

dates = c(1749, 1913)
hard = c(0.0163, 0.0708)
genre = c('fiction\n')
points = data.frame(year = dates, colorpct = hard, genre = genre)

p <- ggplot(causes, aes(x = year, y = hardpct, color = genre, shape = genre)) + 
  geom_smooth() + geom_point() +  
  scale_color_manual(name = 'genre\n', values = c('gray60', 'black'), 
                     guide = guide_legend(keyheight = 3.5,  label.vjust = 0, override.aes= list(size = 3))) + 
  scale_y_continuous('', labels = percent) + 
  scale_x_continuous("") + theme_bw() +
  annotate('text', x = 1700, y = 0.0755, label = 'Frequency of\nStanford "hard seeds"', 
           hjust = 0, family = 'Baskerville', size = 6.6) +
  theme(text = element_text(size = 24, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black')) +
  scale_shape_discrete(name = "genre\n",
                       guide = guide_legend(keyheight = 3.5,  label.vjust = 0, override.aes = list(linetype = 0, fill = NA)))
tiff("/Users/tunder/Dropbox/book/chapter1/images/C1Fig2stanford.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)