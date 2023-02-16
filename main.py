# @Time : 21-12-20
# @Author : RK
# @Company : Digiconnect
# @File : main.py
# @Software : PyCharm


from fastapi import FastAPI,HTTPException
from typing import Optional
from fastapi import FastAPI,File, Form
from fastapi.datastructures import UploadFile
import uvicorn
import shutil
import schemas
import base64
import glob
import model_loader
from fastapi.middleware.cors import CORSMiddleware

INPUT_FILE = "./images/input_files/"
EXTRACT_SIGN = "./images/extracted_signatures/"
INPUT_SIGN = "./images/input_signatures/"

REFERENCE_SIGN= "./images/ref_signatures/"

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def img_to_base64(imageFullPath):
    with open(imageFullPath,"rb") as img_file:
        encoded_image_string = base64.b64encode(img_file.read())
    return (encoded_image_string)

def save_image(image_path,image):
    with open(image_path,"wb") as buffer:
        shutil.copyfileobj(image,buffer)


@app.post("/extractor",response_model = schemas.extractor_response,status_code=200,tags=['Offline Signature Authentication'])
async def extract(image: UploadFile = File(...),clean: Optional[bool]= True):
    save_image(INPUT_FILE+image.filename,image.file)
    pred_score = model_loader.extractSign(image.filename,clean)
    if(pred_score==0):
        raise HTTPException(status_code=400, detail="Invalid Image, No signatures Found")
    else:
        encoded_image = img_to_base64(EXTRACT_SIGN+image.filename)
        result = {"pred_score":float(pred_score),"extracted_image":encoded_image}
    return{"success":True, "data":result}

@app.post("/comparer",response_model = schemas.compare_response,status_code=200,tags=['Offline Signature Authentication'])
async def compare(imagea: UploadFile = File(...), imageb: UploadFile = File(...),clean: Optional[bool]= False):
    save_image(INPUT_SIGN+imagea.filename,imagea.file)
    save_image(INPUT_SIGN+imageb.filename,imageb.file) 
    sim,sim_score = model_loader.compare(INPUT_SIGN+imagea.filename,INPUT_SIGN+imageb.filename,clean)
    result = {"sim_score":float(sim_score),"similar":sim}
    return{"success":True, "data":result}

@app.post("/checker",response_model = schemas.checker_response,status_code=200,tags=['Offline Signature Authentication'])
async def check(image: UploadFile = File(...), id: str = Form(...) ,clean: Optional[bool]= False):
    save_image(INPUT_SIGN+image.filename,image.file)
    originalImagePath=(glob.glob((f"./images/ref_signatures/{id}*")))
    if((len(originalImagePath))==1):
        sim,sim_score = model_loader.compare(INPUT_SIGN+image.filename,originalImagePath[0],clean)
        encoded_image = img_to_base64(originalImagePath[0])
        result = {"sim_score":float(sim_score),"ref_image":encoded_image,"similar":sim}
        return{"success":True, "data":result,"id":id}
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.post("/verifyer",response_model = schemas.verifyer_response,status_code=200,tags=['Offline Signature Authentication'])
async def verify(image: UploadFile = File(...), id: str = Form(...) ,clean: Optional[bool]= True):
    save_image(INPUT_FILE+image.filename,image.file)
    originalImagePath=(glob.glob((f"./images/ref_signatures/{id}*")))
    if((len(originalImagePath))==1):
        pred_score = model_loader.extractSign(image.filename,False)
        sim,sim_score = model_loader.compare(EXTRACT_SIGN+image.filename,originalImagePath[0],clean)
        encoded_ref_img = img_to_base64(originalImagePath[0])
        encoded_extract_img = img_to_base64(EXTRACT_SIGN+image.filename)
        result = {"sim_score":float(sim_score),"pred_score":pred_score,"ref_image":encoded_ref_img,"extracted_image":encoded_extract_img ,"similar":sim}
        return{"success":True, "data":result,"id":id}
    else:
        raise HTTPException(status_code=404, detail="Image not found")

if __name__ == "__main__":
    # uvicorn.run(app,host='192.168.1.1',port=8080)
    uvicorn.run(app)
