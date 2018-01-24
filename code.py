import operator
import random
import re
import sets

f = open('A Christmas Carol.txt', 'r')
text = f.read()
f.close()

words = filter(None, re.split('[^A-Za-z\']+', text.lower()))

unigram = dict()
bigram = dict()
trigram = dict()

for w in words:
	if not unigram.has_key(w):
		unigram[w] = 1
	else:
		unigram[w] += 1

for i in range(len(words) - 1):
    element = (words[i], words[i + 1])
    if not bigram.has_key(element):
        bigram[element] = 1
    else:
        bigram[element] += 1

for i in range(len(words) - 2):
    element = (words[i], words[i + 1], words[i + 2])
    if not trigram.has_key(element):
        trigram[element] = 1
    else:
        trigram[element] += 1

unigram = sorted(unigram.items(), key=operator.itemgetter(1))
bigram = sorted(bigram.items(), key=operator.itemgetter(1))
trigram = sorted(trigram.items(), key=operator.itemgetter(1))

f = open('1_gram_data.csv', 'w')
for w, c in unigram:
    f.write(w + ', ' + str(c) + '\n')

f.close()

f = open('2_gram_data.csv', 'w')
for w, c in bigram:
    f.write(w[0] + ' ' + w[1] + ', ' + str(c) + '\n')

f.close()

f = open('3_gram_data.csv', 'w')
for w, c in trigram:
    f.write(w[0] + ' ' + w[1] + ' ' + w[2] + ', ' + str(c) + '\n')

f.close()

def next_word(ngram):
    N = 0
    for k, v in ngram:
        N += v
    thresh = random.randint(0, N)
    cnt = 0
    for k, v in ngram:
        cnt += v
        if cnt >= thresh:
            return k

print "\n1-GRAM SENTENCES:\n"
for j in range(5):
    sentence = ''
    for i in range(j+6):
        word = next_word([x for x in unigram])
        sentence += word + ' '
    
    print sentence

print "\n2-GRAM SENTENCES:\n"
for j in range(5):
    word = next_word([x for x in unigram])
    sentence = ''
    for i in range(j+6):
        sentence += word + ' '
        ngram = [x for x in bigram if x[0][0] == word]
        word = next_word(ngram)[1]

    print sentence

print "\n3-GRAM SENTENCES:\n"
for j in range(5):
    sentence = ''
    prev_word = next_word([x for x in unigram])
    sentence += prev_word + ' '
    ngram = [x for x in bigram if x[0][0] == prev_word]
    word = next_word(ngram)[1]
    for i in range(j+5):
        sentence += word + ' '
        ngram = [x for x in trigram if (x[0][1] == word and x[0][0] == prev_word)]
        prev_word = word
        word = next_word(ngram)[2]
    
    print sentence
