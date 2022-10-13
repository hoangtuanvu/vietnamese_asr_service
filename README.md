# Vietnamese ASR + Google Translations
## Introduction
This simple API is to combine Automatic Speech Recognition for Vietnamese and then translate to the other supported langagues from Google Translations client 
library. I utilized FastAPI for building this (Great opensource for fast and efficient building the API applications).


## Vietnamese ASR
Please refer to the opensource https://github.com/vietai/ASR

## Google Translations client
Please refer to the opensource https://pypi.org/project/googletrans/

## Web framework (FastAPI)
Please refer to the opensource https://fastapi.tiangolo.com/

## Web UI

<p align="center">
<img src="https://github.com/hoangtuanvu/vietnamese_asr_service/blob/main/app/visualization/FastAPI.JPG" width="1280" height="640">
</p>

## Pull source code for setup
```
git pull https://github.com/hoangtuanvu/vietnamese_asr_service.git
cd vietnamese_asr_service
```

## Pretrained ASR model
Please download follow by the instruction of the source link (HuggingFace) and then copy all relevant directories and files to 'app/pretrained_models' folder.

## Build Docker Image
```
docker build -t vi_asr_image .
```

## Run API
```
docker run -d --name vi_asr -p 8000:80 vi_asr_image:latest
```

or do it locally

```
uvicorn app.service:app --host 0.0.0.0 --port 8000
```

## Mockup API testing
```
pip install pytest
pytest app/test_service.py
```

Note: Please note that, there are some common use-cases. You then add more if needed.

## Use WebUI
Please open the WebUI followed by
```
http://host:port/docs
```

And then fill data input such as 'file' and 'data'.