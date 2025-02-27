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


class AsunaroRandomDice:
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "min": ("INT", {"default": 1, "min": 0, "step": 1}),
                "max": ("INT", {"default": 1, "min": 0, "step": 1}),
                "seed": ("INT:seed", {}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "asunaro_random_dice"

    def asunaro_random_dice(self, min, max, seed):
        random.seed(seed)
        result = random.randint(min, max)
        return (result,)


class AsunaroAutomaticSexPrompter:
    CATEGORY = "AsuraroTools"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sex_mode": (["sex", "fellatio"], {"default": "sex"}),
                "insertion": (["deep", "normal", "imminent"], {"default": "normal"}),
                "cum": (["none", "normal", "excessive"], {"default": "none"}),
                "panty": (["on", "aside", "off", "random"]),
                "bra": (["on", "aside", "off", "random"]),
                "topless": ("BOOLEAN", ),
                "bottomless": ("BOOLEAN", ),
                "face": (['random', "use_face_string"], {"default": ""}),
                "face_string": ('STRING', {"default": ""}),
                "angle": (['random', "use_angle_string"], {"default": "random"}),
                "angle_string": ('STRING', {"default": ""}),
                "lighting": (['random', "use_lighting_string"], {"default": "random"}),
                "lighting_string": ('STRING', {"default": ""}),
                "focus": (["face", "pussy", "none", "random"], {"default": "none"}),
                "min_number_of_penis": ("INT", {"default": 1}),
                "max_number_of_penis": ("INT", {"default": 1}),
                "seed": ("INT:seed", {}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "asunaro_auto_sex"

    def asunaro_auto_sex(self, sex_mode, insertion, cum, panty, bra, topless, bottomless, face, face_string, angle, angle_string, lighting, lighting_string, focus, min_number_of_penis, max_number_of_penis, seed):
        random.seed(seed)
        positive_prompt = []
        negative_prompt = []
        face_option = ["ahegao", "frown", "ahegao", "frown", "disgust", "angry, ahegao", "angry", "surprized", "scared", "disgust"]
        angle_option = ["ceiling", "character focus", "cinematic angle", "close to viewer", "dutch angle", "dynamic angle", "feet out of frame", "fisheye lens", "from above", "from behind", "from below", "from side", "front view", "full body", "intense angle", "on screen of smartphone camera app frame"]
        lighting_option = ["volumetric lighting", "cinematic lighting", "rim lighting", "dynamic lighting","dimly light", "crepuscular rays", "bokeh"]

        #nothing = ["mating press", "full nelson", "piledriver", "reverse suspended congress", ]
        handjob = ["spitroast", "doggystyle", "amazon position", "legs over head", "reverse cowgirl position", "bent over", "cowgirl position", "girl on top", "missionary"]
        blowjob = ["full nelson", "knees to chest", "doggystyle", "amazon position", "legs over head", "reverse cowgirl position", "bent over", "cowgirl position", "girl on top", "missionary"]
        #bandjob_blowjob = ["amazon position", "legs over head", "spooning"]
        kissing = ["upright straddle", "suspended congress", "reverse upright straddle", "knees to chest", "legs over head", "spooning", "legs over head", "spooning", "boy on top", "bent over", "girl on top", "missionary"]
        grabbing_breast = ["spitroast", "full nelson", "piledriver", "reverse suspended congress", "amazon position", "legs over head", "spooning", "doggystyle", "boy on top", "bent over", "cowgirl position", "missionary"]
        grabbing_hair = ["spitroast", "full nelson", "piledriver", "mating press", "reverse suspended congress", "knees to chest", "legs over head", "spooning", "prone bone", "top-down bottom-up", "doggystyle", "reverse cowgirl position", "boy on top", "bent over", "cowgirl position", "girl on top", "missionary"]
        grabbing_waist = ["spitroast", "mating press", "reverse suspended congress", "amazon position", "doggystyle", "reverse cowgirl position", "boy on top", "bent over", "cowgirl position", "missionary"]
        grabbing_hands = ["prone bone", "top-down bottom-up", "doggystyle", "reverse cowgirl position", "boy on top", "bent over", "cowgirl position", "missionary"]

        if face == "face_string":
            positive_prompt.append(face_string)
        else:
            positive_prompt.append(random.choice(face_option))


        num_of_penis = random.randint(min_number_of_penis, max_number_of_penis)
        if num_of_penis == 1:
            positive_prompt.append("1boy")
            positive_prompt.append("penis")
        elif num_of_penis > 1:
            boys = f"{num_of_penis}boys"
            positive_prompt.append(boys)
            positive_prompt.append("multiple penises")


        if(sex_mode == "sex"):

            if insertion == "deep":
                positive_prompt.append("having a sex, deep insertion")
            elif insertion == "normal":
                positive_prompt.append("having a sex, insertion")
            elif insertion == "imminent":
                positive_prompt.append("imminent sex, imminent insertion")

            sex_option = ["spitroast ", "reverse upright straddle", "mating press", "full nelson", "amazon position", "legs over head", "spooning", "suspended congress", "piledriver", "knees to chest", "reverse suspended congress", "upright straddle", "prone bone", "top-down bottom-up", "doggystyle", "reverse cowgirl position", "boy on top", "bent over", "cowgirl position", "girl on top", "missionary"]
            sex = random.choice(sex_option)
            positive_prompt.append(sex)


            if num_of_penis > 1:
                options = [
                    ["handjob", ""],
                    ["blowjob", ""],
                    ["kissing, forced kiss", "", ""],
                    ["grabbing_breast", "grabbing_breast", ""],
                    ["grabbing_hair", "grabbing_hair", ""],
                    ["grabbing_waist", ""],
                    ["grabbing_hands", ""]
                ]
            else:
                options = [
                    [""],
                    [""],
                    ["kissing, forced kiss", "kissing, forced kiss", ""],
                    ["grabbing_breast", ""],
                    ["grabbing_hair", ""],
                    ["grabbing_waist", ""],
                    ["grabbing_hands", ""]
                ]
            for item in [handjob, blowjob, kissing, grabbing_breast, grabbing_hair, grabbing_waist, grabbing_hands]:
                index = 0
                if(sex in item):
                    item.append("")
                    rst = random.choice(options[index])
                    if rst != "":
                        positive_prompt.append(rst)
                index += 1

            if focus == "face":
                positive_prompt.append("face forcus, headshot")
            elif focus == "pussy":
                positive_prompt.append("pussy forcus")
            elif focus == "random":
                positive_prompt.append(random.choice(["face forcus, headshot", "pussy forcus"]))

        else:
            fellatio = ["fellatio", "irrumatio", "handjob", "penis on face"]
            positive_prompt.append(random.choice(fellatio))
            positive_prompt += ["face forcus", "headshot"]


        if topless:
            positive_prompt.append("(topless:1.2)")
        if bottomless:
            positive_prompt.append("(bottomless:1.2)")

        if panty == "random":
            panty = random.choice(["on", "aside", "off"])
        if panty == "on":
            positive_prompt.append("panty")
            negative_prompt.append("pussy")
        elif panty == "aside":
            positive_prompt.append(["panty, panty aside"])
        elif panty == "off":
            negative_prompt.append("panty")

        if bra == "random":
            bra = random.choice("on", "aside", "off")
        if bra == "on":
            positive_prompt.append("bra")
            negative_prompt.append("nipple")
        elif bra == "aside":
            positive_prompt.append("bra, nipple")
        elif panty == "off":
            negative_prompt.append("bra")

        cum_option = ["cum on face", "cum in mouth", "cum on body", "cum on hair", "cum in pussy"]
        cum_count = random.randint(1, 3)
        cums = []
        if cum == "none":
            pass
        elif cum == "normal":
            cums = random.sample(cum_option, cum_count)
        elif cum == "excessive":
            cums = random.sample(cum_option, cum_count)
            cums.append("excessive cum")
        positive_prompt += cums



        if angle == "angle_string":
            positive_prompt.append(angle_string)
        else:
            positive_prompt.append(random.choice(angle_option))

        if lighting == "lighting_string":
            positive_prompt.append(lighting_string)
        else:
            positive_prompt.append(random.choice(lighting_option))

        positive_prompt = ",".join(positive_prompt)
        negative_prompt = ",".join(negative_prompt)

        return (positive_prompt, negative_prompt)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "AsunaroRandomDice": AsunaroRandomDice,
    "AsunaroAutomaticSexPrompter": AsunaroAutomaticSexPrompter,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AsunaroRandomDice": "AsunaroRandomDice",
    "AsunaroAutomaticSexPrompter": "AsunaroAutomaticSexPrompter",
}
