library(scales)
library(ggplot2)
library(dplyr)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
l <- read.csv('../plotdata/the900.csv')

reviewd <- as.factor(l$realclass)
levels(reviewd) <- c('not', 'rev')
l$reviewed <- reviewd
levels(l$reviewed) = c('biography\n', 'fiction\n')
l$volid <- as.character(l$volid)
l$size <- (rep(1, length(l$reviewed)))
l$size[l$volid == 'mdp.39015056795308' | l$volid == 'uc2.ark+=13960=t5h99113n' | l$volid == 'uc1.$b404097'] <- 3

p <- ggplot(l, aes(x = dateused, y = logistic, color = reviewed, shape = reviewed)) + 
  geom_point(aes(size = size)) + geom_smooth() + 
  scale_color_manual(name = 'actually\n', values = c('gray60', 'black'),
                     guide = guide_legend(keyheight = 3,  label.vjust = -0.4, override.aes = list(linetype = 0, fill = NA, size = 3))) + 
  theme(text = element_text(size = 24)) + scale_size(guide = FALSE, range = c(1.5,3.5)) +
  scale_y_continuous('', labels = percent, breaks = c(0.3, 0.4, 0.5, 0.6, 0.7)) + 
  scale_x_continuous("") + theme_bw() +
  annotate('text', x = 1700, y = 0.7, label = 'Probability of\nbeing fiction', 
           hjust = 0, family = 'Baskerville', size = 6.5) +
  theme(text = element_text(size = 24, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black')) +
  scale_shape_discrete(name = "actually\n")

tiff("/Users/tunder/Dropbox/book/chapter1/images/C1Fig4probabilities.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)