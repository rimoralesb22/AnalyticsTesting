# Fija semilla inicial de numeros pseudoaleatorios
# para obtener misma serie aleatoria en ejecuciones.
set.seed(123)

source('DBConnection.r')

#Kmeans

rs <- dbSendQuery(con,"Select vf.cuenta, sum(vf.PRECIO_FOLLETO1) as ganancia,( max(vf.fecha) - avon.sku_cuentacampana(vf.cuenta))/365 AS anosConsultora
                  from avon.view_Facturas2013_2015_2 vf
                  group by vf.cuenta")

Clientes <- fetch(rs)
head(Clientes)

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
  Errores[i] <- sum(kmeans(Clientes[-1], centers=i)$withinss)
}

#------------------------------------------------------------------------------------
# Grafica el vector "Errores"
plot(1:K_Max, Errores, type="b", 
     xlab="Cantidad de Cluster", 
     ylab="Suma de error")