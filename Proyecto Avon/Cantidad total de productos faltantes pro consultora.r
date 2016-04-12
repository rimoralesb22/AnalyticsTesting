#
# 2)	Una tabla donde queremos ver para cada zona la curva por campaña de la cantidad total de 
#	productos faltantes / cantidad de consultoras de la zona. Estudiar la desviación estándar del promedio
#	de faltantes por zona sobre el último año (ene-dic 2015). 
#



# load Practice data frame into memory
#   if not alredy there
source('DBConnection.r')

rs <- dbSendQuery(con,"SELECT  f.zona,b.CAMPANA,(sum(b.cantidad) / count(b.cuenta) ) as Articulos_Consultora
FROM AVON.BACKORDER b, AVON.factura f where b.ESTADO is NULL and b.ano=2015 and b.numero=f.numero and f.zona not in (301,399)
group by   (f.zona,b.CAMPANA)
order by f.zona")

RS <- fetch(rs)


DS <- dbSendQuery(con,"SELECT  f.zona,AVG(b.cantidad) as Faltantes
FROM AVON.BACKORDER b, AVON.factura f 
WHERE b.ESTADO is NULL and
b.ano=2015 and
b.numero=f.numero and
f.zona <> 399
group by (f.zona)
order by f.zona")

ds <- fetch(DS)

desviacion <- sd(ds$faltantes)
#dotchart(t(RS))