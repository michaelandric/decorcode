#little code to get the timing info summarized
rr = read.table("AR_timings")
numsegments <- length(rr$V1)

secondsAR <- c()
minsAR <- c()

for (i in 1:numsegments)
{
    secondsAR <- c(secondsAR, as.numeric(noquote(strsplit(noquote(levels(factor(rr$V3[i]))),":")[[1]]))[2])
    minsAR <- c(minsAR, as.numeric(noquote(strsplit(noquote(levels(factor(rr$V3[i]))),":")[[1]]))[1])
}

#print(sum(secondsAR) / 60 + (sum(minsAR)))
ARtimes = (minsAR * 60) + secondsAR

rr = read.table("AWH_timings")
numsegments <- length(rr$V1)
secondsAF <- c()
minsAF <- c()

for (i in 1:numsegments)
{
    secondsAF <- c(secondsAF, as.numeric(noquote(strsplit(noquote(levels(factor(rr$V3[i]))),":")[[1]]))[2])
    minsAF <- c(minsAF, as.numeric(noquote(strsplit(noquote(levels(factor(rr$V3[i]))),":")[[1]]))[1])
}

#print(sum(secondsAF) / 60 + (sum(minsAF)))
AFtimes = (minsAF * 60) + secondsAF


movs_in_secs = c(AFtimes[2], ARtimes[2], ARtimes[11], ARtimes[7], AFtimes[12], ARtimes[8], AFtimes[5], AFtimes[1], AFtimes[7], AFtimes[3], ARtimes[10], AFtimes[6], AFtimes[4], ARtimes[1], AFtimes[13], ARtimes[5])
movs_in_secs[7] = 116   # adjustment for this movie too short estmate
movs_in_secs_final = movs_in_secs[c(4,9,16,7,8,10,6,15)]

