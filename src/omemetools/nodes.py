from inspect import cleandoc
import torch
from PIL import Image, PngImagePlugin
import numpy as np
import folder_paths
import datetime
import os
import json


class SaveWithAsunaroInfo:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive_prompt": ("STRING", {
                    "multiline": False,
                    "default": "positive_prompt",
                }),
                "negative_prompt": ("STRING", {
                    "multiline": False,
                    "default": "negative_prompt",
                }),
                "images": ("IMAGE",),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_image_with_meta"

    def save_image_with_meta(self, positive_prompt, negative_prompt, images):
        output_dir = folder_paths.get_output_directory()
        # 画像が複数の場合もあるためenumerateで処理する
        for idx, img_tensor in enumerate(images):
            img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
            pil_img = Image.fromarray(img_np, mode='RGB')

            metadata = PngImagePlugin.PngInfo()
            metadata.add_text("asunaro_positive_prompt", positive_prompt)
            metadata.add_text("asunaro_negative_prompt", negative_prompt)

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"asunaro_{timestamp}_{idx}.png"
            file_path = os.path.join(output_dir, filename)

            pil_img.save(file_path, pnginfo=metadata)
            print(f"Saved image: {file_path}", flush=True)

        return ()




class ImageMetaDataLoader:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = False

    @classmethod
    def list_images(cls):
        input_dir = folder_paths.get_input_directory()
        valid_extensions = (".png", ".jpg", ".jpeg", ".webp")
        files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_extensions)]
        return files if files else ["no_images_found.png"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_filename": (cls.list_images(),),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "load_metadata_from_image"

    def load_metadata_from_image(self, image_filename):
        input_dir = folder_paths.get_input_directory()
        full_path = os.path.join(input_dir, image_filename)

        if not os.path.isfile(full_path):
            print(f"File not found: {full_path}")
            return ("", "")

        img = Image.open(full_path)
        metadata = img.info

        positive_prompt = metadata.get("asunaro_positive_prompt", "")
        negative_prompt = metadata.get("asunaro_negative_prompt", "")

        print(f"Positive Prompt: {positive_prompt}")
        print(f"Negative Prompt: {negative_prompt}")

        return (positive_prompt, negative_prompt)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "SaveWithAsunaroInfo": SaveWithAsunaroInfo,
    "ImageMetaDataLoader": ImageMetaDataLoader,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWithAsunaroInfo": "Save with simple information",
    "ImageMetaDataLoader": "ImageMetaDataLoader"
}
