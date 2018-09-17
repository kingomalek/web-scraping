import sys

import pandas as pd

import unidecode


def get_digit(x):
    if isinstance(x, str):
        if x is not None:
            s =''
            for i in x:
                if i.isdigit():
                    s+=i
        return float(s)
    return x

def clean_removeUnicodes(x):
    if isinstance(x, str):
        return unidecode.unidecode(x)
    return x

if len (sys.argv) != 2 :
    print("Error: wrong args numbers ")
    print("python cleaner.py filename")
    sys.exit (1)
print(sys.argv[1])
df = pd.read_json(sys.argv[1], orient='columns')
df.dropna(subset=['titre', 'price','stars','id','country','city'],inplace=True)
df.drop_duplicates(subset=['id'], keep='last',inplace=True)


df['price'] = df['price'].apply(lambda x: get_digit(x))
df['stars'] = df['stars'].apply(lambda x: int(get_digit(x)))
df['review'] = df['review'].apply(lambda x: get_digit(x))/10.

df['titre'] = df.titre.str.lower().str.strip()
df['titre'] = df['titre'].apply(lambda x: clean_removeUnicodes(x))

df['city'] = df.city.str.lower().str.strip()
df['city'] = df['city'].apply(lambda x: clean_removeUnicodes(x))

df['country'] = df.country.str.lower().str.strip()
df['country'] = df['country'].apply(lambda x: clean_removeUnicodes(x))
countries = ['united arab emirates', 'algeria', 'morocco', 'jordan', 'tunisia', 'lebanon']
df = df[df['country'].isin(countries)]

df.to_csv("clean_"+sys.argv[1].split('.')[0]+".csv",index=False)

