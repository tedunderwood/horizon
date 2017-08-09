library(ggplot2)
library(scales)

causes <- read.csv('~/Dropbox/book/chapter1/plotdata/colorfic.csv')
causes$class <- as.factor(causes$class)
levels(causes$class) <- c('random\n', 'reviewed\n')
causes$size <- (rep(2, length(causes$class)))
causes$size[causes$docid == 'mdp.39015056795308' | causes$docid == 'uc2.ark+=13960=t5h99113n'] <- 3

p <- ggplot(causes, aes(x = date, y = colors)) + geom_smooth(color = 'gray30') +
  geom_point(aes(color = class, shape = class, size = size)) + 
  scale_shape(name="fiction\n", 
              guide = guide_legend(keyheight = 3,  label.vjust = -0.2, override.aes= list(size = 3))) + 
  scale_size(guide = FALSE, range = c(2,4)) +
  scale_y_continuous('', labels = percent) + 
  scale_x_continuous("") + theme_bw() +
  annotate('text', x = 1700, y = 0.00655, label = 'Frequency of\ncolor terms', 
           hjust = 0, size = 6.6, family = 'Baskerville') +
  theme(text = element_text(size = 24, color = 'black', family = 'Baskerville'), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black')) +
  scale_color_manual(name = "fiction\n", values = c('gray55', 'black'), 
                     guide = guide_legend(keyheight = 3,  label.vjust = -0.2))
tiff("/Users/tunder/Dropbox/book/chapter1/images/C1Fig1colors.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)