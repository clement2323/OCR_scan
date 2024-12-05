from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer
import requests 
from io import BytesIO
from PIL import Image

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')

chemin_image = "elle_sapelle.jpg"
img = Image.open(chemin_image)
img = img.convert("RGB")

pixel_values = processor(images=img, return_tensors="pt").pixel_values
generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

##Chat GPT
## Cas bizarres wereas -> rue
## appariement avec base de données d'adresses existantes (éappariement flou")
## valache -> Valoche 