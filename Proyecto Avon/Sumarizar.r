#
# Sumarizar 
#



# load Practice data frame into memory
#   if not alredy there
source('DBConnection.r')


rs <- dbSendQuery(con,"Select f.CAMPANA, f.zona, f.ANO_CAMP, sum(f.monto_neto) / count(f.cuenta) as Promedio, sum(monto_neto) as Total, count(f.cuenta) as Consultoras
From factura f 
Where f.ANO_CAMP between 2013 and 2015
group by f.CAMPANA,f.zona,f.ANO_CAMP")

RS <- fetch(rs)

head(RS)