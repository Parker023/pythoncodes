name="Aannirrudh"

#reverse a string


print(name[::-1])

#palindrome

print(name[::-1]==name)

#count vowels and consonants

vowels="aeiou"

vcnt=0
ccnt=0

for i in name:
    if i in vowels:
        vcnt=vcnt+1
    else:
        ccnt=ccnt+1


print(f"Vowels:{vcnt} Consonants:{ccnt}")



#count occurrence of each character

char_count={}

for i in name:
    if i in char_count:
        char_count[i]=char_count[i]+1
    else:
        char_count[i]=1

print(char_count)

# remove duplicates

uniq_list=[]

set_name=set()

for i in name:
    if i not in set_name:
        set_name.add(i)
        uniq_list.append(i)

print(uniq_list)


#convert String to upper without using upper() function

# assuming all characters are lower case

lower_name=name.lower()
upper_name=""

for i in lower_name:
    upper_name=upper_name+ chr(ord(i)-32)

print(f"upper_name: {upper_name}")


#first non-repeated character case-insensitive

char_freq={}

case_sensitive_name=name.lower()

for i in case_sensitive_name:
    if i in char_freq:
        char_freq[i]=char_freq[i]+1
    else:
        char_freq[i]=1



for entry in char_freq:
   if char_freq[entry]==1:
        print(entry)
        break

#Most repeated character case-insensitive

max_freq=0

maxfreq_char=""

for entry in char_freq:
   if char_freq[entry]>max_freq:
       print(entry)
       max_freq=char_freq[entry]
       maxfreq_char=entry

print(f"Most repeated character: {maxfreq_char} with frequency: {max_freq}")


#anagram

s1="listen"
s2="silent"

st_set=set(s1)

anagram=True
if len(s1)==len(s2):
    for i in s2:
        if i not in st_set:
            anagram=False
            break
        else:
            st_set.remove(i)
else:
    anagram=False

if anagram:
    print(f"{s1} and {s2} are anagram")
else:
    print(f"{s1} and {s2} are not anagram")


#count digits, alphabets and special characters

dig_cnt=0
alph_cnt=0
spec_cnt=0

for i in name:
    if i.isdigit():
        dig_cnt=dig_cnt+1
    elif i.isalpha():
        alph_cnt=alph_cnt+1
    else:
        spec_cnt=spec_cnt+1

print(f"Digits:{dig_cnt} Alphabets:{alph_cnt} Special characters:{spec_cnt}")


#reverse each word in a string

sentence="There is a rainbow in the sky"

reversed_sentence=""

for word in sentence.split():
    reversed_sentence=reversed_sentence+word[::-1]+" "

print(f"Reversed sentence: {reversed_sentence.rstrip()}")



#find longest word in a string

max_len=0
max_word=""
for word in sentence.split():
    if len(word)>max_len:
        max_len=len(word)
        max_word=word
print(f"Longest word: {max_word} with length: {max_len}")


# count the frequency of each word in a string

word_dict={}
for word in sentence.split():
    if word in word_dict:
        word_dict[word]=word_dict[word]+1
    else:
        word_dict[word]=1

for word in word_dict:
    print(f"{word} occurs {word_dict[word]} times")