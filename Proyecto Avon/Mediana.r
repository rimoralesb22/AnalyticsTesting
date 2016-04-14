# load Practice data frame into memory
#   if not alredy there

source('utils.R')

# install the xlsx package, if needed
# and load it into memory
ensure.loaded("data.table")

source('DBConnection.r')

#Kmeans

rs <- dbSendQuery(con,"Select vz.zona,vz.cuenta,round(sum(vz.precio*vz.CANTIDAD),2) as Monto from avon.view_Zona2013_2015 vz 
                  group by vz.zona,vz.cuenta
                  order by zona,monto")

Zonas <- fetch(rs)
head(Zonas)


#Calcular Mediana

zonas1 <-data.table(Zonas)

#zonas1[ZONA==301,Mediana :=median(zonas1[ZONA==301][,MONTO])]
##Remove outliers
remove_outliers <- function(x, na.rm = TRUE, ...) {
  qnt <- quantile(x, probs=c(.01, .99), na.rm = na.rm, ...)
  H <- 1.5 * IQR(x, na.rm = na.rm)
  y <- x
  y[x < (qnt[1] - H)] <- NA
  y[x > (qnt[2] + H)] <- NA
  y
}
for(i in 301:355)
{
  y <- remove_outliers(zonas1[ZONA==i][,MONTO])
  zonas1[ZONA==i,PORCENTAJE :=median(na.omit(y))/max(na.omit(y))]
}




head(zonas1)

## png()
##par(mfrow = c(1, 2))
##boxplot(zonas1[ZONA==303][,MONTO])
##boxplot(y)


write.csv(zonas1[,min(PORCENTAJE),ZONA],"C:/Users/ricmorales/Desktop/BD/Mediana.csv")
