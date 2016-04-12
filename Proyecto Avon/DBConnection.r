#String de Conexion

# load utility functions
source('utils.R')

# install the xlsx package, if needed
# and load it into memory
ensure.loaded("ROracle")


drv <- dbDriver("Oracle")
host <- "5.152.182.176"
port <- 1521
servname <- "DBAVON"

connect.string <- paste("(DESCRIPTION=","(ADDRESS_LIST=","(ADDRESS=(PROTOCOL=tcp)(HOST=", host,")(PORT=", port,")))","(CONNECT_DATA=(SERVICE_NAME=", servname, ")))", sep = "")
con <- dbConnect(drv, username = "TESTER",password = "D3loi773943$",dbname=connect.string)

