setwd(".")
library(plyr)
library(dplyr)
library(ggplot2)
library(extrafont)
require(reshape2)
library(nortest)
library(effsize)
library(splitstackshape)
library(car)
library(rstatix)
library(tidyverse)
library(ggpubr)
library(ez)
library(bestNormalize)

loadfonts()
options(max.print=50)
fontSize = 10

data = read.csv("data.csv")

# Beautify the data frame

data = data %>% select(!X)

data$movement = as.factor(data$movement)
data$environment = as.factor(data$environment)
data$tactic = as.factor(data$tactic)

data = rename(data, energy = total_energy)
data = rename(data, cpu = total_cpu)
data = rename(data, ram = total_ram)

data$energy = data$energy / 1000

data$run = as.factor(data$run)

data$tactic = revalue(data$tactic, c("baseline"="B", "ee1"="EE1", "ee2"="EE2", "ee3"="EE3", "ee4"="EE4", "combined"="C"))
data$tactic <- factor(data$tactic, levels = c("B", "EE1", "EE2", "EE3", "EE4", "C"))

data$environment = revalue(data$environment, c("empty"="empty", "obstacles"="cluttered"))
data$environment <- factor(data$environment, levels = c("empty", "cluttered"))

data$movement = revalue(data$movement, c("AUTONOMOUS"="autonomous", "NO"="noMovement", "FIXED"="sweep"))
data$movement <- factor(data$movement, levels = c("noMovement", "autonomous", "sweep"))

data$trial_id = factor(paste(data$tactic, data$movement, data$environment, sep="_"))

#=========================================================
# Data exploration
#=========================================================

# Summarize data for the table

data %>% group_by(tactic) %>% 
  summarise(min=min(energy), max=max(energy), median=median(energy), mean=mean(energy), sd=sd(energy)) %>% 
  mutate(cv=100 * sd/mean) %>% as.data.frame()

data %>% 
  summarise(min=min(energy), max=max(energy), median=median(energy), mean=mean(energy), sd=sd(energy)) %>% 
  mutate(cv=100 * sd/mean) %>% as.data.frame()

#=========================================================
# Normality checks
#=========================================================

check_normality = function(data) {
  plot(density(data)) 
  qqPlot(data)
  shapiro.test(data)
}

check_normality(data$energy)

#=========================================================
# Statistical tests
#=========================================================

# data = data %>% filter(movement == "autonomous")
# 
res.kruskal <- data %>% kruskal_test(energy ~ tactic)
res.kruskal

data %>% kruskal_effsize(energy ~ tactic)

pwc2 <- data %>% 
  wilcox_test(energy ~ tactic, p.adjust.method = "BH", ref.group = "B", exact=F)
pwc2

pwc2 <- data %>% group_by(movement, environment) %>%
  wilcox_test(energy ~ tactic, p.adjust.method = "BH", ref.group = "B", exact=F)
pwc2

# pwc3 <- data %>%
#   dunn_test(energy ~ tactic, p.adjust.method = "holm")
# pwc3

#=========================================================
# Effect size
#=========================================================

check_effect_size = function(df) {
  result = data.frame()
  
  df.b = df %>% filter(tactic == "B")
  df.ee1 = df %>% filter(tactic == "EE1")
  df.ee2 = df %>% filter(tactic == "EE2")
  df.ee3 = df %>% filter(tactic == "EE3")
  df.ee4 = df %>% filter(tactic == "EE4")
  df.c = df %>% filter(tactic == "C")
  
  cd.ee1 = cliff.delta(df.b$energy, df.ee1$energy)
  cd.ee2 = cliff.delta(df.b$energy, df.ee2$energy)
  cd.ee3 = cliff.delta(df.b$energy, df.ee3$energy)
  cd.ee4 = cliff.delta(df.b$energy, df.ee4$energy)
  cd.c = cliff.delta(df.b$energy, df.c$energy)
  
  va.ee1 = VD.A(df.b$energy, df.ee1$energy)
  va.ee2 = VD.A(df.b$energy, df.ee2$energy)
  va.ee3 = VD.A(df.b$energy, df.ee3$energy)
  va.ee4 = VD.A(df.b$energy, df.ee4$energy)
  va.c = VD.A(df.b$energy, df.c$energy)
  
  result = rbind(result, list("EE1", "cd", cd.ee1$estimate, cd.ee1$magnitude))
  result = rbind(result, list("EE2", "cd", cd.ee2$estimate, cd.ee2$magnitude))
  result = rbind(result, list("EE3", "cd", cd.ee3$estimate, cd.ee3$magnitude))
  result = rbind(result, list("EE4", "cd", cd.ee4$estimate, cd.ee4$magnitude))
  result = rbind(result, list("C", "cd", cd.c$estimate, cd.c$magnitude))
  
  result = rbind(result, list("EE1", "va", va.ee1$estimate, va.ee1$magnitude))
  result = rbind(result, list("EE2", "va", va.ee2$estimate, va.ee2$magnitude))
  result = rbind(result, list("EE3", "va", va.ee3$estimate, va.ee3$magnitude))
  result = rbind(result, list("EE4", "va", va.ee4$estimate, va.ee4$magnitude))
  result = rbind(result, list("C", "va", va.c$estimate, va.c$magnitude))
  
  colnames(result) <- c("tactic","type", "estimate", "magnitude")
  
  return(result)
}

