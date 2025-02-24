from inspect import cleandoc
import torch
from PIL import Image, PngImagePlugin
import numpy as np
import folder_paths
import datetime
import os
import json

def load_latest_workflow():
    workflow_path = os.path.join(folder_paths.base_path, "temp", "prompt.json")
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Workflow load error: {e}")
        return None

class SaveWithSimpleMeta:
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
        # prompt（workflow情報）をJSON形式で文字列化
        # ワークフローをファイルから取得する
        workflow = load_latest_workflow()
        workflow_json = json.dumps(workflow, ensure_ascii=False, indent=2) if workflow else "{}"

        # 画像が複数の場合もあるためenumerateで処理する
        for idx, img_tensor in enumerate(images):
            img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
            pil_img = Image.fromarray(img_np, mode='RGB')

            metadata = PngImagePlugin.PngInfo()
            metadata.add_text("asunaro_prompt", positive_prompt)
            metadata.add_text("asunaro_negative_prompt", negative_prompt)
            metadata.add_text("workflow", workflow_json)

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"asunaro_{timestamp}_{idx}.png"
            file_path = os.path.join(output_dir, filename)

            pil_img.save(file_path, pnginfo=metadata)
            print(f"Saved image: {file_path}", flush=True)

        return ()

    def add_ome_meta_to_image(self, text_1, text_2, images):
        # imagesはテンソル型: [batch, height, width, channels]
        # 最初の画像のみを処理する
        img_tensor = images[0]  # (height, width, 3)

        # テンソルのピクセル値は0〜1なので、0〜255に変換
        img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)

        # PIL Imageに変換 (RGB)
        pil_img = Image.fromarray(img_np, mode='RGB')

        # メタデータを追加
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("omemeta_prompt", text_1)
        metadata.add_text("omemeta_negative_prompt", text_2)

        # メタデータ付き画像を一度メモリ内で保存
        from io import BytesIO
        buffer = BytesIO()
        pil_img.save(buffer, format="PNG", pnginfo=metadata)
        buffer.seek(0)

        # メタデータ付き画像を再読み込み
        pil_img_with_metadata = Image.open(buffer)

        # PIL画像から再度テンソルに変換 (0〜1に戻す)
        img_array = np.array(pil_img_with_metadata).astype(np.float32) / 255.0
        tensor_out = torch.from_numpy(img_array).unsqueeze(0)

        return (tensor_out,)

class ImageSelector:
    CATEGORY = "OmemeTools"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"images": ("IMAGE",)}}

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "choose_image"

    def choose_image(self, images):
        brightness = [torch.mean(image.flatten()).item() for image in images]
        brightest_index = brightness.index(max(brightness))
        return (images[brightest_index],)

class Example:
    # """
    # A example node
    #
    # Class methods
    # -------------
    # INPUT_TYPES (dict):
    #     Tell the main program input parameters of nodes.
    # IS_CHANGED:
    #     optional method to control when the node is re executed.
    #
    # Attributes
    # ----------
    # RETURN_TYPES (`tuple`):
    #     The type of each element in the output tulple.
    # RETURN_NAMES (`tuple`):
    #     Optional: The name of each output in the output tulple.
    # FUNCTION (`str`):
    #     The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
    # OUTPUT_NODE ([`bool`]):
    #     If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
    #     The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
    #     Assumed to be False if not present.
    # CATEGORY (`str`):
    #     The category the node should appear in the UI.
    # execute(s) -> tuple || None:
    #     The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
    #     For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    # """
    """
    d
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """dd"""
        # """
        #     Return a dictionary which contains config for all input fields.
        #     Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
        #     Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
        #     The type can be a list for selection.
        #
        #     Returns: `dict`:
        #         - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
        #         - Value input_fields (`dict`): Contains input fields config:
        #             * Key field_name (`string`): Name of a entry-point method's argument
        #             * Value field_config (`tuple`):
        #                 + First value is a string indicate the type of field or a list for selection.
        #                 + Secound value is a config for type "INT", "STRING" or "FLOAT".
        # """
        return {
            "required": {
                "image": ("Image", { "tooltip": "This is an image"}),
                "int_field": ("INT", {
                    "default": 0,
                    "min": 0, #Minimum value
                    "max": 4096, #Maximum value
                    "step": 64, #Slider's step
                    "display": "number" # Cosmetic only: display as "number" or "slider"
                }),
                "float_field": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.001, #The value represeting the precision to round to, will be set to the step value by default. Can be set to False to disable rounding.
                    "display": "number"}),
                "print_to_screen": (["enable", "disable"],),
                "string_field": ("STRING", {
                    "multiline": False, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": "Hello World!"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    #RETURN_NAMES = ("image_output_name",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "test"

    #OUTPUT_NODE = False
    #OUTPUT_TOOLTIPS = ("",) # Tooltips for the output node

    CATEGORY = "Example"

    def test(self, image, string_field, int_field, float_field, print_to_screen):
        if print_to_screen == "enable":
            print(f"""Your input contains:
                string_field aka input text: {string_field}
                int_field: {int_field}
                float_field: {float_field}
            """)
        #do some processing on the image, in this example I just invert it
        image = 1.0 - image
        return (image,)

    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """
    #@classmethod
    #def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Example": Example,
    "ImageSelector": ImageSelector,
    "SaveWithSimpleMeta": SaveWithSimpleMeta,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Example": "Example Node",
    "ImageSelector": "Image Selector Node",
    "SaveWithSimpleMeta": "Save with simple information",
}
