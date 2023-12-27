import pathlib
import textwrap
import urllib.request
import google.generativeai as genai
import PIL.Image
from fastapi import FastAPI
from pydantic import BaseModel
import os

API_KEY = os.environ.get('GeminiAPI')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')


app = FastAPI()


class Item (BaseModel):
    url: str
    hintText: str
    platform: str


@app.get('/')
async def hello():
    return "welcome, Zoomer ai API is live"


@app.post('/capta')
async def pred_class(src: Item):
    print('Capta request called with: ', src.url)
    link = src.url
    hintTexts = src.hintText
    req = urllib.request.urlretrieve(link, "SavedImage")
    img = PIL.Image.open('SavedImage')
    query = "Write a short trending instagram caption, hastags.and a short story and return result in json format"
    if len(hintTexts) > 0:
        query += 'use these hint texts' + hintTexts
    response = model.generate_content(
        [query, img])
    response.resolve()
    res = response.text.split('\n')
    caption = res[2][11:].strip()
    hashtags = res[3][14:].strip().split(',')
    story = res[4][10:].strip()
    hashtags[0] = hashtags[0][1:]
    hashtags[-2] = hashtags[-2][:-2]
    r = response.text.replace('*', '')
    result = {'caption': caption, 'hashtags': hashtags,
              'story': story, 'result': r}
    print('Capta request completed')
    return result
