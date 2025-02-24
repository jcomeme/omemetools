from inspect import cleandoc
import torch
from PIL import Image, PngImagePlugin
import numpy as np
import folder_paths
import datetime
import os
import json
import random
import time


class AsunaroWildCard:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pick_up_num": ("INT", {"default": 1, "min": 0, "max": 100, "step": 1}),
                "wildcard": ("STRING", {
                    "multiline": True,
                }),
                "delimiter": ("STRING", {"default": ",", "multiline": False}),

                "seed": ("INT:seed", {}),

            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "asunaro_wildcard"

    def asunaro_wildcard(self, wildcard, delimiter, pick_up_num, seed):
        random.seed(seed)
        w_list = wildcard.replace('\n', '').split(delimiter)

        if pick_up_num > len(w_list):
            pick_up_num = len(w_list)
            print (f"Error: pick_up_num is too large. The number of wildcards is {len(w_list)}",)
        elif pick_up_num < 1:
            return ("",)
        result = ""

        result += ",".join(random.sample(w_list, pick_up_num))
        if not result:
            return ("",)
        return (result,)

class AsunaroIfSame:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target": ("STRING",),
                "compare": ("STRING", {
                    "multiline": False,
                }),
                "if_true": ("INT", {"default": 1, "min": 0, "max": 100, "step": 1}),
                "if_false": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "asunaro_if_int"

    def asunaro_if_int(self, target, compare, if_true, if_false):
        if compare == target:
            return (if_true,)
        else:
            return (if_false,)

class AsunaroIfContain:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "haystack": ("STRING",),
                "needle": ("STRING", {
                    "multiline": False,
                }),
                "if_true": ("INT", {"default": 1, "min": 0, "max": 100, "step": 1}),
                "if_false": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "asunaro_if_contain"

    def asunaro_if_contain(self, haystack, needle, if_true, if_false):
        if needle in haystack:
            return (if_true,)
        else:
            return (if_false,)

class AsunaroIfBiggerThanZero:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target": ("INT",),
                "input": ("STRING", ),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "asunaro_if_bigger_than_zero"

    def asunaro_if_bigger_than_zero(self, target, input):
        if target > 0:
            return (input,)
        else:
            return ("",)

class AsunaroRandomDice:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "min": ("INT", {"default": 1, "min": 0, "max": 100, "step": 1}),
                "max": ("INT", {"default": 1, "min": 0, "max": 100, "step": 1}),
                "seed": ("INT:seed", {}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "asunaro_random_dice"

    def asunaro_wildcard(self, min, max, seed):
        random.seed(seed)
        result = random.randint(min, max)
        return (result,)

class AsunaroAnd:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("INT",),
                "input2": ("INT",),
                "if_true": ("INT", {"default": 1, "min": 0, "max": 100, "step": 1}),
                "if_false": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "asunaro_and"

    def asunaro_and(self, input1, input2, if_true, if_false):
        if input1 > 0 & input2 > 0:
            return (if_true,)
        return (if_false,)


class AsunaroOr:
    CATEGORY = "OmemeTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("INT",),
                "input2": ("INT",),
                "if_true": ("INT", {"default": 1, "min": 0, "max": 100, "step": 1}),
                "if_false": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "asunaro_or"

    def asunaro_or(self, input1, input2, if_true, if_false):
        if input1 > 0 | input2 > 0:
            return (if_true,)
        return (if_false,)



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


            dt_now = datetime.datetime.now()
            output_dir = os.path.join(output_dir, "asunaro")
            save_dir = os.path.join(output_dir, dt_now.strftime('%Y%m%d'))
            os.makedirs(save_dir, exist_ok=True)  # フォルダが存在しない場合は作成

            timestamp = dt_now.strftime("%Y%m%d%H%M%S")

            filename = f"{timestamp}_{idx}.png"
            file_path = os.path.join(save_dir, filename)

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
    "AsunaroWildCard": AsunaroWildCard,
    "AsunaroIfSame": AsunaroIfSame,
    "AsunaroIfContain": AsunaroIfContain,
    "AsunaroIfBiggerThanZero": AsunaroIfBiggerThanZero,
    "AsunaroRandomDice": AsunaroRandomDice,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWithAsunaroInfo": "Save with asunaro information",
    "ImageMetaDataLoader": "ImageMetaDataLoader",
    "AsunaroWildCard": "AsunaroWildCard",
    "AsunaroIfSame": "AsunaroIfSame",
    "AsunaroIfContain": "AsunaroIfContain",
    "AsunaroIfBiggerThanZero": "AsunaroIfBiggerThanZero",
    "AsunaroRandomDice": "AsunaroRandomDice",

}
