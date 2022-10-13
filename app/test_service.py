import json
import requests

url = 'http://127.0.0.1:8000/translate/'


def test_translate_to_english():
    data = {'data': json.dumps(
        {"dest_language": "en", "source_language": "vi"})}

    files = [('file', open("./app/audio_samples/t2_0000006682.wav", 'rb'))]

    response = requests.post(url=url,
                             headers={'Accept': 'application/json'},
                             data=data,
                             files=files)

    assert response.status_code == 200
    assert response.json() == {"text": "TV volume is low"}


def test_translate_to_german():
    data = {'data': json.dumps({
        "dest_language": "de",
        "source_language": "vi"})}

    files = [('file', open("./app/audio_samples/t2_0000006682.wav", 'rb'))]

    response = requests.post(url=url,
                             data=data,
                             files=files)

    assert response.status_code == 200
    assert response.json() == {
        "text": "Die Lautstärke des Fernsehers ist niedrig"}


def test_translate_to_chinese():
    data = {'data': json.dumps({
        "dest_language": "zh-cn",
        "source_language": "vi"})}

    files = [('file', open("./app/audio_samples/t2_0000006682.wav", 'rb'))]

    response = requests.post(url=url,
                             data=data,
                             files=files)

    assert response.status_code == 200
    assert response.json() == {
        "text": "电视音量低"}


def test_translate_wrong_source_language():
    data = {'data': json.dumps({
        "dest_language": "en",
        "source_language": "en"})}

    files = [('file', open("./app/audio_samples/t2_0000006682.wav", 'rb'))]

    response = requests.post(url=url,
                             data=data,
                             files=files)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Only support Vietnamese as a source language. Please fill the bank by 'vi'."}


def test_translate_not_supported_destination_language():
    data = {'data': json.dumps({
        "dest_language": "asd",
        "source_language": "vi"})}

    files = [('file', open("./app/audio_samples/t2_0000006682.wav", 'rb'))]

    response = requests.post(url=url,
                             data=data,
                             files=files)

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Invalid target language. Please fill with the supported language by refering to https://pypi.org/project/googletrans/"}


def test_translate_without_destination_language():
    data = {'data': json.dumps({
        # "dest_language": "en",
        "source_language": "vi"})}

    files = [('file', open("./app/audio_samples/t2_0000006682.wav", 'rb'))]

    response = requests.post(url=url,
                             data=data,
                             files=files)

    assert response.status_code == 422
    assert response.json() == {'detail': [
        {'loc': ['dest_language'], 'msg': 'field required', 'type': 'value_error.missing'}]}


def test_translate_without_audio_file():
    data = {'data': json.dumps({
        "dest_language": "en",
        "source_language": "vi"})}

    response = requests.post(url=url,
                             data=data)

    assert response.status_code == 422
    assert response.json() == {'detail': [
        {'loc': ['body', 'file'], 'msg': 'field required', 'type': 'value_error.missing'}]}


def test_translate_without_source_language():
    data = {'data': json.dumps({
        "dest_language": "en"})}

    files = [('file', open("./app/audio_samples/t2_0000006682.wav", 'rb'))]

    response = requests.post(url=url,
                             data=data,
                             files=files)

    assert response.status_code == 200
    assert response.json() == {"text": "TV volume is low"}


def test_translate_add_more_attribute():
    data = {'data': json.dumps({
        "dest_language": "en",
        "source_language": "vi",
        "att": "haha"})}

    files = [('file', open("./app/audio_samples/t2_0000006682.wav", 'rb'))]

    response = requests.post(url=url,
                             data=data,
                             files=files)

    assert response.status_code == 200
    assert response.json() == {"text": "TV volume is low"}
