rawjson_1 <- rjson::fromJSON(file =
                             paste("data/","rewards_no_sche",
                                   ".json", sep=""))
rawjson_2 <- rjson::fromJSON(file =
                             paste("data/","rewards_naive_sche",
                                   ".json", sep=""))
#rawjson_3 <- rjson::fromJSON(file =
#                             paste("data/","rewards_rl_sche",
#                                   ".json", sep=""))

Data_1 <- as.data.frame(rawjson_1)
Data_2 <- as.data.frame(rawjson_2)
#Data_3 <- as.data.frame(rawjson_3)

Data <- rbind(Data_1, Data_2)#, Data_3)
# print(Data)

p <- ggplot2::ggplot(Data,
                     ggplot2::aes(x=Day,
                                  y=Rewards,
                                  group=categ,
                                  color=categ)
                     ) + ggplot2::geom_line(size=1.2)

png(paste("figure/","rewards",".png",sep=""))

plot(p)

dev.off()