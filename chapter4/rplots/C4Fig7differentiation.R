# Plotting differentiation for individual volumes

library(scales)
library(ggplot2)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

df <- read.csv('../dataforR/differentiation_plot.csv')
df <- df[df$year > 1799, ]
sf = data.frame(year = 1958,  low = 0.0312, mean = 0.0380, high = 0.0442)
individuals = data.frame(year = c(1927, 1852, 1939, 1848, 1974, 1819), diff = c(0.0370, 0.0794, 0.0877, 0.0419, 0.0074, 0.0916), 
                         labels = c('To the Lighthouse', 'The Blithedale Romance', 'The Big Sleep', 'Jane Eyre', 'The Dispossessed', 'Ivanhoe'),
                         hjust = c(1.13, -0.05, -0.1, 1.15, 1.12, -0.2),
                         vjust = c(0.4,-0.4, 0.4, 0.4, 0.4, .4))
legend = data.frame(year = c(1999, 1995, 1947), diff = c(0.058, 0.020, 0.0353),
                    labels = c('all books\nwritten by men', 'all books\nwritten by women', '20c SF'))

p <- ggplot(df, aes(x = year)) + geom_line(aes(y = median, linetype = authgender)) + 
  geom_errorbar(data=sf, mapping=aes(x=year, ymin=low, ymax=high), width=5, size=1) +
  geom_ribbon(data=subset(df, authgender =='f'), aes(ymin=lower, ymax=upper), alpha=0.2) +
  geom_ribbon(data=subset(df, authgender == 'm'), aes(ymin=lower, ymax=upper), alpha=0.2) +
  theme_bw() + theme(text = element_text(size = 17, family = 'Avenir Next Medium'),
                     panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black')) +
  geom_point(data=individuals, mapping=aes(x=year, y=diff), size= 3, shape=21, fill="white") +
  geom_point(aes(x = 1958, y = 0.0378), size = 3, shape = 21, fill = 'white') +
  geom_text(data = individuals, aes(x = year, y = diff, label = labels, hjust = hjust,
                                    vjust = vjust, family = 'Avenir Next Medium',
                                    fontface = 'italic', size = 4.5)) + 
  scale_x_continuous("") + theme(legend.position = 'none') +
  geom_text(data = legend, aes(x = year, y = diff, label = labels), size = 4.5, 
            family = 'Avenir Next Medium', fontface = 'plain') +
  scale_y_continuous("gender difference", labels = percent, limits = c(0, 0.092))

tiff("../images/C4Fig7differentiation_plot.tiff", height = 7, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)