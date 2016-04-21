#K-means sample rows
source('DBConnection.r')

source('utils.R')

# install the xlsx package, if needed
# and load it into memory
ensure.loaded("dplyr")
ensure.loaded("cluster")
#Kmeans

#rs <- dbSendQuery(con,"select vf.cuenta,sum(vf.precio_folleto1) AS Ganacia,
#avon.sku_CampanaTot(AVON.sku_CampanaMax(vf.cuenta))-avon.sku_campanatot(avon.sku_CampanaMin(vf.cuenta))+1 as TotalCampanas,
#                  Round(avon.sku_CuentaCampana(vf.cuenta)/(avon.sku_CampanaTot(AVON.sku_CampanaMax(vf.cuenta))-avon.sku_campanatot(avon.sku_CampanaMin(vf.cuenta))+1),2) as Participacion
#                  from avon.view_Factura2013_2015_3 vf 
#                  group by vf.cuenta")


#Funcion para outliers
remove_outliers <- function(x, na.rm = TRUE, ...) {
  qnt <- quantile(x, probs=c(.001, .999), na.rm = na.rm, ...)
  H <- 1.5 * IQR(x, na.rm = na.rm)
  y <- x
  y[x < (qnt[1] - H)] <- NA
  y[x > (qnt[2] + H)] <- NA
  y
} 

#ClientesTot <- fetch(rs)
ClientesTot = read.csv("Valor_clientes.csv")
#Clientes$Grupo <- NULL
head(ClientesTot)
ClientesTot$CUENTA <- gsub(",","",ClientesTot$CUENTA)
ClientesTot$GANACIA <- gsub(",","",ClientesTot$GANACIA)
ClientesTot$TOTALCAMPANAS <- gsub(",","",ClientesTot$TOTALCAMPANAS)
ClientesTot$PARTICIPACION <- gsub(",","",ClientesTot$PARTICIPACION)


#Clientes<- transform(Clientes,NOMBRE = as.factor(Clientes$NOMBRE))
ClientesTot$CUENTA <- as.numeric(ClientesTot$CUENTA)
ClientesTot$GANACIA <- as.numeric(ClientesTot$GANACIA)
ClientesTot$TOTALCAMPANAS <- as.numeric(ClientesTot$TOTALCAMPANAS)
ClientesTot$PARTICIPACION <- as.numeric(ClientesTot$PARTICIPACION)

#Estandarizar y Escalar las variables y centrar
Clientes2 = scale(ClientesTot[2:4], center = TRUE, scale = TRUE)

#Sacar los outliers
Clientes3 <- remove_outliers(Clientes2)
head(Clientes3)

#Unimos a la matriz la informaciÃ³n original para mantener las variables originales, sin embargo no las tomamos en cuenta para hacer el kmeans.

Clientes5 <- cbind(Clientes3,CUENTA=ClientesTot$CUENTA,GANANCIAREAL=ClientesTot$GANACIA,CAMAPANASREAL=ClientesTot$TOTALCAMPANAS,PARTICIPACIONREAL=ClientesTot$PARTICIPACION)
Clientes5 <- data.frame(Clientes5)
head(Clientes5)


#Sacar la muestra
Clientes4 <- sample_n(na.omit(Clientes5), 10000)


#Calcular la cantidad de clusters
#------------------------------------------------------------------------------------
# Crea vector "Errores", sin datos
# Crea variable "K_Max" con la cant. maxima de k a analizar
Errores <-NULL
  K_Max   <-9


#------------------------------------------------------------------------------------
# Ejecuta kmeans con diferentes cluster, desde 1 hasta 9
# Luego guarda el error de cada ejecucion en el vector "Errores"
for (i in 1:K_Max)
{
  Errores[i] <- sum(kmeans(Clientes4[1:3], centers=i)$withinss)
}

#------------------------------------------------------------------------------------
# Grafica el vector "Errores"
plot(1:K_Max, Errores, type="b", 
     xlab="Cantidad de Cluster", 
     ylab="Suma de error")
