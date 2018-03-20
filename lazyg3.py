import argparse

def get_alteration_words(wordlist_fname):
    list = [line.rstrip() for line in wordlist_fname]
    return list

def remove_duplicates(list_buckets):
    return list(set(list_buckets))

def remove_existing(altered_buckets, existing_buckets):
    return [x for x in altered_buckets if x not in existing_buckets]

def read_list_domains(filename):
    buckets = [line.rstrip() for line in filename]
    return buckets

# adds prefix and suffix word to each subdomain
def join_words(list_buckets, alteration_words):
    new_buckets = []
    for bucket in list_buckets:
        current_sub = bucket.split("-")
        for word in alteration_words:
            for index, value in enumerate(current_sub):
                original_sub = current_sub[index]
                current_sub[index] = current_sub[index] + word.strip()
                # join the list to make into actual subdomain (aa.bb.cc)
                actual_sub = "-".join(current_sub)
                # save full URL as line in file
                new_buckets.append(actual_sub)
                current_sub[index] = original_sub
                # second dash alteration
                current_sub[index] = word.strip() + current_sub[index]
                actual_sub = "-".join(current_sub)
                # save second full URL as line in file
                new_buckets.append(actual_sub)
                current_sub[index] = original_sub
    return new_buckets

def insert_dash(list_buckets, alteration_words):
    new_buckets = []
    for bucket in list_buckets:
        current_sub = bucket.split("-")
        for word in alteration_words:
            for index, value in enumerate(current_sub):
                for index, value in enumerate(current_sub):
                    original_sub = current_sub[index]
                    current_sub[index] = current_sub[index] + "-" + word.strip()
                    # join the list to make into actual subdomain (aa.bb.cc)
                    actual_sub = "-".join(current_sub)
                    # save full URL as line in file
                    if len(current_sub[0]) > 0 and actual_sub[:1] is not "-":
                        new_buckets.append(actual_sub)
                    current_sub[index] = original_sub
                    # second dash alteration
                    current_sub[index] = word.strip() + "-" + \
                        current_sub[index]
                    actual_sub = "-".join(current_sub)
                    # save second full URL as line in file
                    new_buckets.append(actual_sub)
                    current_sub[index] = original_sub
    return new_buckets

def insert_number_suffix_subdomains(list_buckets, alternation_words):
    new_buckets = []
    for bucket in list_buckets:
        current_sub = bucket.split("-")
        for word in range(0, 10):
            for index, value in enumerate(current_sub):
                #add word-NUM
                original_sub = current_sub[index]
                current_sub[index] = current_sub[index] + "-" + str(word)
                # join the list to make into actual subdomain (aa.bb.cc)
                actual_sub = "-".join(current_sub)
                new_buckets.append(actual_sub)
                current_sub[index] = original_sub

                #add wordNUM
                original_sub = current_sub[index]
                current_sub[index] = current_sub[index] + str(word)
                # join the list to make into actual subdomain (aa.bb.cc)
                actual_sub = "-".join(current_sub)
                new_buckets.append(actual_sub)
                current_sub[index] = original_sub
    return new_buckets

def brute_force_g3(list_buckets):
    for bucket in list_buckets:
        h = [('Host', bucket)]

        #for res in sess.fuzz(scanmode=True,url=schema+u+payload):

def write_list(filename,buckets):
    for d in buckets:
        filename.write(d+'\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="List of subdomains input", type=argparse.FileType('r'), default="-")
    parser.add_argument("-w", "--wordlist",
                        help="List of words to alter the subdomains with",
                        required=False, default="words.txt", type=argparse.FileType('r'))
    parser.add_argument("-o", "--output",
                        help="Output location for altered subdomains", type=argparse.FileType('wb'), default="-")

    args = parser.parse_args()
    alteration_words = get_alteration_words(args.wordlist)
    list_buckets = read_list_domains(args.input)

    alternate_buckets = []
    alternate_buckets += insert_dash(list_buckets, alteration_words)
    alternate_buckets += insert_number_suffix_subdomains(list_buckets, alteration_words)
    #alternate_buckets += join_words(list_buckets, alteration_words)
    
    alternate_buckets = remove_existing(alternate_buckets, list_buckets)
    alternate_buckets = remove_duplicates(alternate_buckets)
    
    write_list(args.output, alternate_buckets)
    print("Number of results: ", len(alternate_buckets))

if __name__ == "__main__":
    main()