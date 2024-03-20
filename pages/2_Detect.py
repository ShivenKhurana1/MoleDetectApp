import PIL
import streamlit as st
import tensorflow as tf

st.set_page_config(
    page_title="MoleDetect",
    page_icon="♋",
    layout="centered",
    initial_sidebar_state="expanded",
)


@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model("./model/modelr.h5", compile=False)
    return model


st.title("MoleDetect Detection")
st.write("Please upload an image of a mole. Make sure to take it in good lighting to ensure the most accurate result.")
pic = st.file_uploader(
    label="Upload a picture",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
    help="Upload a picture of your skin to get a diagnosis",
)
if st.button("Predict"):
    if pic != None:
        st.header("Results")

        cols = st.columns([1, 2])
        with cols[0]:
            st.image(pic, caption=pic.name, use_column_width=True)

        with cols[1]:
            labels = [
                #"actinic keratosis",
                #"basal cell carcinoma",
                #"dermatofibroma",
                #"melanoma",
                #"nevus",
                #"pigmented benign keratosis",
                #"seborrheic keratosis",
                #"squamous cell carcinoma",
                #"vascular lesion",
                "benign",
                "malignant",
            ]

            model = load_model()

            with st.spinner("Predicting..."):
                img = PIL.Image.open(pic)
                img = img.resize((180, 180))
                img = tf.keras.preprocessing.image.img_to_array(img)
                img = tf.expand_dims(img, axis=0)

                prediction = model.predict(img)
                prediction = tf.nn.softmax(prediction)

                score = tf.reduce_max(prediction)
                score = tf.round(score * 100, 2)

                prediction = tf.argmax(prediction, axis=1)
                prediction = prediction.numpy()
                prediction = prediction[0]

                disease = labels[prediction].title()
                
                st.write(f"**Prediction:** `{disease}`")
                st.write(f"**Confidence:** `{score:.2f}%`")
                # st.info(f"The model predicts that the lesion is a **{prediction}** with a confidence of {score}%")

        st.warning(
            ":warning: This is not a medical diagnosis. Please consult a doctor for a professional diagnosis."
        )
    else:
        st.error("Please upload an image")
        
        
        
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
        st.header("How to Understand Confidence")
        st.write("##")
        st.write(
            """
            This section is mainly for those who have their diagnosis as Malignant.
            - If Confidence is 50-60%: You should still get the "mole" checked out as it not detected as Malignant depending on the Diagnosis
            - If Confidence is 61-80%: You have a high change that the diagnosis is correct. Recommended to check with Dermatologists just to be sure
            - If Confidence is 81-100%: Your chances that the diagnosis is correct is very high. Recommended to check with Dermatologist to be sure and the take further actions into removing it.
            If you believe you have Malignant, be sure to check the "Articles" page on the left side of the screen to learn more about the different types of skin cancer, to further educate yourself.
            """
        )
