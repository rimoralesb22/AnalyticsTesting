#
# utils.R
#

# ensure a package is installed and loaded into memory
# sample call:
#   ensure.loaded("qcc")
#
ensure.loaded <- function(package) {
  if (! package %in% installed.packages()[,1]) {
    cat(sprintf("Installing package %s", package))
    install.packages(package)
  }
  require(package, character.only = T)
}

