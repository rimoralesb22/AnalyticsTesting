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
                  order by zona")

Zonas <- fetch(rs)
head(Zonas)


#Calcular Mediana

zonas1 <-data.table(Zonas)

zonas1[ZONA==301,Mediana :=median(zonas1[ZONA==301][,MONTO])]


for(i in 301:355)
{
  zonas1[ZONA==i,Mediana :=median(zonas1[ZONA==i][,MONTO])]
}

zonas1

write.csv(zonas1,"C:/Users/ricmorales/Desktop/BD/Mediana.csv")
