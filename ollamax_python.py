import requests
import json
import os
import base64 

base_url="https://ollama-clem.lab.sspcloud.fr"
model_name = "llama3.2-vision"

image_path = "barbadines.jpg"
with open(image_path, "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

# Construire l'URL de génération
generate_url = f"{base_url}/api/chat"
question = "donne moi l'adresse écrite sur l'image (ne me renvoie rien d'autre, n'ajoute pas de ville si tu nn'en vois pas ) ajoute un niveau de certitude entre 0 et 1"
# Préparer le corps de la requête
payload = {
    "model": model_name,
    "messages": [
        {
            "role": "user",
            "content": question,
            "images": [encoded_image] if encoded_image else []
        }
    ]
}

# Préparer les en-têtes pour inclure le JSON
headers = {"Content-Type": "application/json"}

response = requests.post(
    url=generate_url,
    data=json.dumps(payload),
    headers=headers
)


def process_streamed_response(response_text):
    """
    Traite une réponse textuelle streaming de l'API et reconstruit le contenu complet.
    
    :param response_text: str - La réponse brute (response.text) en JSON streaming.
    :return: str - Le contenu complet reconstruit.
    """
    lines = response_text.strip().split("\n")  # Découper chaque ligne du streaming
    content = []  # Liste pour collecter les morceaux de réponse

    for line in lines:
        try:
            # Charger chaque ligne comme JSON
            message = json.loads(line)
            # Extraire le champ 'content' s'il est présent
            if "message" in message and "content" in message["message"]:
                content.append(message["message"]["content"])
        except json.JSONDecodeError:
            # Ignorer les lignes mal formées
            print(f"Ligne ignorée : {line}")

    # Reconstituer la réponse complète
    return "".join(content)

# Exemple d'utilisation
response_text = response.text  # Votre réponse API
full_content = process_streamed_response(response_text)

print("Réponse complète reconstituée :")
print(full_content)