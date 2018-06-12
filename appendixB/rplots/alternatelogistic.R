# logistic test
library(ggplot2)
library(scales)
disease = c(0,0,0,0,0,1,1,1,1)
test = c(62, 71, 77, 81, 85, 79, 88, 95, 106)

frame = data.frame(disease = disease, test = test)
model = glm(disease ~ test, family=binomial(link='logit'),
            data = frame)
probabilities = predict(model, newdata = data.frame(test = seq(50, 120, 0.1)),
            type = 'response')

prob.frame = data.frame(test = seq(50, 120, 0.1), prob = probabilities)

p <- ggplot() + geom_line(data = prob.frame, aes(x = test, y = prob), size = 2, color = 'gray64') +
    geom_point(data = frame, aes(x = test, y = disease), size = 3) + theme_bw() +
  scale_x_continuous('test result') +
  scale_y_continuous('probability of disease', breaks = c(0, 0.25, 0.5, 0.75, 1)) + 
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.title.x = element_text(margin = margin(t = 14)),
        axis.title.y = element_text(margin = margin(r = 14))) 
tiff("/Users/tunder/Dropbox/book/appendixB/images/alternatelogistic.tiff", height = 4, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)
plot(p)