"""
- very small amount of primary memory
- no variable names or tagged memory addresses
"""

import sys, os


# secondary memory util
def touchopen(filename, *args, **kwargs):
    try:
        os.remove(filename)
    except OSError:
        pass
    open(filename, "a").close()
    return open(filename, *args, **kwargs)


data = []
f = open('./files/stop_words.txt')
data = [f.read(1024).split(',')]  # data[0] - stop words
f.close()

data.append([])  # data[1] is line (max 80 characters)
data.append(None)  # data[2] is index of the start_char of word
data.append(0)  # data[3] is index on characters, i = 0
data.append(False)  # data[4] is flag indicating if word was found
data.append('')  # data[5] is the word
data.append('')  # data[6] is word,NNNN
data.append(0)  # data[7] is frequency

word_freqs = touchopen('word_freqs', 'rb+')
# Open the input file
f = open(sys.argv[1], 'r')

while True:
    data[1] = [f.readline()]
    if data[1] == ['']:  # end of input file
        break
    if data[1][0][len(data[1][0]) - 1] != '\n':
        data[1][0] = data[1][0] + '\n'
    data[2] = None
    data[3] = 0

    for char in data[1][0]:  # elimination of symbol c is exercise
        if data[2] == None:
            if char.isalnum():
                # start of a word
                data[2] = data[3]
        else:
            if not char.isalnum():
                # end of a word
                data[4] = False
                data[5] = data[1][0][data[2]:data[3]].lower()
                # Ignore words with len < 2, and stop words
                if len(data[5]) >= 2 and data[5] not in data[0]:
                    # if it already exists
                    while True:
                        data[6] = str(word_freqs.readline().strip(), 'utf-8')
                        if data[6] == '':
                            break;
                        data[7] = int(data[6].split(',')[1])
                        # word, no white space
                        data[6] = data[6].split(',')[0].strip()
                        if data[5] == data[6]:
                            data[7] += 1
                            data[4] = True
                            break
                    if not data[4]:
                        word_freqs.seek(0, 1)
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], 1), 'utf-8'))
                    else:
                        word_freqs.seek(-26, 1)
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], data[7]), 'utf-8'))
                    word_freqs.seek(0, 0)

                data[2] = None
        data[3] += 1

f.close()
word_freqs.flush()

del data[:]

# Let's use the first 25 entries for the top 25 words
data = data + [[]] * (25 - len(data))
data.append('')  # data[25] is word,freq from file
data.append(0)  # data[26] is freq

while True:
    data[25] = str(word_freqs.readline().strip(), 'utf-8')
    if data[25] == '':  # EOF
        break
    data[26] = int(data[25].split(',')[1])  # Read it as integer
    data[25] = data[25].split(',')[0].strip()  # word
    # Check if this word has more counts than the ones in memory
    for i in range(25):
        if data[i] == [] or data[i][1] < data[26]:
            data.insert(i, [data[25], data[26]])
            del data[26]  # delete the last element
            break

for tf in data[0:25]:
    if len(tf) == 2:
        print(tf[0], '-', tf[1])

word_freqs.close()