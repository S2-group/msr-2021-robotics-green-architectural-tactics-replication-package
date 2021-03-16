library(jsonlite)
library(data.table)
library(raster)

num_of_days <- function(unix_time_list, current_time){
  i <- 0
  numDays_list <- c()
  for(t in unix_time_list){
    numDays <- abs(t - current_time)/60/60/24
    numDays <- round(numDays, digits = 0)
    numDays_list <- c(numDays_list, numDays)
  }
  return(numDays_list)
}
time_to_uxtime <- function(time){
  i <- 0
  unix_time_list <- c()
  for(t in time){
    unix_time <- as.numeric(as.POSIXct(t))
    unix_time_list <- c(unix_time_list,unix_time)
  }
  return(unix_time_list)
}
col_to_list <- function(col){
  i <- 0
  c_list <- c()
  for(c in col){
    c_list <- c(c_list, c)
  }
  return(c_list)
}

stat_info <- function(list){
  cv <- (sd(list)/mean(list))
  return(list(min(list), 
         max(list), 
         median(list), 
         mean(list), 
         sd(list), 
         cv)
         )
}
#get current time
# current_time = as.numeric(as.POSIXct(Sys.time()))
# current_time

#StackOverflow Stats
so_timee = 1581897600
so_data <- fromJSON("../phase1_data_collection/data/stackoverflow_data.json")
colnames(so_data)
so_time <- so_data[("time")]
so_unix_time_list = time_to_uxtime(so_time)
so_days = num_of_days(so_unix_time_list, so_timee)
#so_stats = stat_info(so_unix_time_list)
#so_stats
so_days
cv(so_days)
so_day_stats = stat_info(so_days)
so_day_stats
#user
so_user <- scan("../phase1_data_collection/data/so_user_frequency.txt", integer())
so_user_stats = stat_info(so_user)
so_user_stats

#ROS-Answers Stats
rosa_timee = 1581897600
rosa_data <- fromJSON("../phase1_data_collection/data/rosa_data.json")
colnames(rosa_data)
rosa_time <- rosa_data[("time")]
rosa_unix_time_list = time_to_uxtime(rosa_time)
rosa_days = num_of_days(rosa_unix_time_list, rosa_timee)
#rosa_stats = stat_info(rosa_unix_time_list)
#rosa_stats
rosa_days
cv(rosa_days)
rosa_day_stats = stat_info(rosa_days)
rosa_day_stats
#user
rosa_user <- scan("../phase1_data_collection/data/rosa_user_frequency.txt", integer())
rosa_user_stats = stat_info(rosa_user)
rosa_user_stats

#ROS Wiki Stats
ros_wiki <- fromJSON("../phase1_data_collection/data/wiki_stats.json")
colnames(ros_wiki)
wiki_time <- ros_wiki[("time")]
wiki_unix_time_list = time_to_uxtime(wiki_time)
wiki_days = num_of_days(wiki_unix_time_list, current_time)
#wiki_stats = stat_info(wiki_unix_time_list)
#wiki_stats
wiki_days
cv(wiki_days)
wiki_day_stats = stat_info(wiki_days)
wiki_day_stats
#user
wiki_user <- scan("../phase1_data_collection/data/wiki_user_frequency.txt", integer())
wiki_user_stats = stat_info(wiki_user)
wiki_user_stats

#ROS-Discourse Stats
#time
rosd_timee = 1582329600
rosd <- fromJSON("../phase1_data_collection/data/rosd_stats.json")
colnames(rosd)
rosd_time <- rosd[("post_time")]
rosd_time
rosd_unix_time_list = time_to_uxtime(rosd_time)
rosd_days = num_of_days(rosd_unix_time_list, rosd_timee)
#rosd_stats = stat_info(rosd_unix_time_list)
#rosd_stats
rosd_days
cv(rosd_days)
rosd_day_stats = stat_info(rosd_days)
rosd_day_stats
#user
rd_user <- scan("../phase1_data_collection/data/rosd_user_frequency.txt", integer())
rd_user_stats = stat_info(rd_user)
rd_user_stats

