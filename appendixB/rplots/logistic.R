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
  scale_y_continuous('', breaks = c(0, 0.25, 0.5, 0.75, 1)) + 
  annotate("text", x = 50, y = 1.12, 
           label = "Probability of\nhaving disease", hjust = 0, size = 5) +
  theme(text = element_text(size = 16), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black')) 
tiff("/Users/tunder/Dropbox/book/appendixB/images/logistic.tiff", height = 6, width = 6, units = 'in', res=400)
plot(p)
dev.off()
plot(p)
plot(p)