library(ggplot2)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
data <- read.csv('../salesdata/pairedwithprestige.csv')

moderns <- data[data$midcareer >= 1925 & data$midcareer < 1950, ]
moderns$reviewed <- as.factor(moderns$reviews > 0)

moderns$plotnames = rep('', length(moderns$author))
moderns$plotnames[moderns$author == 'Cain, James M'] <- 'James M Cain'
moderns$plotnames[moderns$author == 'Faulkner, William'] <- 'William Faulkner'
moderns$plotnames[moderns$author == 'Stein, Gertrude'] <- 'Gertrude Stein'
moderns$plotnames[moderns$author == 'Hemingway, Ernest'] <- 'E. Hemingway'
moderns$plotnames[moderns$author == 'Joyce, James'] <- 'James Joyce'
moderns$plotnames[moderns$author == 'Forester, C. S. (Cecil Scott)'] <- 'C. S. Forester'
moderns$plotnames[moderns$author == 'Spillane, Mickey'] <- 'Mickey Spillane'
moderns$plotnames[moderns$author == 'Howard, Robert E'] <- 'Robert E. Howard'
moderns$plotnames[moderns$author == 'Buck, Pearl S'] <- 'Pearl S. Buck'
moderns$plotnames[moderns$author == 'Christie, Agatha'] <- 'Agatha Christie'
moderns$plotnames[moderns$author == 'Hurston, Zora Neale'] <- 'Zora Neale Hurston'
moderns$plotnames[moderns$author == 'Rhys, Jean'] <- 'Jean Rhys'

model = lm(data = moderns, formula = prestige ~ percentile)
intercept = coef(model)[1]
slope = coef(model)[2]

p <- ggplot(moderns, aes(x = percentile, y = prestige, shape = reviewed, color = reviewed, fill = reviewed, size = num_vols, alpha = 0.6)) +
  geom_point() + theme_bw() +
  geom_text(aes(label = plotnames), color = 'black', size = 4, 
            position = position_nudge(x = 0.025), hjust = 0,
            family = 'Avenir Next Medium', alpha = 1) +
  geom_abline(intercept = intercept, slope = slope, linetype = 'dashed') +
  scale_color_manual(values = c('black', 'gray20')) +
  scale_fill_manual(values = c('gray85', 'gray20')) +
  scale_shape_manual(values = c(21, 17)) +
  scale_x_continuous(limits = c(0, 1.15), breaks = c(0, 0.25, 0.5, 0.75, 1)) +
  labs(x = 'percentile ranking, sales', y = 'prob. of review in selective venues') +
  theme(text = element_text(size = 18, family = "Avenir Next Medium"), panel.border = element_blank()) +
  ggtitle('The literary field, 1925-49') +
  theme(axis.line = element_line(color = 'black'), 
        legend.position = 'none',
        plot.title = element_text(size = 18),
        axis.title.x = element_text(margin = margin(t = 14)),
        axis.title.y = element_text(margin = margin(r = 14)))

tiff("~/Dropbox/book/chapter3/images/C3Fig5modernfield.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)
