# TODO: replace FROM
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install libsndfile1 (linux soundfile package)
RUN apt-get update && apt-get install -y gcc build-essential libsndfile1 ffmpeg wget \
    && rm -rf /var/lib/apt/lists/*

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir Cython==0.29.33
RUN pip install --no-cache-dir torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu116
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV TRANSFORMERS_CACHE="/workspace/models/transformers_cache"

WORKDIR "/workspace"
CMD ["python", "src/app.py"]
