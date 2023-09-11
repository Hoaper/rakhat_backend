from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
import os, random


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')
girly_path = os.path.join(base_path, 'girly')
aesthetic_path = os.path.join(base_path, 'aesthetic')

def get_images(n: int, p: int, type_: ('girly', 'aesthetic')):
    path = girly_path if type_ == 'girly' else aesthetic_path

    return [os.path.join(type_, img)  for img in os.listdir(path)]


@app.get(
    "/showImage",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
)
async def show_image(src: str):
    with open(os.path.join(base_path, src), 'rb') as f:
        image = f.read()
    return Response(content=image, media_type="image/png")


@app.get("/getGirly")
async def get_girly(n: int, p: int):
    girly_images = get_images(n, p, 'girly')
    # pagination
    return girly_images[n*p-n:n*p]


@app.get("/getAesthetic")
async def get_aesthetic(n: int, p: int):
    aesthetic_images = get_images(n, p, 'aesthetic')
    
    # pagination
    return aesthetic_images[n*p-n:n*p]


@app.get("/getRandom")
async def get_random(n: int, p: int):
    all_images = get_images(n, p, 'girly') + get_images(n, p, 'aesthetic')
    random.shuffle(all_images)
    
    # pagination
    return all_images[n*p-n:n*p]

