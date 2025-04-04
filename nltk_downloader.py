import nltk
import os

nltk.data.path.append("/opt/render/nltk_data")

nltk.download('stopwords', download_dir="/opt/render/nltk_data")
nltk.download('wordnet', download_dir="/opt/render/nltk_data")
nltk.download('punkt', download_dir="/opt/render/nltk_data")