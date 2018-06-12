library(scales)
library(ggplot2)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
l <- read.csv('../modeloutput/fullfiction.results.csv')

model = lm(data = l, formula = logistic ~ dateused)
intercept = coef(model)[1]
slope = coef(model)[2]

line = intercept + (slope * l$pubdate)
l$reviewed = as.factor(l$realclass)
levels(l$reviewed) = c('random', 'reviewed')
p <- ggplot(l, aes(x = dateused, y = logistic, color = reviewed, shape = reviewed)) + theme_bw() +
  geom_point() + geom_abline(intercept = intercept, slope = slope) + scale_shape_manual(name="actually\n", values = c(1, 17)) + 
  scale_color_manual(name = "actually\n", values = c('gray40', 'gray0')) + 
  theme(text = element_text(size = 16, family = 'Avenir Next Medium')) + 
  scale_y_continuous('probability', labels = percent, breaks = c(0.25,0.5,0.75)) + 
  scale_x_continuous("", breaks = c(1850, 1875, 1900, 1925, 1950))

tiff("~/Dropbox/book/chapter3/images/C3Fig2fictionmodel.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)

tp = sum(l$realclass == 1 & l$logistic >= 0.5)
tn = sum(l$realclass == 0 & l$logistic < 0.5)
fp = sum(l$realclass == 0 & l$logistic >= 0.5)
fn = sum(l$realclass == 1 & l$logistic < 0.5)
print((tp + tn) / (tp+tn+fp+fn))