
import PyPDF2 
import os, sys

#import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk


def searchInPDF(filename, key):
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
    occurrences = 0
    pdfFileObj = open(filename,'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    num_pages = len(pdfReader.pages)
    count = 0
    text = ""
    while count < num_pages:
        pageObj = pdfReader.pages[count]
        count +=1
        text += pageObj.extract_text()
        print(text)
    if text != "":
       text = text
#   else:
  #     text = textract.process(filename, method='tesseract', language='eng')
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    punctuation = ['(',')',';',':','[',']',',']
    stop_words = stopwords.words('english')
    keywords = [word for word in tokens if not word in stop_words and  not word in punctuation]
    for k in keywords:
        if key == k: occurrences+=1
    return occurrences

directory = '.'
#pdf_filename = '0330.pdf'
for file in os.listdir(directory):
    if not file.endswith(".pdf"):
        continue
    pdf_filename =  os.path.join(directory,file)
    search_for = 'Word'
    result = searchInPDF(pdf_filename,search_for)
    print(result)

