import streamlit as st
from PIL import Image, ImageEnhance
import model_loader
import main
from fastapi import HTTPException, status
import glob


sim = 0
sim_score = 0
predScore = 0

INPUT_FILE = "./images/input_files/"
EXTRACT_SIGN = "./images/extracted_signatures/"
INPUT_SIGN = "./images/input_signatures/"
DOWNLOAD_IMAGE = "./images/download_path/"


with st.sidebar:
    st.image("https://bitskraft.com/wp-content/uploads/2022/04/bits-kraft-logo.png")
    st.title("Signature Verification Tool")
    choice = st.radio("Navigation", ["Compare", "Extract", "Verify"])


    st.info("This project application helps you to process different signed Papers using Neural Network models.📝")

if choice == "Compare":
    choice1 = st.selectbox("Please select an option", ["image - image", "image - url"])
    if choice1 == "image - image":
        col1, col2, col3 = st.columns([0.5, 0.5, 0.5])
        st.title("Please Upload the Signatures")
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            file1 = st.file_uploader("Sign-1", type=['jpg', 'png', 'jpeg', 'tif'])
            if file1 is not None:
                image = Image.open(file1)
                image.save(INPUT_SIGN+"sign1.png")
                st.markdown(
                    '<p style="text-align: center;">Signature-1</p>', unsafe_allow_html=True)
                st.image(image, width=300)

        with col2:
            file2 = st.file_uploader("Sign-2", type=['jpg', 'png', 'jpeg', 'tif'])
            if file2 is not None:
                image = Image.open(file2)
                image.save(INPUT_SIGN+"sign2.png")
                st.markdown(
                    '<p style="text-align: center;">Signature-2</p>', unsafe_allow_html=True)
                st.image(image, width=300)

        if file1 and file2:
            col1, col2, col3 = st.columns([0.5, 0.5, 0.5])
            with col2:
                if st.button('Compare Signature'):
                    sim, sim_score = model_loader.compare(
                        INPUT_SIGN+"sign1.png", INPUT_SIGN+"sign2.png", 0)
                    print(sim, sim_score)
                    if sim:
                        st.success(f"Similar: {sim}")
                        st.success(f"Similarity: {round(sim_score,2)} %")
                    else:
                        st.error(f"Similar: {sim}")
                        st.error(f"Similarity: {round(sim_score,2)} %")

    if choice1 == "image - url":
        st.title("Please Upload the Signatures")
        image = st.file_uploader("Signature Image", type=[
                                'jpg', 'png', 'jpeg', 'tif'])
        if image is not None:
            image = Image.open(image)
            image.save(INPUT_FILE+"signImg.png")
            st.image(image)
        urlSign = st.text_input("Signature Image url")
        filename = main.get_filename(DOWNLOAD_IMAGE, "signUrl.png")
        if image:
            col1, col2 = st.columns([0.5, 0.5])
            if st.button("Compare"):
                download_status= main.download_file(DOWNLOAD_IMAGE, urlSign, filename.split('/'[-1]))
                if not download_status:
                    st.error("Invalid Signature image url.")
                originalImg =  (glob.glob((f'{filename}')))
                sim, sim_score = model_loader.compare(INPUT_SIGN+"signImg.png", DOWNLOAD_IMAGE+filename, 0)
                if sim:
                    st.success(f"Similar: {sim}")
                    st.success(f"Similarity: {round(sim_score, 2)} %")
                else:
                    st.error(f"Similar: {sim}")
                    st.error(f"Signature: {round(sim_score, 2)} %")

    


if choice == "Extract":
    st.title("Please Upload the Cheque Image")
    exFile = st.file_uploader("", type=['jpg', 'png', 'jpeg', 'tif'])
    if exFile is not None:
        image = Image.open(exFile)
        image.save(INPUT_FILE+"cheq.png")
        st.image(image)
        if st.button('Extract'):
            predScore = model_loader.extractSign("cheq.png", True)
            if predScore == 0 and exFile is not None:
                st.error("Signature not found in the Image")
            else:
                image = Image.open(EXTRACT_SIGN+'cheq.png')
                st.image(image, caption="Extracted Image")
                st.success(f"Score {round(predScore,2)}%")

