library(scales)
library(ggplot2)
library(dplyr)
l <- read.csv('../modeloutput/allSF.csv')
l$realclass <- as.character(l$realclass)
l$realclass[l$realclass == '1'] <- 'SF'
l$realclass[l$realclass == '0'] <- 'random'
l$reviewed <- as.factor(l$realclass)

textframe = data.frame(label = c("L'An 2440"), x = c(1800), y = c(.7))

p <- ggplot(l, aes(x = dateused, y = logistic, color = reviewed, shape = reviewed)) + 
  geom_point() + scale_shape_manual(name="actually\n", values = c(3, 17)) + 
  scale_color_manual(name = "actually\n", values = c('gray40', 'black')) + 
  theme_bw() + theme(text = element_text(size = 16, family = 'Avenir Next Medium')) + 
  scale_y_continuous('probability', labels = percent, breaks = c(0.25,0.5,0.75)) + 
  scale_x_continuous("", breaks = c(1800,1850,1900,1950,2000))
plot(p)

tiff("../images/C2Fig2allSF.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)