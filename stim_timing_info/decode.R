# function that creates 1D stimulus files from the func run timings
#"This does in seconds. This version for inputing a set of movie ids"
#decoder <- function(x)
#{
#    stimvec = rep(0, 480)
#    begends = c()
#    begin = 11
#    for (mm in (x))
#    {   
#        end = begin+mm
#        begends = c(begends, paste(begin,":",(end-begin),sep = ""))
#        stimvec[c(begin:end)] = 1
#        begin = end+40
#    }
#    list(stimuli_vec = stimvec, startfinish = begends)
#}

#For the *_V/A suffixes: A == good Audio, scrambled video; V == good Video, scrambled audio
AV1 = list(run = "AV1", numid = c(7, 8, 10), clipid = c("AF5_AV", "AF1_AV", "AF3_AV"))
AV2 = list(run = "AV2", numid = c(4, 9, 16), clipid = c("AR7_AV", "AF7_AV", "AR5_AV"))
AV3 = list(run = "AV3", numid = c(15, 6), clipid = c("AF13_AV", "AR8_AV"))
SC1 = list(run = "SC1", numid = c(8, 16, 7), clipid = c("AF1_V", "AR5_A", "AF5_V"))
SC2 = list(run = "SC2", numid = c(15, 4, 10), clipid = c("AF13_V", "AR7_A", "AF3_A"))
SC3 = list(run = "SC3", numid = c(9, 6), clipid = c("AF7_A", "AR8_V"))
SC4 = list(run = "SC4", numid = c(7, 16, 8), clipid = c("AF5_A", "AR5_V", "AF1_A"))
SC5 = list(run = "SC5", numid = c(4, 10, 15), clipid = c("AR7_V", "AF3_V", "AF13_A"))
SC6 = list(run = "SC6", numid = c(6, 9), clipid = c("AR8_A", "AF7_V"))

"Below this dones in TRs"
decoder <- function(x)
{
    stimvec = rep(0, 320)
    begends = c()
    #begin = 11/1.5
    begin = 8
    #for (mm in (x/1.5))
    for (mm in round((x/1.5)))
    {   
        end = begin+mm
        #begends = c(begends, paste(round(begin),':',round(end), sep = ''))
        #begends = c(begends, paste(floor(begin),':',floor(end), sep = ''))
        begends = c(begends, paste(begin,':',end, sep = ''))
        stimvec[c(begin:end)] = 1
        #begin = end+(40/1.5)
        begin = end + 27
    }
    list(stimuli_vec = stimvec, startfinish = begends)
}


