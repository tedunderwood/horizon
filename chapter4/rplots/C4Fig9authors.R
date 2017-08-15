library(ggplot2)
library(scales)
library(dplyr)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

data=read.table("../dataforR/author_ci.txt", sep="\t")
gdf=as.data.frame(data)
p <- ggplot(gdf, (aes(x=gdf$V1, y=gdf$V3))) + 
  geom_point(size = 2, shape = 18, alpha = 0.7) + 
  xlab("") + ylab("") + ggtitle("Percentage of fiction volumes written by women") + 
  scale_y_continuous(labels = scales::percent, limits = c(0, 0.8)) + 
  theme_bw() +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), 
        panel.border = element_blank(),
        axis.line = element_line(color = 'black'),
        plot.title = element_text(margin = margin(b = 14), size = 16, lineheight = 1.1))

tiff("../images/C4Fig9authors.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)