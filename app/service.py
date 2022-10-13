from fastapi import FastAPI, File, HTTPException, Form, status, Depends
from fastapi.encoders import jsonable_encoder
from googletrans import Translator
from app.asr_model import ASRModel
from pydantic import BaseModel, ValidationError
from typing import Optional

app = FastAPI()

# Loads translation model using googletrans to translate other language input to Vietnamese if any.
translator = Translator()

# Loads ASR model
model = ASRModel()


class Base(BaseModel):
    dest_language: str
    source_language: Optional[str] = "vi"


def checker(data: str = Form(...)):
    try:
        language = Base.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return language


@app.post('/translate/')
# async def translate(dest_language: str, source_language: str, file: bytes = File()):
async def translate(language: Base = Depends(checker), file: bytes = File()):
    """Do transform raw audio or audio file path to text by using a pretrained Vietnamese 
    ASR model. And then translate the output text to any supported languages from 
    googletrans.

    Args:
        dest_language (str): Targe language for translating from source language
        source_language (str, optional): Take output from ASR model to translate to target language. Defaults to "vi".
        file (bytes, optional): raw audio file in bytes format can be updated from computer or client sent. Defaults to File().

    Returns:
        _type_: translated text
    """

    source_language = language.source_language
    dest_language = language.dest_language

    # Only support Vietnamese as source language
    if source_language != "vi":
        raise HTTPException(
            status_code=400,
            detail="Only support Vietnamese as a source language. Please fill the bank by 'vi'."
        )

    # Model inference
    text = model.infer(file)

    # Translate from source language to target one
    translated_text = ""

    if dest_language == source_language:
        translated_text = text
    else:
        try:
            translation = translator.translate(
                text, src=source_language, dest=dest_language)
            translated_text = translation.text
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail="Invalid target language. Please fill with the supported language by refering to https://pypi.org/project/googletrans/"
            )

    return {"text": translated_text}
