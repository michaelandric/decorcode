# function that creates 1D stimulus files from the func run timings
"This does in seconds"
decoder <- function(x)
{
    stimvec = rep(0, 480)
    begends = c()
    begin = 11
    for (mm in (x))
    {   
        end = begin+mm
        #begends = c(begends, begin, end)
        #begends = c(begends, begin, (end-begin))   # for afni stim file with start time + duration
        begends = c(begends, paste(begin,":",(end-begin),sep = ""))   # for afni stim file with start time + duration
        stimvec[c(begin:end)] = 1
        begin = end+40
    }
    #begends = matrix(begends, ncol = 2, byrow = 2)
    list(stimuli_vec = stimvec, startfinish = begends)
}
stim1d = decoder(movs_in_secs[c(7,8,10)])



AV1 = c(7, 8, 10)
AV2 = c(4, 9, 16)
AV3 = c(15, 6)
SC1 = c(8, 16, 7)
SC2 = c(15, 4, 10)
SC3 = c(9, 6)
SC4 = c(7, 16, 8)
SC5 = c(4, 10, 15)
SC6 = c(6, 9)
"
decoder <- function(x)
{
    stimvec = rep(0, 320)
    begends = c()
    begin = 11/1.5
    for (mm in (x/1.5))
    {   
        end = begin+mm
        begends = c(begends, begin, end)
        stimvec[c(begin:end)] = 1
        begin = end+(40/1.5)
    }
    begends = matrix(begends, ncol = 2, byrow = 2)
    list(stimuli_vec = stimvec, startfinish = begends)
}

stimulus1d = decoder(movs_in_secs[c(7,8,10)])
"
