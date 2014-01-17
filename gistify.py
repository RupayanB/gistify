#! /usr/bin/python

from __future__ import division
import nltk, sys, re, getopt
from nltk.corpus import stopwords
from colorama import init, Fore

__author__ = "Rupayan Basu <rb3034@columbia.edu>"
__date__ = "$Dec 3, 2013"

def get_content(infile):
    """
    returns entire body of text from a file.
    """
    try:
        f = open(infile,'r')
        txt = f.read()
        f.close()
        return txt
    except:
        print "Could not open input file.\n"
        exit(1)

def get_sentences(content):
    """
    takes a bulk of text and returns list of (id,sentence) pairs called sentuples
    performs minor preprocessing before using the punkt tokenizer 
    """
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    content = re.sub(r'\s\n\n','. ',content)    #handle subtitles in the body
    content = re.sub(r'\.\.','.',content)
    content = re.sub(r'\.\"','\".',content)     #place quotes before periods
    content = re.sub(r'\n',' ',content)          
    sentences = tokenizer.tokenize(content)
    sentuples = list()
    i = 1
    for s in sentences:
        sentuples.append((i,s))                 #number sentences from 1 to n
        i += 1
    return sentuples

def preprocess_sentences(sentuples):
    """
    takes list of (id, sentence) and returns list of (id, preprocessed_sentence)
    removes all special characters other than letters, digits and whitespaces.
    removes stop words, and performs lower casing, stemming and lemmatization.
    """
    new_sentuples = list()
    for i,s in sentuples:
        sent = re.sub(r'[^a-zA-Z0-9\s]','',s)
        tokens = nltk.word_tokenize(sent)
        #remove words which are short and not useful
        tokens = [token for token in tokens if (token not in stopwords.words('english'))]
        j = 0
        porter = nltk.PorterStemmer()
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        for token in tokens:
            #convert to lowercase
            token = token.lower()
            #use only legitimate words from a dictionary
            token = lemmatizer.lemmatize(token)
            #reduce words to their stem/root
            tokens[j] = porter.stem(token)
            j += 1
        new_sentuples.append((i,' '.join(tokens)))
    return new_sentuples

def find_edges(sentuples, threshold):
    """
    converts sentences to an undirected graph
    takes list of (id, preprocessed_sentence) and an integer threshold (default=3)
    returns list of (id1, id2) representing endges between nodes (sentences) id1 and id2
    """
    edges = list()
    for id1,u in sentuples:
        for id2,v in sentuples:
            count = 0
            if id1 != id2 and ((id1,id2) not in edges and (id2,id1) not in edges):
                words1 = set(u.split(' '))
                words2 = set(v.split(' '))
                for w in words1:
                    if w in words2:
                        count += 1
                if count >= threshold:
                    edges.append((id1,id2))
    return edges

def get_vertex_cover(edges):
    """
    Implements a linear time approximation of the Minimum Vertex Cover algorithm
    Vertex cover has size <= 2 * minimum size (optimal solution)
    returns sorted resultant list of edges
    sorting takes O(|e|log|e|) time, so total running time is in O(|e|log|e|)
    """
    C = list()
    for e in edges:
        u,v = e
        if u not in C and v not in C:
            C.append(u)
            C.append(v)
    C.sort()
    return C

def get_orig_sentences(vc_edges, sentuples):
    """
    takes result of vertex cover and original list of (id, sentences)
    returns list of (unpreprocessed) sentences selected for the summary
    """
    sentences = list()
    for i,s in sentuples:
        if i in vc_edges:
            sentences.append(s)

    return sentences

def convert_to_string(sentence_list):
    """
    Converts list of sentences to string for printing
    takes list of sentences selected for the summary and returns a string
    """
    sen_str = '\n'
    for s in sentence_list:
        sen_str += s + '\n'
    #sen_str = re.sub(r'\.','.\n',sen_str)
    return sen_str

def pretty_print(sentence_list, sentuples):
    """
    prints all sentences, with those in the summary highlighted in blue.
    """
    print "\n"
    for i,s in sentuples:
        if s in sentence_list:
            print(Fore.BLUE + s + Fore.RESET)
        else:
            print(s)
    print "\n"

def graceful_quit():
    print 'Usage1: ./gistify -i <input.txt> -s <similarity threshold> -t <test.txt> -p'
    print 'Options -o, -t and -p are optional. Use -p for pretty print.'
    sys.exit(2)

def test(tfile, sentence_list):
    """
    compares the summary with a gold standard and prints precision and recall
    """
    try:
        f = open(tfile,'r')
        txt = f.read()
        f.close()
    except:
        print "Could not open test file.\n"
        exit(1)
    
    num = 0
    test_sentuples = get_sentences(txt)
    #print test_sentuples
    for i,t in test_sentuples:
        t = t.strip()
        if t in sentence_list:
            num += 1
    if(len(sentence_list) != 0 and len(test_sentuples) != 0):
        precision = num/len(sentence_list)
        recall = num/len(test_sentuples)
    else:
        print "Division by zero error\n"
        exit(1)

    print("Precision: %.2f" %precision)
    print("Recall: %.2f" %recall)

def summarize(argv):
    ifile = ''
    tfile = ''
    pretty = False
    threshold = 3
    try:
        opts, args = getopt.getopt(argv, "hpi:s:t:")
    except getopt.GetoptError:
        graceful_quit()
    if len(opts) == 0:
        graceful_quit()
    for opt, arg in opts:
        if opt == "-i":
            ifile = arg
        elif opt == "-s":
            threshold = int(arg)
        elif opt == "-t":
            tfile = arg
        elif opt == "-p":
            pretty = True
        
    content = get_content(ifile)

    sentuples = get_sentences(content)
    #print "sentences:\n",sentuples
    preproc_sentences = preprocess_sentences(sentuples)
    #print "Preprocessed sentences:\n",preproc_sentences
    #print "sentences:\n",str(preproc_sentences)
    edges = find_edges(preproc_sentences, threshold)
    #print "edges:\n",str(edges)
    vc_edges = get_vertex_cover(edges)

    #print "Vertex Cover:\n",vc_edges
    summary = get_orig_sentences(vc_edges, sentuples)
    if pretty == True:
        pretty_print(summary, sentuples)
    else:
        print convert_to_string(summary),'\n'
        #print summary
    print "Number of sentences in article: ",str(len(sentuples))
    print "Number of sentences in summary: ",str(len(summary)),'\n'

    if tfile != '':
        test(tfile, summary)

if __name__ == '__main__':
    init()
    summarize(sys.argv[1:])

