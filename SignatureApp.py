import streamlit as st
from  PIL import Image, ImageEnhance
import model_loader
sim =0
sim_score=0
predScore = 0

INPUT_FILE = "./images/input_files/"
EXTRACT_SIGN = "./images/extracted_signatures/"
INPUT_SIGN = "./images/input_signatures/"


with st.sidebar: 
    st.image("https://bitskraft.com/wp-content/uploads/2022/04/bits-kraft-logo.png")
    st.title("Signature Verification Tool")
    choice = st.radio("Navigation", ["Compare","Extract","Check", "Verify"])
    st.info("This project application helps you to process different signed Papers using Neural Network models.📝")

if choice =="Compare":
    col1,col2,col3 = st.columns( [0.5, 0.5,0.5])
    st.title("Please Upload the Signatures")
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:
        file1 = st.file_uploader("Sign-1",type=['jpg','png','jpeg','tif'])
        if file1 is not None:
            image = Image.open(file1)
            image.save(INPUT_SIGN+"sign1.png")
            st.markdown('<p style="text-align: center;">Signature-1</p>',unsafe_allow_html=True)
            st.image(image,width=300)  
    
    with col2:
        file2 = st.file_uploader("Sign-2",type=['jpg','png','jpeg','tif'])
        if file2 is not None:
            image = Image.open(file2)
            image.save(INPUT_SIGN+"sign2.png")
            st.markdown('<p style="text-align: center;">Signature-2</p>',unsafe_allow_html=True)
            st.image(image,width=300) 
    
    if file1 and file2:
        col1,col2,col3 = st.columns( [0.5, 0.5,0.5])
        with col2:
            if st.button('Compare Signature'):
                sim,sim_score = model_loader.compare(INPUT_SIGN+"sign1.png",INPUT_SIGN+"sign2.png",0)
                print (sim, sim_score)
                if sim:
                    st.success(f"Similar: {sim}")
                    st.success(f"Similarity: {round(sim_score,2)} %")
                else:
                    st.error(f"Similar: {sim}")
                    st.error(f"Similarity: {round(sim_score,2)} %")

if choice =="Extract":
    st.title("Please Upload the Cheque Image")
    exFile = st.file_uploader("",type=['jpg','png','jpeg','tif'])
    if exFile is not None:
        image = Image.open(exFile)
        image.save(INPUT_FILE+"cheq.png")
        st.image(image)     
        if st.button('Extract'):
            predScore = model_loader.extractSign("cheq.png",True)
            if predScore==0 and exFile is not None:
                st.error("Signature not found in the Image")
            else:
                
                image = Image.open(EXTRACT_SIGN+'cheq.png')
                st.image(image,caption="Extracted Image") 
                st.success(f"Score {round(predScore,2)}%")

    
    

    


