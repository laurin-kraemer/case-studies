library(reticulate)
reticulate::use_condaenv("r-reticulate")
reticulate::source_python("download_spdr_holdings.py")
