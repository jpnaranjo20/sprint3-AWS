from typing import Optional

import requests
import streamlit as st
from app.settings import API_BASE_URL
from PIL import Image
import uuid
import os


def login(username: str, password: str) -> Optional[str]:
    """This function calls the login endpoint of the API to authenticate the user
    and get a token.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if login is successful, None otherwise
    """
    # TODO MARIA: Implement the login function
    # Steps to Build the `login` Function:
    #  1. Construct the API endpoint URL using `API_BASE_URL` and `/login`.
    #  2. Set up the request headers with `accept: application/json` and
    #     `Content-Type: application/x-www-form-urlencoded`.
    #  3. Prepare the data payload with fields: `grant_type`, `username`, `password`,
    #     `scope`, `client_id`, and `client_secret`.
    #  4. Use `requests.post()` to send the API request with the URL, headers,
    #     and data payload.
    #  5. Check if the response status code is `200`.
    #  6. If successful, extract the token from the JSON response.
    #  7. Return the token if login is successful, otherwise return `None`.
    #  8. Test the function with various inputs.

    login_url = f"{API_BASE_URL}/login"

    headers = {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }

    payload={
                    "grant_type": "",
                    "username": username,
                    "password": password,
                    "scope": "",
                    "client_id": "",
                    "client_secret": "",
                }
    
    resp = requests.post(login_url, data=payload, headers=headers)

    token = None

    if resp.status_code == 200:
        token = resp.json().get("access_token")

    return token


def predict(token: str, uploaded_file: Image) -> requests.Response:
    """This function calls the predict endpoint of the API to classify the uploaded
    image.

    Args:
        token (str): token to authenticate the user
        uploaded_file (Image): image to classify

    Returns:
        requests.Response: response from the API
    """
    # TODO SIMON: Implement the predict function
    # Steps to Build the `predict` Function:
    #  1. Create a dictionary with the file data. The file should be a
    #     tuple with the file name and the file content.
    #  2. Add the token to the headers.
    #  3. Make a POST request to the predict endpoint.
    #  4. Return the response.

    # Convertir la imagen a datos binarios para poder enviarla vía HTTP    
    # file_content = uploaded_file.getvalue()

    # Extraer el formato de la imagen para poder incluirlo en la información que será enviada en el request
    # _, file_extension = os.path.splitext(file_name)

    # ALmacenar el nombre del archivo o asignarle un Universally Unique
    # Identifier (UUI) como placeholder en caso de que el usuario no haya ingresado un nombre.
    # No tengo claro cómo se podría acceder a ese UUID, tal vez sería mejor usar el username
    # del usuario. Debo revisar la función que llama a esta función para determinar qué información
    # estaría disponible, y verificar si en efecto es posisble que el usuario pueda omitir el nombre,
    # pero esto implicaría cambiar el signature de esta función y el de la que la llama.
    file_name = uploaded_file.name 
    # or f"{uuid.uuid4()}.{file_extension}"

    # Crear diccionario con los datos de la imagen (nombre y contenido)
    # Se debe añadir un dato adicional: 'image/file-extension'), ya que el protocolo HTTP
    # requiere saber el Content-Type de lo que se está enviando
    
    uploaded_file.seek(0)
    
    files = {
        'file': (file_name, uploaded_file)
                #  , f'image/{file_extension}')
    }
    
    # Crear el header con el token de autorización
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Enviar la solicitud con los headers y el diccionario de datos
    # El request puede fallar, así que conviene implementar error-handling
    # try:
    response = requests.post(f'{API_BASE_URL}/model/predict', files=files, headers=headers)
    # response.raise_for_status()
    return response
    # except requests.exceptions.RequestException as e:
        # st.error(f'An error occurred while processing the request: {e}')
        # return 
        #raise e en caso de querer propagar el error a la función que llama a esta función  


def send_feedback(
    token: str, feedback: str, score: float, prediction: str, image_file_name: str
) -> requests.Response:
    """This function calls the feedback endpoint of the API to send feedback about
    the classification.

    Args:
        token (str): token to authenticate the user
        feedback (str): string with feedback
        score (float): confidence score of the prediction
        prediction (str): predicted class
        image_file_name (str): name of the image file

    Returns:
        requests.Response: _description_
    """
    # TODO SEBAS: Implement the send_feedback function
    # Steps to Build the `send_feedback` Function:
    # 1. Create a dictionary with the feedback data including feedback, score,
    #    predicted_class, and image_file_name.
    # 2. Add the token to the headers.
    # 3. Make a POST request to the feedback endpoint.
    # 4. Return the response.
    response = None

    #1 Crear el diccionario con los datos del feedback
    data = {
        'feedback': feedback,
        'score': score,
        'predicted_class': prediction,
        'image_file_name': image_file_name
    }

    #2 Crear el header con el token de autorización
    headers = {
        'Authorization': f'Bearer {token}'
    }

    #3 Enviar la solicitud con los headers y el diccionario de datos
    # El request puede fallar, así que conviene implementar error-handling
    try:
        response = requests.post(f'{API_BASE_URL}/feedback', json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f'An error occurred while processing the request: {e}')
        return None

    return response


# Interfaz de usuario
st.set_page_config(page_title="Image Classifier", page_icon="📷")
st.markdown(
    "<h1 style='text-align: center; color: #4B89DC;'>Image Classifier</h1>",
    unsafe_allow_html=True,
)

# Formulario de login
if "token" not in st.session_state:
    st.markdown("## Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        token = login(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful!")
        else:
            st.error("Login failed. Please check your credentials.")
else:
    st.success("You are logged in!")


if "token" in st.session_state:
    token = st.session_state.token

    # Cargar imagen
    uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    print(type(uploaded_file))

    # Mostrar imagen escalada si se ha cargado
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen subida", width=300)

    if "classification_done" not in st.session_state:
        st.session_state.classification_done = False

    # Botón de clasificación
    if st.button("Classify"):
        if uploaded_file is not None:
            response = predict(token, uploaded_file)
            if response.status_code == 200:
                result = response.json()
                st.write(f"**Prediction:** {result['prediction']}")
                st.write(f"**Score:** {result['score']}")
                st.session_state.classification_done = True
                st.session_state.result = result
            else:
                st.error("Error classifying image. Please try again.")
        else:
            st.warning("Please upload an image before classifying.")

    # Mostrar campo de feedback solo si se ha clasificado la imagen
    if st.session_state.classification_done:
        st.markdown("## Feedback")
        feedback = st.text_area("If the prediction was wrong, please provide feedback.")
        if st.button("Send Feedback"):
            if feedback:
                token = st.session_state.token
                result = st.session_state.result
                score = result["score"]
                prediction = result["prediction"]
                image_file_name = result.get("image_file_name", "uploaded_image")
                response = send_feedback(
                    token, feedback, score, prediction, image_file_name
                )
                if response.status_code == 201:
                    st.success("Thanks for your feedback!")
                else:
                    st.error("Error sending feedback. Please try again.")
            else:
                st.warning("Please provide feedback before sending.")
                st.warning("Please provide feedback before sending.")

    # Pie de página
    st.markdown("<hr style='border:2px solid #4B89DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4B89DC;'>2024 Image Classifier App</p>",
        unsafe_allow_html=True,
    )
