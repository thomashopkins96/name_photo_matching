import torch
import clip
import os
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image


class CLIPHandler:
    def __init__(self, model: str = "ViT-B/32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(model, device=self.device)
        self.images = {
            'name': [],
            'description': [],
            'preprocessed_image': [],
            'original_image': []
        }

    def add_image(self, image_path: str, name: str, description: str):
        image = Image.open(image_path).convert("RGB")
        self.images['image_object'].append(self.preprocess(image))
        self.images['original_image'].append(image)
        self.images['description'].append(description)
        self.images['name'].append(name)

    def normalize_images(self):
        return torch.tensor(np.stack(self.images['preprocessed_image'])).cuda()

    def tokenize_description(self):
        return clip.tokenize(["This is " + desc for desc in self.images['description']]).cuda()

    def encode(self):
        image_input = self.normalize_images()
        text_tokens = self.tokenize_description()

        with torch.no_grad():
            image_features = self.model.encode_image(image_input).float()
            text_features = self.model.encode_text(text_tokens).float()

        return image_features, text_features

    def normalize_features(self, features):
        features /= features.norm(dim=-1, keepdim=True)
        return features

    def get_similarity(self, matrix_1, matrix_2):
        return matrix_1.cpu().numpy() @ matrix_2.cpu().numpy().T
