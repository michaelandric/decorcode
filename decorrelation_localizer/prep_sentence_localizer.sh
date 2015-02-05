#!/bin/sh

# first make movie of fixation
#ffmpeg -loop 1 -r 29.97 -t 324 -i fixate.png -pix_fmt yuv420p -vcodec libx264 -vb 2000k sentence_fixation.avi

# now put them together
#ffmpeg -i sentence_fixation.avi -i sentence_localizer_run1.wav -c copy sentence_localizer_run1_movie.avi
#ffmpeg -i sentence_fixation.avi -i sentence_localizer_run2.wav -c copy sentence_localizer_run2_movie.avi

# Have to convert to codec recognized on PC in Presentation
cd /Users/andric/Documents/workspace/decorrelation/localizers/sentencestims
echo ${PWD}

ffmpeg -i sentence_fixation.avi -i sentence_localizer_run2.wav -vcodec mpeg4 sentence_localizer_run2_moviePRES.avi

