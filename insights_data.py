import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import collections
import nltk
import string
from num2words import num2words

from nltk.corpus import stopwords
from collections import Counter

nltk.download('stopwords')


def split(word):
    return [char for char in word]


list_of_lengths_of_spam_mail = []
list_of_lengths_of_no_spam_mail = []
data_set_frame = pd.read_csv('Spam_Emails/Spam_Emails.csv', quotechar='"')

data_frame_for_spam = data_set_frame.query("spam == 1")
data_frame_for_no_spam = data_set_frame.query("spam == 0")
# first_row = data_frame_for_no_spam.head(1)

# print("First row Of Dataframe: ")
# print(first_row)

# list_of_all_words=[]
list_of_words_of_spam = []
list_of_words_of_no_spam = []
# data_set_frame= data_set_frame.reset_index()
for index, row in data_frame_for_spam.iterrows():
    # print(row)
    text = row['text'].lower()
    # aux_text_no_thrash =  text.split(" ")
    aux_text_no_trash = [i for i in text.split(" ") if i not in (
            ["subject:", "subject", "'", '"', "_", "/", "-", ""] + stopwords.words('english') + split(
                string.punctuation)) and not i.isdigit()]
    numbers_as_words = [num2words(i) for i in text.split(" ") if i.isdigit()]
    list_of_words_of_spam += (aux_text_no_trash + numbers_as_words)

    # print(text)
    # print("-------------------------------------------------------------------------------")
    list_of_lengths_of_no_spam_mail.append(len(aux_text_no_trash))

for index, row in data_frame_for_no_spam.iterrows():
    # print(row)
    text = row['text'].lower()
    # print(" Im here")
    # aux_text_no_thrash =  text.split(" ")
    aux_text_no_trash = [i for i in text.split(" ") if i not in (
            ["subject:", "subject", "'", '"', "_", "/", "-", ""] + stopwords.words('english') + split(
                string.punctuation)) and not i.isdigit()]
    numbers_as_words = [num2words(i) for i in text.split(" ") if i.isdigit()]

    # list_of_words_of_spam+=aux_text_no_thrash
    list_of_words_of_no_spam += (aux_text_no_trash + numbers_as_words)


    # print(text)
    # print("-------------------------------------------------------------------------------")
    list_of_lengths_of_no_spam_mail.append(len(aux_text_no_trash))

# print("past the loop Im here")
list_of_all_words = list_of_words_of_spam + list_of_words_of_no_spam

list_of_lengths_all = list_of_lengths_of_spam_mail + list_of_lengths_of_no_spam_mail

# Creating dataset
# print("Im here")

data_1 = list_of_lengths_of_spam_mail
data_2 = list_of_lengths_of_no_spam_mail

data = [data_1, data_2]

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
bp = ax.boxplot(data, patch_artist=True,
                notch='True', vert=0)

colors = ['#0000FF', '#00FF00']

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# changing color and linewidth of
# whiskers
for whisker in bp['whiskers']:
    whisker.set(color='#8B008B',
                linewidth=1.5,
                linestyle=":")

# changing color and linewidth of
# caps
for cap in bp['caps']:
    cap.set(color='#8B008B',
            linewidth=2)

# changing color and linewidth of
# medians
for median in bp['medians']:
    median.set(color='red',
               linewidth=3)

# changing style of fliers
for flier in bp['fliers']:
    flier.set(marker='D',
              color='#e7298a',
              alpha=0.5)

# x-axis labels
ax.set_yticklabels(['Spam Emails', 'Normal Emails'])

# Adding title
plt.title("Comparison of length between spam and non spam emails")

# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.xticks(np.arange(0, max(list_of_lengths_all) + 1, 250))
plt.xlabel("Number of characters in email")
# show plot
plt.savefig("insights_of_data/Comparison_length_types_emails.png")

# print(len(list_of_words_of_spam))
d = collections.defaultdict(int)
for x in list_of_words_of_spam: d[x] += 1
results = [x for x in list_of_words_of_spam if d[x] == 1]
# print(results)
print("Number of unique words in spam emails: " + str(len(results)))
# print(len(list_of_words_of_no_spam))
d = collections.defaultdict(int)
for x in list_of_words_of_no_spam: d[x] += 1
results = [x for x in list_of_words_of_no_spam if d[x] == 1]
print("Number of unique words in non spam emails: " + str(len(results)))
d = collections.defaultdict(int)
for x in list_of_all_words: d[x] += 1
results = [x for x in list_of_all_words if d[x] == 1]
print("Number of unique words across all emails: " + str(len(results)))

c = Counter(list_of_words_of_spam)

print("Most common words in spam emails (<word>,<number_occurrences>): " + str(c.most_common(20)))

c = Counter(list_of_words_of_no_spam)

print("Most common words in non spam emails (<word>,<number_occurrences>): " + str(c.most_common(20)))
