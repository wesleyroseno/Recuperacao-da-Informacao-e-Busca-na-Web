
# coding: utf-8

# ## Matrix and Vocabulary Construction

# In[ ]:


from pandas import read_csv

from scipy import sparse

from nltk import FreqDist
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


# In[ ]:


news = read_csv("../data/estadao_noticias_eleicao.csv", encoding="utf-8")


# In[ ]:


content = news.titulo + " " + news.subTitulo + " " + news.conteudo
content = content.fillna("")


# In[ ]:


def co_occurrence_matrix(corpus):
    vocab = set(corpus)
    vocab = list(vocab)
    n = len(vocab)
   
    vocab_to_index = {word:i for i, word in enumerate(vocab)}
    
    bi_grams = list(bigrams(corpus))

    bigram_freq = FreqDist(bi_grams).most_common(len(bi_grams))

    I=list()
    J=list()
    V=list()
    
    for bigram in bigram_freq:
        current = bigram[0][1]
        previous = bigram[0][0]
        count = bigram[1]

        I.append(vocab_to_index[previous])
        J.append(vocab_to_index[current])
        V.append(count)
        
    co_occurrence_matrix = sparse.coo_matrix((V,(I,J)), shape=(n,n))

    return co_occurrence_matrix, vocab_to_index


# #### Removing punctuation

# In[ ]:


tokenizer = RegexpTokenizer(r'\w+')
tokens_lists = content.apply(lambda text: tokenizer.tokenize(text.lower()))


# #### Removing stopwords

# In[ ]:


stopword_ = stopwords.words('portuguese')
filtered_tokens = tokens_lists.apply(lambda tokens: [token for token in tokens if token not in stopword_])


# #### Transforming list of lists into one list

# In[ ]:


tokens = [token for tokens_list in filtered_tokens for token in tokens_list]


# In[ ]:


matrix, vocab = co_occurrence_matrix(tokens)


# ## Consult Bigram Frequency

# In[ ]:


consultable_matrix = matrix.tocsr()


# In[ ]:


def consult_frequency(w1, w2):
    return(consultable_matrix[vocab[w1],vocab[w2]])


# #### Example

# In[ ]:


w1 = 'poucos'
w2 = 'recursos'
consult_frequency(w1, w2)