if choice == "Verify":
    choice2 = st.selectbox("Please select an option",["image - image", "image - url"])
    if choice2 == "image - image":
        st.title("Please Upload the Signatures")
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            file1 = st.file_uploader("Cheque Image", type=['jpg', 'png', 'jpeg', 'tif'])
            if file1 is not None:
                image = Image.open(file1)
                image.save(INPUT_FILE+"sign1.png")
                st.markdown(
                    '<p style="text-align: center;">Signature-1</p>', unsafe_allow_html=True)
                st.image(image, width=300)

        with col2:
            file2 = st.file_uploader("Sign", type=['jpg', 'png', 'jpeg', 'tif'])
            if file2 is not None:
                image = Image.open(file2)
                image.save(INPUT_FILE+"sign2.png")
                st.markdown(
                    '<p style="text-align: center;">Signature-2</p>', unsafe_allow_html=True)
                st.image(image, width=300)

        if file1 and file2:
            col1, col2, col3 = st.columns([0.5, 0.5, 0.5])
            with col2:
                if st.button('Compare Signature'):
                    predScore =  model_loader.extractSign("sign1.png", False)
                    print(EXTRACT_SIGN+"sign1.png")
                    image = Image.open(EXTRACT_SIGN+"sign1.png")
                    st.image(image, caption="Extracted Image")

                    if predScore == 0:
                        st.error("Signature not found in the Image")
                    else:
                        col1, col2 = st.columns([0.5, 0.5])
                        with col1:
                            image = Image.open(INPUT_FILE+"sign1.png")
                            st.image(image, caption="Extracted Sign - 1")
                        with col2:
                            image = Image.open(INPUT_FILE+"sign2.png")
                            st.image(image, caption="Extracted Sign - 2")
                    sim, sim_score = model_loader.compare(
                            EXTRACT_SIGN+"sign1.png", INPUT_SIGN+"sign2.png", 0)
                    if sim:
                        st.success(f"Similar: {sim}")
                        st.success(f"Similarity: {round(sim_score,2)} %")
                    else:
                        st.error(f"Similar: {sim}")
                        st.error(f"Similarity: {round(sim_score,2)} %")

    if choice2 == "image - url":
        col1, col2, col3 = st.columns([0.5, 0.5, 0.5])
        st.title("Please Upload the Signatures")
        image = st.file_uploader("Cheque Image", type=['jpg', 'png', 'jpeg', 'tif'])
        if image is not None:
            image = Image.open(image)
            image.save(INPUT_FILE+"cheqSign.png")
            st.image(image)
        urlSign = st.text_input("Signature Image url")
        filename = main.get_filename(DOWNLOAD_IMAGE, "cheqSign.png")
        if st.button('Verify'):
            download_status = main.download_file(
                DOWNLOAD_IMAGE, urlSign, filename.split('/')[-1])
            if not download_status:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=filename)
            originalImg = (glob.glob((f'{filename}')))
            predScore = model_loader.extractSign("cheqSign.png", False)
            if predScore == 0 and exFile is not None:
                st.error("Signature not found in the Image")
            else:
                col1, col2 = st.columns([0.5, 0.5])
                with col1:
                    image = Image.open(EXTRACT_SIGN+"cheqSign.png")
                    st.image(image, caption="Extracted Image")
                with col2:
                    image = Image.open(filename)
                    st.image(image, caption="Downloaded Image from URL.")
                sim, sim_score = model_loader.compare(EXTRACT_SIGN+"cheqSign.png", originalImg[0], False)
                if sim:
                    st.success(f"Similar: {sim}")
                    st.success(f"Similarity: {round(sim_score, 2)} %")
                else:
                    st.error(f"Similar: {sim}")
                    st.error(f"Similarity: {round(sim_score,2)} %")
            