#BOTH Repository stats (python and cpp projects)
repo <- fromJSON("../phase1_data_collection/data/both_repo_stats.json")
colnames(repo)
#Commits
repo_commits <- repo[("commits")]
repo_c_l = col_to_list(repo_commits)
repo_c_l
repo_c_stats = stat_info(repo_c_l)
repo_c_stats
#PRs
repo_pr <- repo[("prs")]
repo_p_l = col_to_list(repo_pr)
repo_p_l
repo_p_stats = stat_info(repo_p_l)
repo_p_stats
#Issues
repo_issue <- repo[("issues")]
repo_i_l = col_to_list(repo_issue)
repo_i_l[is.na(repo_i_l)] <- 0
repo_i_l
repo_i_stats = stat_info(repo_i_l)
repo_i_stats
#Contributors
repo_contributors <- repo[("contributors")]
repo_cr_l = col_to_list(repo_contributors)
repo_cr_l
repo_cr_stats = stat_info(repo_cr_l)
repo_cr_stats
#.md files
repo_md <- repo[("md")]
repo_md_l = col_to_list(repo_md)
repo_md_l
repo_md_stats = stat_info(repo_md_l)
repo_md_stats

#CPP repo stats
cpp_repo <- fromJSON("../phase1_data_collection/data/cpp_repo_stats.json")
colnames(cpp_repo)
#Commits
cpp_repo_commits <- cpp_repo[("commits")]
cpp_repo_c_l = col_to_list(cpp_repo_commits)
cpp_repo_c_l
cpp_repo_c_stats = stat_info(cpp_repo_c_l)
cpp_repo_c_stats
#PRs
cpp_repo_pr <- cpp_repo[("prs")]
cpp_repo_p_l = col_to_list(cpp_repo_pr)
cpp_repo_p_l
cpp_repo_p_stats = stat_info(cpp_repo_p_l)
cpp_repo_p_stats
#Issues
cpp_repo_issue <- cpp_repo[("issues")]
cpp_repo_i_l = col_to_list(cpp_repo_issue)
cpp_repo_i_l[is.na(cpp_repo_i_l)] <- 0
cpp_repo_i_l
cpp_repo_i_stats = stat_info(cpp_repo_i_l)
cpp_repo_i_stats
#Contributors
cpp_repo_contributors <- cpp_repo[("contributors")]
cpp_repo_cr_l = col_to_list(cpp_repo_contributors)
cpp_repo_cr_l
cpp_repo_cr_stats = stat_info(cpp_repo_cr_l)
cpp_repo_cr_stats
#.md files
cpp_repo_md <- cpp_repo[("md")]
cpp_repo_md_l = col_to_list(cpp_repo_md)
cpp_repo_md_l
cpp_repo_md_stats = stat_info(cpp_repo_md_l)
cpp_repo_md_stats

#PYTHON repo stats
py_repo <- fromJSON("../phase1_data_collection/data/python_repo_stats.json")
colnames(py_repo)
#Commits
py_repo_commits <- py_repo[("commits")]
py_repo_c_l = col_to_list(py_repo_commits)
py_repo_c_l
py_repo_c_stats = stat_info(py_repo_c_l)
py_repo_c_stats
#PRs
py_repo_pr <- py_repo[("prs")]
py_repo_p_l = col_to_list(py_repo_pr)
py_repo_p_l
py_repo_p_stats = stat_info(py_repo_p_l)
py_repo_p_stats
#Issues
py_repo_issue <- py_repo[("issues")]
py_repo_i_l = col_to_list(py_repo_issue)
py_repo_i_l[is.na(py_repo_i_l)] <- 0
py_repo_i_l
py_repo_i_stats = stat_info(py_repo_i_l)
py_repo_i_stats
#Contributors
py_repo_contributors <- py_repo[("contributors")]
py_repo_cr_l = col_to_list(py_repo_contributors)
py_repo_cr_l
py_repo_cr_stats = stat_info(py_repo_cr_l)
py_repo_cr_stats
#.md files
py_repo_md <- py_repo[("md")]
py_repo_md_l = col_to_list(py_repo_md)
py_repo_md_l
py_repo_md_stats = stat_info(py_repo_md_l)
py_repo_md_stats


