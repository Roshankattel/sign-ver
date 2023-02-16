# @Time : 21-12-20
# @Author : RK
# @Company : Digiconnect
# @File : model_loader.py
# @Software : PyCharm

from pydantic import BaseModel

class extractor_result(BaseModel):
    pred_score: float
    extracted_image: str

class extractor_response(BaseModel):
    success:bool
    data:extractor_result

class compare_result(BaseModel):
    sim_score: float
    similar:bool

class compare_response(BaseModel):
    success:bool
    data:compare_result

class checker_result(BaseModel):
    sim_score: float
    similar:bool
    ref_image: str

class checker_response(BaseModel):
    id:str
    success:bool
    data:checker_result

class verifyer_result(BaseModel):
    pred_score:float
    sim_score: float
    similar:bool
    ref_image: str
    extracted_image:str
       
class verifyer_response(BaseModel):
    id:str
    success:bool
    data:verifyer_result





