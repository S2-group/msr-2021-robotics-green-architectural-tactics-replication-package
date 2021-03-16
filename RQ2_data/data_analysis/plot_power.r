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
library(zoo)


loadfonts()
options(max.print=50)
fontSize = 10

main_dir = "./experiment_output/"

path_movmnt = c('/n_movement', '/f_movement', '/a_movement')
path_tactic = c('/1_baseline', '/2_ee1', '/3_ee2', '/4_ee3', '/5_ee4', '/6_combined')
path_envmnt = c('/empty', '/obstacles')

energy_hertz <- 200 # Frequency at which energy is measured.

get_all_runs <- function(path) {
  run_list <- list()
  
  for (i in 1:10) {
    file_path = paste(main_dir, path, '/run', i, '/DATA.txt', sep="")
    run <- read.csv(file_path, header = FALSE)
    run_list[[i]] <- run
  }
  
  return(run_list)
}

filter_data <- function(d) {
  d<-d[!(d$V1==0.0),]
  return(d)
}

convert_run_to_per_second <- function(data) {
  # Energy part:
  deltas <- data.frame(V1 = data$V1, 
                       V2 = sapply(data$V5, 
                                   function (x) x * (1/energy_hertz))
  )      # Convert every reading to 1/200th of its value
  per_second <- rollapply(deltas$V2, energy_hertz, sum, by = energy_hertz)  # Sum each 200 readings to an accumulated value, representing energy per second in mJ
  run_per_second <- data.frame(V1 = seq(1, length(per_second), by=1), 
                               V2 = per_second
  )
  
  return(run_per_second)
}

convert_data <- function(all_runs) {
  all_runs_return <- data.frame()
  for (i in 1:length(all_runs)) {
    all_runs_return <- rbind(all_runs_return, 
                             convert_run_to_per_second(
                               top_n(filter_data(all_runs[[i]]), 24000)
                             )
    )
  }
  all_runs_return = all_runs_return %>% filter(V1 <= 120)
  return(all_runs_return)
}

get_random_slice = function(data) {
  random_start = sample(seq(1, 1200, 120), 1)
  return(data %>% slice(random_start:(random_start + 120)))
}

no_empty_b <- convert_data(get_all_runs(paste('/n_movement', '/1_baseline', sep="")))
no_empty_c <- convert_data(get_all_runs(paste('/n_movement', '/6_combined', sep="")))
no_empty_b = get_random_slice(no_empty_b)
no_empty_b$tactic = factor("B")
no_empty_c = get_random_slice(no_empty_c)
no_empty_c$tactic = factor("C")
no_empty = rbind(no_empty_b, no_empty_c)
no_empty$combination = factor("no_empty")

auto_empty_b <- convert_data(get_all_runs(paste('/a_movement/empty', '/1_baseline', sep="")))
auto_empty_c <- convert_data(get_all_runs(paste('/a_movement/empty', '/6_combined', sep="")))
auto_empty_b = get_random_slice(auto_empty_b)
auto_empty_b$tactic = factor("B")
auto_empty_c = get_random_slice(auto_empty_c)
auto_empty_c$tactic = factor("C")
auto_empty = rbind(auto_empty_b, auto_empty_c)
auto_empty$combination = factor("auto_empty")

auto_cluttered_b <- convert_data(get_all_runs(paste('/a_movement/obstacles', '/1_baseline', sep="")))
auto_cluttered_c <- convert_data(get_all_runs(paste('/a_movement/obstacles', '/6_combined', sep="")))
auto_cluttered_b = get_random_slice(auto_cluttered_b)
auto_cluttered_b$tactic = factor("B")
auto_cluttered_c = get_random_slice(auto_cluttered_c)
auto_cluttered_c$tactic = factor("C")
auto_cluttered = rbind(auto_cluttered_b, auto_cluttered_c)
auto_cluttered$combination = factor("auto_cluttered")

sweep_empty_b <- convert_data(get_all_runs(paste('/f_movement/empty', '/1_baseline', sep="")))
sweep_empty_c <- convert_data(get_all_runs(paste('/f_movement/empty', '/6_combined', sep="")))
sweep_empty_b = get_random_slice(sweep_empty_b)
sweep_empty_b$tactic = factor("B")
sweep_empty_c = get_random_slice(sweep_empty_c)
sweep_empty_c$tactic = factor("C")
sweep_empty = rbind(sweep_empty_b, sweep_empty_c)
sweep_empty$combination = factor("sweep_empty")

sweep_cluttered_b <- convert_data(get_all_runs(paste('/f_movement/obstacles', '/1_baseline', sep="")))
sweep_cluttered_c <- convert_data(get_all_runs(paste('/f_movement/obstacles', '/6_combined', sep="")))
sweep_cluttered_b = get_random_slice(sweep_cluttered_b)
sweep_cluttered_b$tactic = factor("B")
sweep_cluttered_c = get_random_slice(sweep_cluttered_c)
sweep_cluttered_c$tactic = factor("C")
sweep_cluttered = rbind(sweep_cluttered_b, sweep_cluttered_c)
sweep_cluttered$combination = factor("sweep_cluttered")

data = rbind(no_empty, auto_empty, auto_cluttered, sweep_empty, sweep_cluttered)

fontSize = 8

global_min = min(data$V2)
global_max = max(data$V2)

plot_power = function(comb, title) {
  data %>% filter(combination == comb) %>%
  ggplot(aes(x=V1, y=V2, color=tactic)) + 
    # geom_hex(bins=120) +
    geom_line() +
    ylim(global_min, global_max) +
    xlim(0, 120) +
    ggtitle(title) +
    theme_bw() + xlab("Mission time (seconds)") + ylab("Power (mW)") +
    scale_x_continuous(breaks=seq(0,120,10)) +
    scale_color_manual(values=c("red", "#009900")) +
    theme(legend.position="none", plot.title=element_text(size=fontSize), axis.text.x=element_text(size=fontSize, angle = 45, hjust = 1), axis.text.y=element_text(size=fontSize), axis.title=element_text(size=fontSize))
  
  ggsave(paste("./plots/power_", comb, ".pdf", sep=""), scale = .9, height = 4, width = 10, unit = "cm")
}

plot_power("no_empty", "a) No movement, empty environment") 
plot_power("auto_empty", "b) Autonomous movement, empty environment")
plot_power("auto_cluttered", "c) Autonomous movement, cluttered environment")
plot_power("sweep_empty", "d) Sweep movement, empty environment")
plot_power("sweep_cluttered", "e) Sweep movement, cluttered environment")


