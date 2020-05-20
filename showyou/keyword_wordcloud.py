from wordcloud import WordCloud
import matplotlib.pyplot as plt



text = open('constitution.txt').read()
wordcloud = WordCloud.generate(text)
wordcloud.Words

plt.figure(figsize = (12,12))
plt.imshow(wordcloud,interpolation = 'bilinear')

plt.axis("off")
plt.show()
