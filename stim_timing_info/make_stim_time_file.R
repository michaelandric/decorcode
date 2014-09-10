#Create afni ready stim timing files

source("gettimes.R")
source("decode.R")
outset <- c()
sink("AV_all3runs.1D")
for (st in list(AV1, AV2, AV3))
{
    cat(decoder(movs_in_secs[st$numid])$startfinish)
    cat("\n")
}
sink()

