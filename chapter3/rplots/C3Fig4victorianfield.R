library(ggplot2)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
data <- read.csv('../salesdata/pairedwithprestige.csv')

victorians <- data[data$midcareer >= 1840 & data$midcareer < 1875, ]
victorians$reviewed <- as.factor(victorians$reviews > 0)

victorians$plotnames = rep('', length(victorians$author))
victorians$plotnames[victorians$author == 'Dickens, Charles'] <- 'Charles Dickens'
victorians$plotnames[victorians$author == 'Wood, Ellen'] <- 'Ellen Wood'
victorians$plotnames[victorians$author == 'Ainsworth, William Harrison'] <- 'W. H. Ainsworth'
victorians$plotnames[victorians$author == 'Lytton, Edward Bulwer Lytton'] <- 'E. Bulwer-Lytton'
victorians$plotnames[victorians$author == 'Eliot, George'] <- 'George Eliot'
victorians$plotnames[victorians$author == 'Sikes, Wirt'] <- 'Wirt Sikes'
victorians$plotnames[victorians$author == 'Collins, A. Maria'] <- 'Maria Collins'
victorians$plotnames[victorians$author == 'Hawthorne, Nathaniel'] <- 'N. Hawthorne'
victorians$plotnames[victorians$author == 'Southworth, Emma Dorothy Eliza Nevitte'] <- 'EDEN Southworth'
victorians$plotnames[victorians$author == 'Helps, Arthur'] <- 'Arthur Helps'

model = lm(data = victorians, formula = prestige ~ percentile)
intercept = coef(model)[1]
slope = coef(model)[2]

p <- ggplot(victorians, aes(x = percentile, y = prestige, shape = reviewed, color = reviewed, fill = reviewed, size = num_vols, alpha = 0.6)) +
  geom_point() + theme_bw() +
  geom_text(aes(label = plotnames), color = 'black', size = 4, 
            position = position_nudge(x = 0.025), hjust = 0,
            family = 'Avenir Next Medium', alpha = 1) +
  geom_abline(intercept = intercept, slope = slope, linetype = 'dashed') +
  scale_color_manual(values = c('black', 'gray20')) +
  scale_fill_manual(values = c('gray85', 'gray20')) +
  scale_shape_manual(values = c(21, 17)) +
  scale_x_continuous(limits = c(0, 1.22), breaks = c(0, 0.25, 0.5, 0.75, 1)) +
  labs(x = 'percentile ranking, sales', y = 'prob. of review in selective venues') +
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'), 
        legend.position = 'none')

tiff("~/Dropbox/book/chapter3/images/C3Fig4victorianfield.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)
