from sys import argv, exit

final_corpus = argv[1]
individual_texts = argv[2:]

def build_sents_dicts(file):

    sent_2_tags = {}
    sent = []
    tags = []
    for line in open(file):
        line = line.split()
        if len(line) > 0:
            tags.append(line[0])
            sent.append(line[1])
        else:
            sent_2_tags[tuple(sent)] = tags 
            sent = []
            tags = []
    if len(sent) > 0:
        sent_2_tags[tuple(sent)] = tags

    return sent_2_tags

sent_2_tags = build_sents_dicts(final_corpus)

for text in individual_texts:

    if 'fullCorpus' not in text and '.tagged' not in text:
        tagged_text = open(text+'.tagged', 'w')

        sent = []
        for line in open(text):
            line = line.split()
            if len(line) > 0:
                sent.append(line[1])
            else:
                tags = sent_2_tags[tuple(sent)]
                for i in range(len(sent)):
                    tagged_text.write('{}\t{}\n'.format(tags[i], sent[i]))
                sent = []
                tagged_text.write('\n')

        if len(sent) > 0:
            tags = sent_2_tags[tuple(sent)]
            for i in range(len(sent)):
                tagged_text.write('{}\t{}\n'.format(tags[i], sent[i]))

        tagged_text.close()