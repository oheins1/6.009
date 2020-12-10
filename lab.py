# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences

class Trie:
    def __init__(self, type_=None):
        self.value = None
        self.children = dict()
        self.type = None



    def set(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.

        """

        #key = ordered sequence, tuple or str
        #store key by prefix, so essentially i am crearting a prefix tree with the keys associated with each 
        #node stored in the edhe connecting it to the longer prefix, and then a final value

        #set self.type to the type of the key (tup, str)
        if self.type == None:
            self.type = type(key)
        #base case, empty key
        if len(key) == 0:
            return None
        #find first key
        fir_key = key[:1]
        #raise TypeError if key is wrong type
        if self.type != type(key):
            raise TypeError
        #if key is already in children dict, find the key's children
        if fir_key in self.children:
            new_children = self.children[fir_key]
        #if key is not in children dict, create new Trie and create first children
        else:
            new_children = Trie() 
            self.children[fir_key] = new_children 
        #base case, set children to value
        if len(key) == 1:
            new_children.value = value 
        #otherwise recursing add children by each recusrive call of key until len(key) is 1
        else:
            next1 = key[1:]
            new_children.set(next1, value)        

    



    def get(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.
        """

        #find node of key

        node = self.get_end_node(key)
        #if key not in trie (ie value is None), raise KeyError
        if node.value == None:
            raise KeyError
        #otherwise return node's value
        else:

            return node.value

    def get_end_node(self, key):
        """
        finds node for a given key recursively
        """
        first_child = key[:1]
     
        
        if type(key) != self.type:
            raise TypeError
       
        #recursve call until node is found, when the key has a length of 1
        if len(key) == 1:
            return self.children[first_child]
        else:
            return self.children[first_child].get_end_node(key[1:])

        

    def delete(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        #find node of key and set value to None

        node = self.get_end_node(key)
        node.value = None
       
        
    def contains(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        #if value of key cannot be found, key DNE is trie, so return False
        try:
            self.get(key)
            return True
        except:
            return False
        
    def items(self, key = 'empty44442'):
        """
        Returns a list of (key, value) pairs for all keys/values in this trie and
        its children.
        """

        #set initial key value to type (str or tup)

        if key == 'empty44442':
            key = self.get_type()


       #iterate through all children 
        for c in self.children: 
            #case where type is string, set word equal to str of child
            if self.type == str: 
                word = key + str(c) 
            #tuple casd, set word eqault o tuple of child
            if self.type == tuple: 
                word = tuple(key) + tuple(c)
            #if no more children break, all pairs have been generated
            if self.children == None: 
                break
            #otherwise, yield children's child's recursively finding each (k,v) pair
            else:
                yield from self.children[c].items(word)
        if self.value != None: 
            yield (key, self.value) 


    def get_type(self):
        '''findings type of trie and returns appropriate data structure
        '''
        if self.type == str:
            key = ''
        if self.type == tuple:
            key = tuple()

        return key



def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """

    #get sentences from text
    sentences = tokenize_sentences(text)
    #create trie
    t = Trie()
    #iterate through sentences, spliting each sentence into individual  words
    for sentence in sentences:
        words = sentence.split(" ")
        for word in words:
            #if word is not trie, add word and set freq to 1
            if not t.contains(word):
                t.set(word, 1)
            #if word in trie already, add 1 to frequency
            else:
                val = t.get(word)
                t.set(word, val +1)
              
    return t


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    sentences = tokenize_sentences(text)
    
    t = Trie()
    #iterate through sentences, spliting each sentence into tuples of each word but 
    #viewed as 1 sent
    for sentence in sentences:
        words_tup = tuple(sentence.split(" "))
        #if phrase is not trie, add word and set freq to 1
        if not t.contains(words_tup):
            t.set(words_tup, 1)
        #if phrase in trie already, add 1 to frequency
        else:
            val = t.get(words_tup)
            t.set(words_tup, val +1)


    return t



def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    tries
    """
    #make sure prefix is approaite type (str or tup) and is same as Trie type
    if type(prefix) != tuple and type(prefix) != str:
        raise TypeError
    if type(prefix) != trie.type:
        raise TypeError
    #iterate through Trie's items and check if each the 1st part of key equals prefix
    #if so add (k,v) tuple
    matches = []
    for c in trie.items():
        if prefix == c[0][:len(prefix)]:
            matches.append(c)

    #if max count is Noen, return all matches as a list
    if max_count == None:
        final = []
        for i in matches:
            final.append(i[0])
        return final
    #if there is a max, sort the matches by word frequency and only return top
    #max_count words as a list
    else:
        matches.sort(key=lambda x: x[1], reverse = True)
        count = 0
        final = []
        for i in matches:
            #add words until max_count is reached
            if count < max_count:
                final.append(i[0])
                count +=1
            if count == max_count:
                break
        return final
                



def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    # alpha = ascii.lowercase()

    #alphabet to check for valid edits
    alpha = "abcdefghijklmnopqrstuvwxyz"
    if type(prefix) != tuple and type(prefix) != str:
        raise TypeError
    if type(prefix) != trie.type:
        raise TypeError
  

   
    #call autocomplete to find valid words by simply prefix
    autocomp = autocomplete(trie, prefix, max_count)


    #if max count is None or the number of autocompletes is less tha. max count, 
    #find all valid edits and add top ones until max count is reached
    if max_count == None or len(autocomp) < max_count:

        matches = []
        items = trie.items()
        trie_words = set()
        all_edits = []
        #find all words in trie
        for i in items:
            trie_words.add(i[0])
        #for loop through all items in trie
        for c in trie.items():

            #skip words in autocomplete
            if c[0] in autocomp:
                continue
            word = c[0]

            #if word is greater than size prefix plus two, there is no need to check if it can be edited to 
            #equal the prefix

            if len(word) > len(prefix) +2:
                continue

          
            
            #add valid edits from each type to a list of all edits, if word is deamed a 
            #valid edit, move on to next
            if insertion(word, prefix, alpha, trie_words):

                all_edits.append(c)
                continue


                
            if delete_one(word, prefix, trie_words):
                all_edits.append(c)
                continue
           
                
            if replace(word, prefix, alpha, trie_words):
                all_edits.append(c)
                continue

           
            
            if transpose(word, prefix, trie_words):
                all_edits.append(c)
                continue
    #if max_count exceeded, retrun autocompletes
    else:
        return autocomp

    


    #remoive duplicated edits
    all_eds = set(all_edits)    
    #get list of edits
    for x in all_eds:
        matches.append(x)
       
               
    #return all autocomps and eidts if max is None
    if max_count == None:
            final = []
            for i in matches:
                final.append(i[0])
            return final + autocomp
    #other sort and only add highest frequency edits until max count is reached
    else:
        matches.sort(key=lambda x: x[1], reverse = True)
        count = 0
        max_lim = max_count - len(autocomp) 
        final = []
        for i in matches:
         
            if count < max_count:
                final.append(i[0])
                count +=1
            if count == max_lim:
                break

        return final + autocomp
            




def insertion(word, prefix, alpha, trie_words):
    """
     checks if insertion of letter makes edit valid
    """
   
    #for each index in the prefix plus 1, insert each letter is alphabet and check if makes words == to prefix
    #if so return True


    for i in range(len(prefix)+1):
        for a in alpha:
      
            temp = word[:i] + str(a) + word[i:]
            if prefix == temp:
                if word in trie_words:
                    return True
    return False
     
       

def delete_one(word, prefix,trie_words):
    '''checks if deleltion of letter makes edit valid
    '''
     
     #delete each letter in word and check if makes word = to prefix
    for i in range(len(word)):
            temp = word[:i] + word[i+1:]
            if prefix == temp:
                if word in trie_words:
                    return True
    return False

def replace(word, prefix, alpha,trie_words):
    '''checks if replacenent of any lette makes valid edit
    '''
   
    for i in range(len(word)):
        for a in alpha:
            temp = word[:i] + a + word[i+1:]
            if prefix == temp:
                if word in trie_words:
                    return True

    return False

def transpose(word, prefix, trie_words):
    '''checks if transpsoing 2 letters makes a valid edit
    '''
    edits = []
    for i in range(len(word)):
        for b in range(len(word)):
            #same index, on to next
            if i == b:
                continue
            #find new word by flipping letters at index i and b
            if i >b:
                diff = i -b
                temp = word[:b] + word[i] + word[b+1:b+diff]  + word[b] + word[i+1:]
                if prefix == temp:
                    if word in trie_words:
                        return True
            else:
           
                diff = b - i
                temp = word[:i] + word[b] + word[i+1:i+diff]  + word[i] + word[b+1:]

 
                if prefix == temp:
                    if word in trie_words:
                        return True
    return False




def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """

    #base case if pattern is empty and trie is also nonexistent return []
  
    if len(pattern) == 0 and trie.value == None:
        return []


    def word_filter_recur(trie, pattern):
        '''recursive part of filter word, returns list of (word, freq) for all words in trie that match pattern
        '''
        if len(pattern) == 0 and trie.value == None:
            return []
       
       #base case, after fully recuurisng through all indices in pattern, return list of empty string and trie.value
        if len(pattern) == 0 and trie.value != None:    
            return [('', trie.value)]    
        
        else:
            #otherwise check first element in pattern
            letter = pattern[0]

            #case where letter/symbol in pattern is a "*"
            if letter == '*':
                matches = set()
            
             
                #find all children in trie, and recurisvely call word filter,
                #generate list of (word, freq) for each chiild and add matches for
                #all children's string and other keys in the recursion, add value to tuple

                #mathc all words with that pattern *a*t (match all words cotain a and end in t)
                for c in trie.children: 
                    recurse_children = word_filter(trie.children[c], pattern)
                   
                    for k, v in recurse_children:
                        matches.add((c+k, v))


                #for "*", also recurse until end to pattern ending each longer version of word that matches

                #second case, find longer words that match the pattern (year*, yearning, yearn)
                recurse_to_end = word_filter(trie, pattern[1:])
                for k, v in recurse_to_end:
                    matches.add((k,v))
                
                    
                return list(matches)

            #case where symbol is "?", 
            #find all children in trie, and recurisvely call word filter,
            #generate list of (word, freq) for each chiild and add matches for
            #all children's string and other keys in the recursion, add value to tuple
            #return list of matches
            if letter == '?':
                matches = set()
        
                for c in trie.children:
                    recurse_children = word_filter(trie.children[c], pattern[1:])
                    for k, v in recurse_children:
                        matches.add((c+k, v))
                return list(matches)
         
            # else:

            #case where letter is in an "abc", recursive call to find all matches by using children and 
            #ieratively add all matches
            if letter in trie.children:
                   
                    
                recurse_children = word_filter(trie.children[letter], pattern[1:])
                matches = set()
                for k, v in recurse_children:
                    matches.add((letter + k, v))
                return list(matches)
            #if none of these cases are found True, return empty list to end current recurisve call
            else:
                return list()
   
    return word_filter_recur(trie, pattern)






if __name__ == '__main__':
    pass




# with open("Pride and Prejudice.txt", encoding="utf-8") as f:
#     text = f.read()
# words = make_word_trie(text)
# # print(words)
# # print(autocorrect(words, "tear", max_count=9))
# print(word_filter(words, 'r?c*t'))


# trie = make_word_trie("cats cattle hat car act at chat crate act car act")
# print(autocorrect(trie, 'cat',4))