#
#---------------------------------------------------------------------------------
# Creando los 3 Cluster o usando K-MEANS
#Luego asigna grupo a cada cliente en tabla Cliente
#ModeloKMEANS <- kmeans(Clientes[-1],3)
#Clientes$Grupo <- ModeloKMEANS$cluster

#---------------------------------------------------------------------------------
#Graficando los puntos de dispersi?n y luego asignando a cada punto etiquetas
#plot(Clientes$ANOSCONSULTORA,Clientes$GANANCIA,
#     col=Clientes$Grupo,cex.axis=.7,cex.lab=.7)

#text(Clientes$ANOSCONSULTORA,Clientes$GANANCIA,
#     labels=Clientes$CUENTA,pos=1,col=Clientes$Grupo,cex=.7)

#Salvando Datos , con el id del grupo
#write.csv(Clientes,"C:/Users/ricmorales/Desktop/BD/ganancia.csv")




#--------------------------------------------------------------#
# PASO 2: Crea vector con Algoritmos y tabla vacía para guardar Iteraciones
Algoritmos         <-c("Hartigan-Wong","Lloyd","Forgy","MacQueen") 
CantidadAlgoritmos <-length(Algoritmos) # guarda la cantidad de algoritmos usados
Iteraciones        <-data.frame(Intraclase=numeric(),Algoritmo=character())

#-------------------------------------------------------------------------

# PASO 3: Ejecuta k-means 10 veces en cada algoritmo
# y guarda la Distancia Intracluster de cada iteracion en la tabla Iteraciones
for (i in 1:CantidadAlgoritmos) 
{
  for (ii in 1:100) 
  {
    Modelo      <- kmeans(Clientes4[1:3],5, algorithm = Algoritmos[i])
    Iteraciones <- rbind(Iteraciones,
                         data.frame(Intraclase = Modelo$betweenss,
                                    Algoritmo = Algoritmos[i]))
  }
}

#-------------------------------------------------------------------------
# PASO 4: Calcula la media de Distancia Intracluster en cada algoritmo
#  e identificar Algoritmo Ganador 
Resultados       <- tapply(Iteraciones$Intraclase,Iteraciones$Algoritmo,mean) 
Resultados       <-sort(Resultados,decreasing = T)
AlgoritmoGanador <-names(Resultados[1])

#-------------------------------------------------------------------------
# PASO 5: Ejecuta kmeans con algoritmo ganador y asigna grupo a cada cliente
KmeansOptimizado <- kmeans(Clientes4[1:3],5, algorithm = AlgoritmoGanador)
Clientes4$Grupo   <-KmeansOptimizado$cluster

#-------------------------------------------------------------------------

#PASO 6: Grafica segmentacion de algoritomo ganador y luego asigna etiquetas
plot(Clientes4$TOTALCAMPANAS,Clientes4$GANACIA,col=Clientes4$Grupo,cex.axis=.7,cex.lab=.7)
text(Clientes4$TOTALCAMPANAS,Clientes4$GANACIA,
     labels=Clientes4$CUENTA,pos=1,col=Clientes4$Grupo,cex=.7)
title(main=paste("Algoritmo ganador:",AlgoritmoGanador),cex.main=.9)

write.csv(Clientes4,"C:/Users/isalopez/Desktop/ganancia_5Clusters_centrado.csv")












#-------------------------------------------------------------------------
#PAM 
PAM = pam(Clientes,k=4,metric="euclidean")
plot(PAM)
write.csv(PAM,"C:/Users/isalopez/Desktop/ganancia_optimizado_6Clusters_sample.csv")

#-------------------------------------------------------------------------
#ACP
install.packages("FactoMineR")
library(FactoMineR)
pruebapca.pca=PCA(Clientes,graph=T)

install.packages("ade4")
library(ade4)

coordenadas=pruebapca.pca$ind$coord
#PLANO PRINCIPAL
s.label(coordenadas,xax = 1,yax = 2,label=Clientes[,1],possub="bottomleft")

library(amap)

#Prueba
Clientes2=scale(Clientes[2:4],center = T,scale = T)
prueba.pca=princomp(Clientes2)
comp=predict(prueba.pca)[,1:2]
grupos=kmeans(comp,4)
plot(comp,col=grupos$cluster)