import cv2

from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import MarianMTModel, MarianTokenizer
from PIL import Image
import torch

translation_models = {}
processor = None
model = None


def _load_captioning_model():
    global processor, model

    if processor is None or model is None:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        model.eval()

    return processor, model


def translate_caption(caption, target_language):
    if target_language == "en":
        return caption
    if target_language not in translation_models:
        model_name = f"Helsinki-NLP/opus-mt-en-{target_language}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        translation_model = MarianMTModel.from_pretrained(model_name)
        translation_models[target_language] = (tokenizer, translation_model)
    else:
        tokenizer, translation_model = translation_models[target_language]

    translated = translation_model.generate(**tokenizer(caption, return_tensors="pt", padding=True))
    translated_caption = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_caption


def generate_caption(image_path, language="en"):
    try:
        image = Image.open(image_path).convert("RGB")
        processor, model = _load_captioning_model()
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)

        if language != "en":
            caption = translate_caption(caption, language)

        return caption
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "An error occurred while generating the caption."


def generate_captions_for_video(video_path, language="en"):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error opening video file.")
            return ["Error opening video file."]

        captions = []
        frame_count = 0
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = max(1, int(frame_rate)) if frame_rate else 1
        processor, model = _load_captioning_model()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                inputs = processor(images=image, return_tensors="pt")

                with torch.no_grad():
                    outputs = model.generate(**inputs)
                caption = processor.decode(outputs[0], skip_special_tokens=True)

                if language != "en":
                    caption = translate_caption(caption, language)

                captions.append({"frame": frame_count, "caption": caption})

            frame_count += 1

        cap.release()

        return captions
    except Exception as e:
        print(f"Error generating captions for video: {e}")
        return ["An error occurred while generating captions."]
