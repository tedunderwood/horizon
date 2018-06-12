library(ggplot2)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
data <- read.csv('../salesdata/dataforC3Fig3.csv')

data$ratiomax[data$ratiomax > 10] <- 10

p <- ggplot(data, aes(x = year)) +
  geom_line(aes(y = ratio), color = 'black') +
  geom_ribbon(aes(ymin = ratiomin, ymax = ratiomax), fill = 'gray60', alpha = 0.4) +
  theme_bw() +
  labs(x = '', y = 'ratio') +
  scale_y_continuous(limits = c(0.5, 3.02)) +
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'), 
        legend.position = 'none')

tiff("~/Dropbox/book/chapter3/images/C3Fig3salesratio.tiff", height = 5, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)