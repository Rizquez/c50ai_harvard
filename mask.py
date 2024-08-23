import sys
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoTokenizer, TFBertForMaskedLM


# El nombre del modelo preentrenado de BERT que se utilizara
MODEL = "bert-base-uncased"

# Numero de predicciones a generar para la mascara en el texto
K = 3

# Define la fuente que se utilizara para dibujar texto en las imagenes
FONT = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 28)

# Tamaño de cada celda en la visualizacion de atencion
GRID_SIZE = 40

# Espacio que se asigna para cada palabra en la visualizacion de atencion
PIXELS_PER_WORD = 200


def main():
    text = input("Text: ")

    # Tokenizar la entrada
    # Se usa el AutoTokenizer de Hugging Face para convertir el texto en tensores (inputs)
    # El texto debe incluir el token de mascara
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    inputs = tokenizer(text, return_tensors="tf")

    # La funcion get_mask_token_index localiza la posicion del token [MASK]
    # Si no se encuentra, se termina la ejecucion
    mask_token_index = get_mask_token_index(tokenizer.mask_token_id, inputs)
    if mask_token_index is None:
        sys.exit(f"Input must include mask token {tokenizer.mask_token}.")

    # Utilizar el modelo para procesar las entradas
    # Se carga el modelo preentrenado TFBertForMaskedLM que esta diseñado para 
    # trabajar con tokens enmascarados. El modelo predice las palabras que podrian 
    # reemplazar el token enmascarado
    model = TFBertForMaskedLM.from_pretrained(MODEL)
    result = model(**inputs, output_attentions=True)

    # Generar predicciones
    # A partir de los logits de salida del modelo, se seleccionan las K mejores 
    # predicciones y se reemplaza el token [MASK] con las predicciones
    mask_token_logits = result.logits[0, mask_token_index]
    top_tokens = tf.math.top_k(mask_token_logits, K).indices.numpy()
    for token in top_tokens:
        print(text.replace(tokenizer.mask_token, tokenizer.decode([token])))

    # Visualizar las atenciones
    visualize_attentions(inputs.tokens(), result.attentions)


def get_mask_token_index(mask_token_id, inputs):
    """
    Devuelve el indice del token con el `mask_token_id` 
    especificado, o `None` si no esta presente en los `inputs`.
    """
    # Extraer la secuencia de tokens de los inputs
    token_ids = inputs['input_ids'].numpy().flatten()

    # Buscar el indice del token de mascara
    try:
        # Convierte los IDs de tokens en una lista y busca el indice del token de mascara (mask_token_id)
        return list(token_ids).index(mask_token_id)
    except ValueError:
        return None



def get_color_for_attention_score(attention_score):
    """
    Devuelve una tupla de tres enteros que representan un tono de gris para 
    la dada `puntuacion_atencion`. Cada valor debe estar en el rango [0, 255].
    """
    # Convertir el puntaje de atencion a un valor de gris
    # Multiplica el puntaje por 255 para obtener un valor de 
    # gris y crea una tupla RGB donde los tres valores son iguales
    gray_value = int(255 * attention_score)
    return (gray_value, gray_value, gray_value)


def visualize_attentions(tokens, attentions):
    """
    Elaborar una representacion grafica de las puntuaciones de autoatencion.

    Para cada capa de atencion, se debe generar un diagrama para cada cabeza 
    de atencion de la capa. Cada diagrama debe incluir la lista de `tokens` 
    en la frase. El nombre de archivo de cada diagrama debe incluir tanto el 
    numero de capa (a partir de 1) como el numero de cabeza (a partir de 1).
    """
    # Asumiendo que todas las capas tienen el mismo numero de cabezas
    num_layers = len(attentions)
    num_heads = attentions[0].shape[0]

    # Itera sobre las capas y cabezas de atencion, extrayendo los pesos de atencion y llamando a generate_diagram para crear los diagramas
    for layer_idx in range(num_layers):
        for head_idx in range(num_heads):
            attention_weights = attentions[layer_idx][0][head_idx]
            generate_diagram(layer_idx + 1, head_idx + 1, tokens, attention_weights)


def generate_diagram(layer_number, head_number, tokens, attention_weights):
    """
    Genere un diagrama que represente las puntuaciones de autoatencion para 
    una sola cabeza de atencion. El diagrama muestra una fila y una columna 
    para cada uno de los `tokens`, y las celdas estan sombreadas en funcion 
    de `attention_weights`, con celdas mas claras mas claras corresponden a 
    puntuaciones de atencion mas altas.

    El diagrama se guarda con un nombre de archivo que incluye tanto el 
    «numero_de_capa» como el «numero_de_cabeza» y `numero_cabeza`.
    """
    # Crear nueva imagen
    image_size = GRID_SIZE * len(tokens) + PIXELS_PER_WORD
    img = Image.new('RGBA', (image_size, image_size), 'black')
    draw = ImageDraw.Draw(img)

    # Dibuja cada ficha en la imagen
    for i, token in enumerate(tokens):

        # Dibujar columnas de fichas
        token_image = Image.new('RGBA', (image_size, image_size), (0, 0, 0, 0))
        token_draw = ImageDraw.Draw(token_image)
        token_draw.text(
            (image_size - PIXELS_PER_WORD, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill='white',
            font=FONT
        )
        token_image = token_image.rotate(90)
        img.paste(token_image, mask=token_image)

        # Dibujar filas de fichas
        _, _, width, _ = draw.textbbox((0, 0), token, font=FONT)
        draw.text(
            (PIXELS_PER_WORD - width, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )

    # Dibuja cada palabra
    for i in range(len(tokens)):
        y = PIXELS_PER_WORD + i * GRID_SIZE
        for j in range(len(tokens)):
            x = PIXELS_PER_WORD + j * GRID_SIZE
            color = get_color_for_attention_score(attention_weights[i][j])
            draw.rectangle((x, y, x + GRID_SIZE, y + GRID_SIZE), fill=color)

    # Guardar imagen
    img.save(f'Attention_Layer{layer_number}_Head{head_number}.png')


if __name__ == '__main__':
    main()