check_effect_size(data)

check_effect_size(data %>% filter(movement == "noMovement"))
check_effect_size(data %>% filter(movement == "sweep"))
check_effect_size(data %>% filter(movement == "autonomous"))
check_effect_size(data %>% filter(environment == "empty"))
check_effect_size(data %>% filter(environment == "cluttered"))

#=========================================================
# Visualizations
#=========================================================

fontSize = 12

# Plot global energy

bp <- ggplot(data, aes(x=tactic, y=energy, fill=tactic)) + #+ ylim(0, max(data$energy)) +
  geom_violin(trim = FALSE, alpha = 0.5, position=position_dodge(0.9)) + theme_bw() + xlab("Tactics") + ylab("Energy (J)") +
  geom_boxplot(alpha=1, color="black", width=.2, fill="white", outlier.size=0) +
  stat_summary(fun.y=mean, colour="black", geom="point", 
               shape=5, size=1,show_guide = FALSE) +
  theme(legend.position="none") +
  guides(color=guide_legend(title="")) + theme(strip.text.x=element_text(size=fontSize), strip.text.y=element_text(size=fontSize),  axis.text.x=element_text(size=fontSize, angle = 45, hjust = 1), axis.text.y=element_text(size=fontSize), axis.title=element_text(size=fontSize))
bp

ggsave("./plots/energy_global.pdf", scale = 1, height = 6, width = 16, unit = "cm")

# Plot all combinations

fontSize = 11

bp <- ggplot(data, aes(x=tactic, y=energy, group=tactic, fill=tactic)) + #+ ylim(0, max(data$energy)) +
  geom_violin(trim = FALSE, alpha = 0.5, position=position_dodge(0.9)) + theme_bw() + xlab("Tactics") + ylab("Energy (J)") +
  geom_boxplot(alpha=1, color="black", width=.2, fill="white", outlier.size=0) +
  stat_summary(fun.y=mean, colour="black", geom="point", 
               shape=5, size=1,show_guide = FALSE) +
  guides(color=guide_legend(title="")) + theme(strip.text.x=element_text(size=fontSize), strip.text.y=element_text(size=fontSize),  axis.text.x=element_text(size=fontSize, angle = 45, hjust = 1), axis.text.y=element_text(size=fontSize), axis.title=element_text(size=fontSize))
# + geom_jitter(shape=16, size = 0.5, position=position_jitter(0.2))
bp
# bp + facet_wrap(environment ~ movement, ncol=3, labeller = label_wrap_gen(multi_line=FALSE))
bp + facet_grid(movement ~ environment, margin=FALSE) + theme(legend.position="none", strip.background = element_rect(
  color="white", fill="white", size=1, linetype="solid"))

ggsave("./plots/energy_faceted.pdf", scale = 1.6, height = 8, width = 10, unit = "cm")

bp <- ggplot(data, aes(x=tactic, y=energy, group=tactic, fill=tactic)) + #+ ylim(0, max(data$energy)) +
  geom_violin(trim = FALSE, alpha = 0.5, position=position_dodge(0.9)) + theme_bw() + xlab("Tactics") + ylab("Energy (J)") +
  geom_boxplot(alpha=1, color="black", width=.2, fill="white", outlier.size=0) +
  stat_summary(fun.y=mean, colour="black", geom="point", 
               shape=5, size=1,show_guide = FALSE) +
  guides(color=guide_legend(title="")) + theme(strip.text.x=element_text(size=fontSize), strip.text.y=element_text(size=fontSize),  axis.text.x=element_text(size=fontSize, angle = 45, hjust = 1), axis.text.y=element_text(size=fontSize), axis.title=element_text(size=fontSize))
# + geom_jitter(shape=16, size = 0.5, position=position_jitter(0.2))
bp
# bp + facet_wrap(environment ~ movement, ncol=3, labeller = label_wrap_gen(multi_line=FALSE))
bp + facet_grid(environment ~ movement, margin=TRUE) + theme(legend.position="none", strip.background = element_rect(
  color="white", fill="white", size=1, linetype="solid"))

ggsave("./plots/energy_faceted_large.pdf", scale = 1.6, height = 15, width = 24, unit = "cm")

