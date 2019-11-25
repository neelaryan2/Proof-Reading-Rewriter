from nltk.corpus import wordnet
import spacy
import urllib
import json

nlp = spacy.load('en_core_web_lg')

def syn_list(word):
    url = "https://api.datamuse.com/words?ml=" + word
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    json_data = json.loads(data)
    word_list = []
    for x in json_data:
        word_list.append(x['word'])
    return word_list[:min(4, len(word_list))]

def rewrite(sentence):
    ans = []
    rewrite_types = [u'NN', u'NNS', u'JJ', u'JJS']
    pos_tokenizer = nlp(sentence)
    words = []
    for token in pos_tokenizer:
        print(token.pos_, token.text, token.tag_)
        if token.tag_ in rewrite_types:
            words.append(token.text)
    rewrited_sentence = sentence
    for word in words:
        ans.append(syn_list(word))
        # word_syn = best_syn(word)
        # rewrited_sentence = rewrited_sentence.replace(word, word_syn)
    # l=(nltk.word_tokenize(rewrited_sentence))
    # rewrited_sentence=TreebankWordDetokenizer().detokenize(l)
    # return rewrited_sentence
    return ans



def best_syn(word):
    word_list = syn_list(word)
    best_syn = ""
    best_score = 0

    for syn_word in word_list:
        use_nltk = True
        try:
            nltk_raw_word = wordnet.synsets(word)[0]
            nltk_syn_word = wordnet.synsets(syn_word)[0]
        except:
            use_nltk = False

        spacy_raw_word = nlp(word.lower())
        spacy_syn_word = nlp(syn_word.lower())

        spacy_score = spacy_raw_word.similarity(spacy_syn_word)

        if (use_nltk == True):
            nltk_score = nltk_syn_word.wup_similarity(nltk_raw_word)
            if (nltk_score == None):
                nltk_score = 0
            score = (nltk_score + spacy_score) / 2
        else:
            score = spacy_score

        if (score > best_score):
            best_score = score
            best_syn = syn_word
        if word[0].isupper():
            best_syn = best_syn.capitalize()
    # [best_score, best_syn]
    return best_syn


# class BestSyn:
#     def get_datamuse_syn_list(self):
#         url = "https://api.datamuse.com/words?ml=" + self.word
#         response = urllib.urlopen(url)
#         data = response.read().decode("utf-8")
#         json_data = json.loads(data)
#         word_list = []
#         for x in json_data:
#             word_list.append(x['word'])
#         return word_list

#     def __init__(self, word):
#         self.word = word
#         self.best_score = 0.0
#         self.best_choice = ""

#     def pull(self):
#         words_list = self.get_datamuse_syn_list()
#         for syn_word in words_list:
            # use_nltk = True
            # try:
            #     nltk_raw_word = wordnet.synsets(self.word)[0]
            #     nltk_syn_word = wordnet.synsets(syn_word)[0]
            # except:
            #     use_nltk = False

            # spacy_raw_word = nlp(unicode(self.word.lower()))
            # spacy_syn_word = nlp(unicode(syn_word.lower()))

            # spacy_score = spacy_raw_word.similarity(spacy_syn_word)

            # if (use_nltk == True):
            #     nltk_score = nltk_syn_word.wup_similarity(nltk_raw_word)
            #     if (nltk_score == None):
            #         nltk_score = 0
            #     score = (nltk_score + spacy_score) / 2
            # else:
            #     score = spacy_score

#             if (score > self.best_score):
#                 self.best_score = score
#                 self.best_choice = syn_word
#         result = [self.best_score, self.best_choice]
#         return result

#     def __del__(self):
#         self.word = False
#         self.best_score = False
#         self.best_choice = False
