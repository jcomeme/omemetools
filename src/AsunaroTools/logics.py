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
import re


class AsunaroWildCard:
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pick_up_num": ("INT", {"default": 1, "min": 0, "step": 1}),
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
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target": ("STRING",),
                "compare": ("STRING", {
                    "multiline": False,
                }),
                "if_true": ("INT", {"default": 1, "min": 0, "step": 1}),
                "if_false": ("INT", {"default": 0, "min": 0, "step": 1}),
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
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "haystack": ("STRING",),
                "needle": ("STRING", {
                    "multiline": False,
                }),
                "if_true": ("INT", {"default": 1, "min": 0, "step": 1}),
                "if_false": ("INT", {"default": 0, "min": 0, "step": 1}),
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
    CATEGORY = "AsuraroTools"
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



class AsunaroAnd:
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("INT",{"default": 1}),
                "input2": ("INT",{"default": 1}),
                "input3": ("INT",{"default": 1}),
                "input4": ("INT",{"default": 1}),
                "input5": ("INT",{"default": 1}),
                "if_true": ("INT", {"default": 1, "min": 0, "step": 1}),
                "if_false": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "asunaro_and"

    def asunaro_and(self, input1, input2, input3, input4, input5, if_true, if_false):
        if input1 > 0 and input2 > 0 and input3 > 0 and input4 > 0 and input5 > 0:
            return (if_true,)
        return (if_false,)


class AsunaroOr:
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("INT",{"default": 0}),
                "input2": ("INT",{"default": 0}),
                "input3": ("INT",{"default": 0}),
                "input4": ("INT",{"default": 0}),
                "input5": ("INT",{"default": 0}),
                "if_true": ("INT", {"default": 1, "min": 0, "step": 1}),
                "if_false": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "asunaro_or"

    def asunaro_or(self, input1, input2, input3, input4, input5, if_true, if_false):
        if input1 > 0 or input2 > 0 or input3 > 0 or input4 > 0 or input5 > 0:
            return (if_true,)
        return (if_false,)



class AsunaroIntToStr:
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int": ("INT", {"default": 1, "min": 0, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "asunaro_int_to_str"

    def asunaro_int_to_str(self, int):
        return (str(int),)

class AsunaroPromptStripper:
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", ),
                "strip_words": ("STRING", ),
                "add_words": ("STRING", ),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "asunaro_prompt_stripper"

    def asunaro_prompt_stripper(self, prompt, strip_words, add_words):
        prompt_array = [s.strip() for s in re.split(r"\s*,+\s*", prompt.strip()) if s.strip()]
        strip_words_array = [s.strip() for s in re.split(r"\s*,+\s*", strip_words.strip()) if s.strip()]
        add_words_array = [s.strip() for s in re.split(r"\s*,+\s*", add_words.strip()) if s.strip()]

        filtered_list = [item for item in prompt_array if item not in strip_words_array]

        result = ", ".join(filtered_list + add_words_array)

        return (result,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "AsunaroWildCard": AsunaroWildCard,
    "AsunaroIfSame": AsunaroIfSame,
    "AsunaroIfContain": AsunaroIfContain,
    "AsunaroIfBiggerThanZero": AsunaroIfBiggerThanZero,
    "AsunaroAnd": AsunaroAnd,
    "AsunaroOr": AsunaroOr,
    "AsunaroIntToStr": AsunaroIntToStr,
    "AsunaroPromptStripper": AsunaroPromptStripper,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AsunaroWildCard": "AsunaroWildCard",
    "AsunaroIfSame": "AsunaroIfSame",
    "AsunaroIfContain": "AsunaroIfContain",
    "AsunaroIfBiggerThanZero": "AsunaroIfBiggerThanZero",
    "AsunaroAnd": "AsunaroAnd",
    "AsunaroOr": "AsunaroOr",
    "AsunaroIntToStr": "AsunaroIntToStr",
    "AsunaroPromptStripper": "AsunaroPromptStripper",
}
