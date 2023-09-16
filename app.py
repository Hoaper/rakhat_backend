from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
import os, random
from enum import Enum 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Types(Enum):
    aesthetic = "aesthetic"
    girly = "girly"
    black_white = "black_white"
    titled = "titled"

base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')
girly_path = os.path.join(base_path, 'girly')
aesthetic_path = os.path.join(base_path, 'aesthetic')
black_white_path = os.path.join(base_path, 'black_white')
titled_path = os.path.join(base_path, 'titled')

pathes = {
    Types.aesthetic: aesthetic_path,
    Types.girly: girly_path,
    Types.black_white: black_white_path,
    Types.titled: titled_path
}

def get_source_images(type_: Types):
    path = pathes[type_]

    return [os.path.join(type_.value, img)  for img in os.listdir(path)]


@app.get(
    "/showImage",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
)
async def show_image(src: str):
    try:
        return FileResponse(os.path.join(base_path, src), media_type="image/generic")
    except:
        return Response(status_code=404)


@app.get("/get_images")
async def get_images(n: int, p: int, type_: Types):
    images = get_source_images(type_)
    
    # pagination
    return images[n*p-n:n*p]


@app.get("/getRandom")
async def get_random(n: int, p: int):
    all_images = get_source_images(Types.girly) + get_source_images(Types.aesthetic) + get_source_images(Types.titled) + get_source_images(Types.black_white)
    random.shuffle(all_images)
    
    # pagination
    return all_images[n*p-n:n*p]

