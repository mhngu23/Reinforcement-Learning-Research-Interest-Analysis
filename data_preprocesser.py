import pandas as pd
import os
import glob
import warnings
warnings.filterwarnings("ignore")

import re

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from k_mean_clustering import k_mean_clustering

PATH = os.getcwd() + "\\data\\"

def csv_data_into_df_reader():
    """
    This function is used to read all csv files from supplied path
    """
    csv_files = glob.glob(os.path.join(PATH, "*.csv"))
    
    df = pd.DataFrame()
    for f in csv_files:
        csv = pd.read_csv(f, index_col=0)
        df = df.append(csv)
    
    return df   


def text_preprocessor(sentence):
    """
    This function is used to process the input sentence
    :param sentence: (str) The sentence to be processed
    """
    wpt = nltk.WordPunctTokenizer()
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    redundant_words = ["deep", "reinforcement", "learning", "portfolio", "optimization", "management"]

    sentence = sentence.lower() # Convert text to lower case

    sentence = re.sub('[^A-Za-z0-9]+', ' ', sentence) # Remove special characters

    sentence = ' '.join(char for char in sentence.split() if char not in stop_words)  # Remove un-needed stopwords

    sentence = ' '.join(char for char in sentence.split() if char not in redundant_words)  # Remove un-needed stopwords

    sentence = re.sub(r"'<.*?>'", "", sentence) # Remove tag

    sentence = " ".join([lemmatizer.lemmatize(char) for char in sentence.split()]) # Apply lemmatization

    return sentence


def dataframe_preprocessor(df):
    """
    This function is used to preprocessed raw dataframe
    """

    index_list = list(range(1, df.shape[0]+1))
    df.index = index_list

    df["citations_by_years"] = df["citations"]/(2023 - df["year"] + 1)

    df = df.drop_duplicates(subset=['title'], keep='first')

    df['processed_title'] = df['title'].apply(lambda x: text_preprocessor(x))

    return df

if __name__=="__main__":

    
    raw_df = csv_data_into_df_reader()

    preprocessed_df = dataframe_preprocessor(raw_df)

    preprocessed_df.to_csv(PATH + f'\\preprocessed_df.csv')

    print("----------------------------------------------------------")
    print(f"The number of articles are {str(preprocessed_df.shape[0])}")
    print("----------------------------------------------------------")


    a = 0

    while str(a) != "a":
        a = input("Press a to continue: ")

    k_mean_clustering(preprocessed_df)
    
