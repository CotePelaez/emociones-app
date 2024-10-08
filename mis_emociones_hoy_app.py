import streamlit as st
from openai import OpenAI
import os
import requests

# Cambiar el tamaño del texto usando CSS inyectado
st.markdown(
    """
    <style>
    .big-font {
        font-size:33px !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Inyectar CSS en la aplicación
st.markdown("""
    <style>
    .stButton button {
        background-color: #c5888a  ;
        color: white;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


# Carga de la imagen de fondo
bg_image = "fondo.jpeg"  # Cambia esto al nombre de tu imagen o la ruta si está en una subcarpeta

import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64_of_bin_file("fondo.jpeg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/jpg;base64,{bg_image}");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stSidebar"] {{
background: rgba(0, 0, 0, 0.5);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Configuración de la API de OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')

# Diccionario de emociones basado en la ruleta

# Diccionario de emociones basado en la ruleta
emociones = {
    'Alegre': {
        'Emocionado': ['Energético', 'Sensual'],
        'Creativo': ['Fascinado', 'Estimulante'],
        'Alegre': ['Juguetón', 'Divertido'],
        'Orgulloso': ['Optimista', 'Esperanzado'],
    },
    'En paz': {
        'Contento': ['Amoroso', 'Íntimo'],
        'Pensativo': ['Reflexivo', 'Receptivo'],
        'Sereno': ['Seguro', 'Agradecido'],
        'Relajado': ['Tranquilo', 'Cómodo']
    },
    'Poderoso': {
        'Orgulloso': ['Confiado', 'Exitoso'],
        'Respetado': ['Importante', 'Valioso'],
        'Valiente': ['Valioso', 'Importante'],
        'Esperanzado': ['Resiliente', 'Capaz']
    },
    'Triste': {
        'Culpable': ['Avergonzado', 'Deprimido'],
        'Confundido': ['Solo', 'Aburrido'],
        'Desamparado': ['Cansado', 'Somnoliento'],
        'Desalentado': ['Apático', 'Aislado'],
        'Desconcertado': ['Inferior', 'Estúpido'],
        'Arrepentido': ['Lamentable', 'Lo siento'],
    },
    'Enojado': {
        'Dolido': ['Distante', 'Sarcástico'],
        'Hostil': ['Enfadado', 'Egoísta'],
        'Odioso': ['Crítico', 'Odiador'],
        'Frustrado': ['Celoso', 'Irritado'],
        'Escéptico': ['Escéptico', 'Desconfiado']
    },
    'Asustado': {
        'Ansioso': ['Abrumado', 'Avergonzado'],
        'Inseguro': ['Desamparado', 'Insignificante'],
        'Rechazado': ['Sumiso', 'Desalentado'],
        'Confundido': ['Perdido', 'Perplejo'],
    }
}

st.title("Conéctate con tu emoción del día")


# Selección de la emoción principal
emocion_principal = st.selectbox("Selecciona tu emoción principal", list(emociones.keys()))

# Selección de la subemoción
subemocion = st.selectbox("Selecciona la emoción que mejor describe cómo te sientes", list(emociones[emocion_principal].keys()))

# Selección de la emoción más específica
emocion_especifica = st.selectbox("Selecciona la emoción más específica", emociones[emocion_principal][subemocion])

ubicacion = st.text_input(label="Donde estás", value="", key="hidden_input1", 
                                placeholder="Ciudad",
                                autocomplete = "on")
edad = ubicacion = st.text_input(label="Edad", value="", key="hidden_input2", 
                                placeholder="Años que tienes",
                                autocomplete = "on")
extra_info = st.text_input(label="sobre ti, si quieres", value="", key="hidden_input3",
                                placeholder="Me siento así por...")
nivel_fisico = st.selectbox("¿Cuál es tu nivel de condición física hoy?", ["Bajo", "Medio", "Alto"])

if st.button("Obtener sugerencias según tu estado de ánimo"):
    # Genera una imagen inspiradora usando una descripción del día
    client = OpenAI(api_key= openai_api_key) 
    #imagen_respuesta = client.images.generate(
    #model="dall-e-3",
    #prompt=f"Con tonos pasteles.Create an inspiring image of a day for someone who is feeling {subemocion} and lives in {ubicacion}.",
    #size="1792x1024",#1024x1792', '1792x1024
    #quality="standard",
    #n=1,
    #)
    #imagen_url = imagen_respuesta.data[0].url
    #st.write("# Tu imagen inspiradora del día:")
    #st.image(imagen_url)

    # Generar sugerencias de ejercicios y en la emoción seleccionada
    prompt = (f"Soy una persona de {edad} años con un nivel físico {nivel_fisico} que vive en {ubicacion}. "
        f"Hoy me siento {emocion_principal}, acompañado/a por sensaciones de {subemocion} y {emocion_especifica}. "
        f"{extra_info}. Considerando mi edad, condición física, ubicación y estado de ánimo, "
        f"¿qué dos acciones simples y creativas podría realizar hoy que me empoderen? "
        f"Por favor, mantén las sugerencias breves, positivas y variadas, cada una de máximo 50 caracteres.")
    
    respuesta = client.chat.completions.create(
        model = "gpt-4o-mini",
        max_tokens = 200,
        temperature = 0.8,
        messages = [{'role': 'user', 'content': prompt}]
    )
    sugerencias =  respuesta.choices[0].message.content

    # Muestra las sugerencias
    st.write("# 2 Sugerencias para ti:")
    st.write(sugerencias)
    
    # Vamos a generar una meditación personalizada para ti
    # Vamos a generar una meditación personalizada para ti
    def generar_consulta_meditacion(estado_animo, necesidad):
        client = OpenAI(api_key=openai_api_key) 
        prompt = f"""
         Soy una aplicación que sugiere meditaciones guiadas basadas en el estado de ánimo y la necesidad del usuario. El usuario se siente {estado_animo} y está buscando una meditación que le ayude a 
         {necesidad}. Genera una consulta de búsqueda específica que podría utilizarse para encontrar meditaciones relevantes en YouTube, Insight Timer, Mindful.org, Spotify, o Tara Brach.
         """
        respuesta = client.chat.completions.create(
        model="gpt-4",
        max_tokens=50,  # Reducido para mantener la consulta simple
        temperature=0.8,
        messages=[{'role': 'user', 'content': prompt}]
        )
        return respuesta.choices[0].message.content.strip()

    def construir_enlaces_meditacion(consulta):
        consulta_codificada = consulta.replace(" ", "+")
        enlaces = [
        f"https://www.youtube.com/results?search_query={consulta_codificada}",
        f"https://insighttimer.com/search?query={consulta_codificada}",
        f"https://www.mindful.org/?s={consulta_codificada}",
        f"https://open.spotify.com/search/{consulta_codificada}",
        f"https://www.tarabrach.com/?s={consulta_codificada}"
        ]
        return enlaces

    def verificar_enlace_funcional(url):
        try:
            response = requests.head(url, allow_redirects=True)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    # Generación de consulta y enlaces
    consulta = generar_consulta_meditacion(emocion_principal, subemocion)
    enlaces = construir_enlaces_meditacion(consulta)

    # Selección de un enlace funcional
    enlace_meditacion = None
    for enlace in enlaces:
        if verificar_enlace_funcional(enlace):
            enlace_meditacion = enlace
            break

    # Mostrar el enlace de la meditación personalizada
    st.write("# Meditación para tí:")

    if enlace_meditacion:
         st.markdown(f"[Haz clic aquí para tu meditación personalizada]({enlace_meditacion})")
    else:
         st.write("Lo siento, no pudimos encontrar un enlace de meditación que funcione en este momento.")

