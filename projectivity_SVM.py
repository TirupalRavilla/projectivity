#####
# Description: Main train Script for SVM model
# Author: Tirupal Rao Ravilla
# Date: 04/2019
#####

import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn import linear_model, preprocessing
import os
import glob
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import nltk
from nltk import tokenize
from nltk.stem import WordNetLemmatizer
import re 
# nltk.download('stopwords')
# nltk.download('all')

from nltk.corpus import stopwords

# nltk.download('averaged_perceptron_tagger')

# data_path='./'
# os.chdir(data_path)
files=glob.glob('*.txt')

sents=[]
tagsP=[]
tagsF=[]
emptyin=[]
for f in files:
    file = open(f)
    df= pd.read_csv(file,delimiter='\t',encoding='utf-8')
    emptyin=df[df['Past'].isnull()].index.tolist()
    st=np.delete(np.array(df['sentence'].values),emptyin)
    ft=np.delete(np.array(df['Future'].values),emptyin)
    pt=np.delete(np.array(df['Past'].values),emptyin)
    sents.extend(list(st))
    tagsF.extend(list(ft))
    tagsP.extend(list(pt))
    print(emptyin)
X=np.asarray(sents)
yf=np.asarray(tagsF)
yp=np.asarray(tagsP)
print(len(X))
print(len(yf))
print(len(yp))

documents = []
stemmer = WordNetLemmatizer()
for sen in range(0, len(X)):
    document = re.sub(r'\W', ' ', str(X[sen]))
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    document = re.sub(r'^b\s+', '', document)
    document = document.lower()
    tokens=nltk.word_tokenize(document)
    bigrams = list(nltk.bigrams(tokens))
    pos_bigrams = list(nltk.bigrams([pos for (word,pos) in nltk.pos_tag(tokens)]))
#     print('bigrams: ',bigrams)
    document=[stemmer.lemmatize(word)+' '+pos for (word,pos) in nltk.pos_tag(tokens)]
#     document.extend([w1+'_'+w2 for (w1,w2) in bigrams])
#     document.extend([w1+'_'+w2 for (w1,w2) in pos_bigrams])
#     document.extend([pos for (word,pos) in nltk.pos_tag(tokens)])
#     print(document)
#     document = document.split()
#     document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)
    documents.append(document)
print(len(documents))

print(documents[1])

print(stopwords.words('english'))

from sklearn.feature_extraction.text import CountVectorizer  
vectorizer = CountVectorizer()  #, stop_words=stopwords.words('english')
X = vectorizer.fit_transform(documents).toarray()

print(X.shape)
# print(X[0][:1000])

from sklearn.feature_extraction.text import TfidfVectorizer  
tfidfconverter = TfidfVectorizer(min_df=2, max_df=0.8, stop_words=stopwords.words('english'))  
Xt = tfidfconverter.fit_transform(documents).toarray()

print(Xt.shape)
# print(Xt[0][:1000])

from sklearn.model_selection import train_test_split  
Xtr, Xts, ytr, yts = train_test_split(X, yf, test_size=0.3, random_state=42)

from sklearn import svm

# TODO:  Create a classifier: a support vector classifier
svc = svm.SVC(probability=True, kernel="linear", C=2.8, gamma=.0073,verbose=10)

svc.fit(Xtr,ytr)

yhat_ts = svc.predict(Xts)

# yhat_tr = svc.predict(Xtr)

# acc = np.mean(yhat_tr == ytr)
# print('Training Accuaracy = {0:f}'.format(acc))

acc = np.mean(yhat_ts == yts)
print('Accuaracy = {0:f}'.format(acc))

print("Future:")
unique, counts = np.unique(yf, return_counts=True)
print("Total: ",dict(zip(unique, counts)))
unique, counts = np.unique(ytr, return_counts=True)
print("Train: ",dict(zip(unique, counts)))
unique, counts = np.unique(yts, return_counts=True)
print("Test: ",dict(zip(unique, counts)))

Xtr, Xts, ytrp, ytsp = train_test_split(X, yp, test_size=0.3, random_state=42)
svcp = svm.SVC(probability=True, kernel="linear", C=2.8, gamma=.0073,verbose=10)

svcp.fit(Xtr,ytrp)

yhat_tsp = svcp.predict(Xts)

# yhat_trp = svcp.predict(Xtr)

# acc = np.mean(yhat_trp == ytrp)
# print('Training Accuaracy = {0:f}'.format(acc))

acc = np.mean(yhat_tsp == ytsp)
print('Accuaracy = {0:f}'.format(acc))

print("Past:")
unique, counts = np.unique(yp, return_counts=True)
print("Total: ",dict(zip(unique, counts)))
unique, counts = np.unique(ytrp, return_counts=True)
print("Train: ",dict(zip(unique, counts)))
unique, counts = np.unique(ytsp, return_counts=True)
print("Test: ",dict(zip(unique, counts)))

C_test = [0.1,1,2.5,5,10]
gam_test = [0.001,0.01,0.1]

nC = len(C_test)
ngam = len(gam_test)
acc = np.zeros((nC,ngam))

Xtr, Xts, ytr, yts = train_test_split(X, yf, test_size=0.3, random_state=42)

# TODO:  Print the accuracy matrix
for index_C , C in enumerate(C_test):
  for index_G , gamma in enumerate(gam_test):
    svc2 = svm.SVC(probability=True, kernel="linear", C=C, gamma=gamma, verbose=10)
    svc2.fit(Xtr,ytr)
    yhat_testing_cross = svc2.predict(Xts)
    acc[index_C , index_G ] = np.mean(yhat_testing_cross == yts)
    print(C,gamma)
    print('Acc', acc[index_C,index_G])

optimal_index_C , optimal_index_Gamma = np.unravel_index(acc.argmax(),acc.shape)

print("Maximum Accuracy",acc[optimal_index_C][optimal_index_Gamma])
print("Optimal C:", C_test[optimal_index_C])
print('Optimal Gamma:' , gam_test[optimal_index_Gamma])

Xtr, Xts, ytrp, ytsp = train_test_split(X, yp, test_size=0.3, random_state=42)

# TODO:  Print the accuracy matrix
for index_C , C in enumerate(C_test):
  for index_G , gamma in enumerate(gam_test):
    svc2 = svm.SVC(probability=True, kernel="linear", C=C, gamma=gamma, verbose=10)
    svc2.fit(Xtr,ytrp)
    yhat_testing_cross = svc2.predict(Xts)
    acc[index_C , index_G ] = np.mean(yhat_testing_cross == ytsp)
    print(C,gamma)
    print('Acc', acc[index_C,index_G])

optimal_index_C , optimal_index_Gamma = np.unravel_index(acc.argmax(),acc.shape)

print("Maximum Accuracy",acc[optimal_index_C][optimal_index_Gamma])
print("Optimal C:", C_test[optimal_index_C])
print('Optimal Gamma:' , gam_test[optimal_index_Gamma])
