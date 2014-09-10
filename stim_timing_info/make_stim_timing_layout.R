#create timing/clip layout file experiment

source("gettimes.R")
source("decode.R")
outset <- c()
outd = NULL
for (st in list(AV1, AV2, AV3, SC1, SC2, SC3, SC4, SC5, SC6))
{
    dd = data.frame(rep(st$run, length(st$clipid)), st$clipid, decoder(movs_in_secs[st$numid])$startfinish)
    outd = rbind(outd, dd)
}

write.table(outd, "Timing_layout.txt", row.names = F, col.names = F, quote = F) 

