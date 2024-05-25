import re
from flask import Flask, render_template, request
import os
from random import random
import numpy as np
import fnmatch
import os
import torch
import faiss
import pickle
import random
from transformers import CLIPProcessor, CLIPModel

app = Flask(__name__)
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def weighted_rand(spec):
    i, sum = 0, 0
    r = random.random()
    for i in spec:
        sum += spec[i]
        if r <= sum:
            return int(i)


def find_images_in_folder(folder_path, image_extensions=('*.jpg', '*.jpeg', '*.png', '*.gif')):
    image_files = []
    for root, _, files in os.walk(folder_path):
        for ext in image_extensions:
            for filename in fnmatch.filter(files, ext):
                full_filepath = os.path.join(root, filename)
                image_files.append(full_filepath)
    return image_files


# Tidy ids so that the back button works

image_id_to_path = {}
path_to_image_id = {}


def assign_ids_to_images():
    global image_id_to_path, path_to_image_id
    all_images = find_images_in_folder(
        os.path.join(os.getcwd(), 'static/youtube'))
    for idx, image_path in enumerate(all_images):
        # Simple ID format, can be made more complex if needed
        image_id = f"img{idx}"
        relative_image_path = image_path.split('static/')[1]
        image_id_to_path[image_id] = relative_image_path
        path_to_image_id[relative_image_path] = image_id


assign_ids_to_images()


@app.route('/query-search', methods=['GET'])
def query_search():
    query = request.args.get('query')
    query_embedding = embed_text(query)
    distances, indexes = search(query_embedding, 100)
    similar_image_paths = [index_to_path[idx].split(
        'static/')[1] for idx in indexes.flatten()]
    return render_template(
        'similar_images.html',
        images=similar_image_paths,
        path_to_image_id=path_to_image_id,
        weighted_rand=weighted_rand
    )


def load_data(file_path):
    with open(file_path, 'rb') as f:
        index, np_embeddings, path_to_index, index_to_path = pickle.load(f)
    return index, np_embeddings, path_to_index, index_to_path


faiss_index, np_embeddings, path_to_index, index_to_path = load_data(
    'data3.pkl')

# Define the search function to find the k nearest neighbors


def search(embedding, k=5):
    # Ensure the input embedding has the correct data type
    embedding = np.array(embedding).astype('float32').reshape(1, -1)
    return faiss_index.search(embedding, k)


def find_nearest_paths(input_path, k=100):
    # Get the embedding for the input path
    input_path = os.path.join(os.getcwd(), 'static/') + input_path
    # @TODO deprecate this substitution
    input_path = re.sub(r'video-search-[^/]+', 'video-search', input_path)
    print(input_path)
    input_embedding = np_embeddings[path_to_index[input_path]]
    print(input_embedding)
    # Perform the search
    distances, indexes = search(input_embedding, k)
    # Convert the indexes to paths
    print(distances, indexes)
    nearest_paths = [index_to_path[idx] for idx in indexes.flatten()]
    return [p.split('static/')[1] for p in nearest_paths]


def embed_text(text):
    inputs = processor(text=text, return_tensors="pt",
                       padding=True, truncation=True)
    with torch.no_grad():
        return clip_model.get_text_features(**inputs).numpy().tolist()


@app.route('/similar-images')
def similar_images():
    image_id = request.args.get('image_id')
    image_path = image_id_to_path.get(image_id)
    print("Backend image path received:", image_path, flush=True)
    similar_image_paths = find_nearest_paths(image_path)
    return render_template(
        'similar_images.html',
        images=similar_image_paths,
        path_to_image_id=path_to_image_id,
        weighted_rand=weighted_rand
    )


@app.route('/nearest_images')
def nearest_images():
    input_path = request.args.get('path')
    nearest_image_paths = find_nearest_paths(input_path)
    return render_template('index.html', images=nearest_image_paths)


def get_random_images(folder_path, num_images=5):
    all_images = find_images_in_folder(folder_path)
    # Ensure we do not sample more images than available
    num_images = min(num_images, len(all_images))
    random_images = np.random.choice(all_images, num_images, replace=False)
    return [img.split('static/')[1] for img in random_images]


@app.route('/')
def index():
    random_image_paths = get_random_images(os.path.join(
        os.getcwd(), 'static/youtube'), num_images=100)
    return render_template(
        'similar_images.html',
        images=random_image_paths,
        path_to_image_id=path_to_image_id,
        weighted_rand=weighted_rand
    )


if __name__ == '__main__':
    app.run(debug=True)
