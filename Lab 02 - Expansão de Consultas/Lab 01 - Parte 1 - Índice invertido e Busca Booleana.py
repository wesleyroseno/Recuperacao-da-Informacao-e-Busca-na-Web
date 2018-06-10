
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


import pandas as pd


# In[3]:


from nltk import word_tokenize


# In[4]:


news = pd.read_csv('noticias_estadao.csv', sep=',', index_col='idNoticia')


# In[5]:


news = news.sort_index(ascending=True)


# # Transforma o texto de cada celula da tabela, em uma lista das palavras do texto, em letras minusculas. E remove pontos finais de cada palavra.

# In[6]:


for i in range(1, len(news) + 1):
    for j in range(len(news.ix[i])):
        news.ix[i][j] = str(news.ix[i][j]) #força que a celula seja uma string, para uso da função lower()
        news.ix[i][j] = list(set(word_tokenize(news.ix[i][j].lower(), language='portuguese')))


# # Cria um índice invertido das palavras dos documentos, onde associa cada palavra aos documentos que ela se encontra.

# In[7]:


reference_list = {}

for i in range(1, len(news) + 1):
    for j in range(len(news.ix[i])):
        for k in news.ix[i][j]:
            if(reference_list.setdefault(k, None) == None):
                reference_list[k] = [i]                
            elif(reference_list[k][-1] != i):    
                reference_list[k].append(i)


# # FUNÇÕS DE BUSCA

# In[8]:


def search_one_term(word):
    return list(reference_list[word])


# In[9]:


def search_or_n_terms(words):
    result = reference_list[words[0]]
    
    for i in range(1, len(words)):
                result = np.union1d(result, reference_list[words[i]])
                # result é o resultado de sucessivas buscas AND das palavras
                
                return list(result)        


# In[10]:


def smaller_terms(words):
    smaller = 0
    
    for i in range(1, len(words)):
            if (len(reference_list[words[smaller]]) > len(reference_list[words[i]])): 
                    smaller = i # posição da palavra com menos documentos
                    
    words[0], words[smaller] = words[smaller], words[0]
    #coloca o termo presente em menos documentos na posição inicial da lista
                    
    return None # função com efeito colateral


# In[11]:


def search_and_n_terms(words):
    if (len(words) > 2):
        smaller = smaller_terms(words)
            
    result = reference_list[words[0]]
    
    for i in range(1, len(words)):
                result = np.intersect1d(result, reference_list[words[i]])
                # result é o resultado de sucessivas buscas OR das palavras
                
    return list(result)


# # Função que trata e identifica a entrada, para selecionar a função de busca

# In[12]:


def search(terms):
    words = terms.lower().split(" ")
    
    if(len(words) == 1):
        return search_one_term(words[0])
        
    if(words[1] == 'or'):
        return search_or_n_terms([words[0],words[2]])
    
    elif(words[1] == 'and'):
            return search_and_n_terms([words[0],words[2]])
        
    else:
        return search_and_n_terms(words)


# # TESTES

# In[13]:


assert len(search("debate OR presidencial")) == 1770


# In[14]:


assert len(search("debate AND presidencial")) == 201


# In[15]:


assert len(search("presidenciáveis OR corruptos")) == 164


# In[16]:


assert len(search("presidenciáveis AND corruptos")) == 0


# In[17]:


assert len(search("Belo OR Horizonte")) == 331


# In[18]:


assert len(search("Belo AND Horizonte")) == 242


# In[19]:


len (search("candidatos"))


# In[20]:


len(search("PT não pode se queixar afirma futuro articulador"))

