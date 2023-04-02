LID_GDRIVE_FOLDER=https://drive.google.com/drive/folders/1Vqf2cTqCenVu_EkOr867pO3CvzvqQcf-
ASR_GDRIVE_FOLDER=https://drive.google.com/drive/folders/1chE2FumxOxsvFMAcvhLi4KCyxV_2R-rT
ESC_GDRIVE_FOLDER=https://drive.google.com/drive/folders/1uCW0cb_2EzWCB2wu6Gk3oPvV_KDO1HlM

# download gdown
pip install gdown

# build standardizer docker image
cd ext/std \
    && make build \
    && cd ../..

# download language identification (LID) models &
# build docker image
cd ext/lid \
    && gdown $LID_GDRIVE_FOLDER -O models --folder \
    && make build \
    && cd ../..

# download automatic speech recognition (ASR) model &
# build docker image
cd ext/asr \
    && gdown $ASR_GDRIVE_FOLDER -O models --folder \
    && make build \
    && cd ../..

# download environmental sound classification (ESC) model &
# build docker image
cd ext/esc \
    && gdown $ESC_GDRIVE_FOLDER -O models --folder \
    && make build \
    && cd ../..

# build main service app docker image
docker build . -t dleongsh/speech-baseline-service:1.0.0
