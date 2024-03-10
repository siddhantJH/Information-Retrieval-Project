import os
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')

# Define path to the base directory
base_directory = '/workspaces/Information-Retrieval-Project/Collected pages'

# Function to preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Remove punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in stripped if word not in stop_words]
    
    # Join words back into a single string
    preprocessed_text = ' '.join(words)
    
    return preprocessed_text

# Function to process HTML content using BeautifulSoup
def process_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ')
    return text

# Preprocess data.txt files in each folder
for folder_name in os.listdir(base_directory):
    folder_path = os.path.join(base_directory, folder_name)
    
    if os.path.isdir(folder_path):
        data_file_path = os.path.join(folder_path, 'data.txt')
        
        if os.path.exists(data_file_path):
            # Read data from data.txt
            with open(data_file_path, 'r') as file:
                data = file.read()
            
            # Preprocess text
            preprocessed_data = preprocess_text(data)
            
            # Process HTML content using BeautifulSoup
            preprocessed_data = process_html(preprocessed_data)
            
            # Write preprocessed data back to data.txt
            with open(data_file_path, 'w') as file:
                file.write(preprocessed_data)
