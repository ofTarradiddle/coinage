import pandas as pd 

#context
#also have text q&a, image gen, text transfer style, flavordb, 

# you need to install Biopython:
# pip install biopython

# Full discussion:
# https://marcobonzanini.wordpress.com/2015/01/12/searching-pubmed-with-python/

#this will pull article infor, including abstract for a query term
from Bio import Entrez
import pandas as pd
from io import StringIO
import json
import argparse

def search(query):
    Entrez.email = 'your.email@example.com'
    #can I sort by relevance and then take some top percentile
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='1000',
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

def process(ppr):
    """
    Given a paper index of papers, return pandas dataframe for each  """
    file = json.dumps(ppr, indent=2, separators=(',', ':'))

    input_dict = json.loads(file)
    try:
        abs = [x for x in input_dict["MedlineCitation"]["Article"]["Abstract"]["AbstractText"] ]
        #abstract in article row index
        #df = pd.read_json(StringIO(file))
        df = abs
    except:
        df = None 

    return df

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   


    return str1 


#images

#other

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if False:
    #install('transformers')
    import torch
    from transformers import pipeline

    summarizer = pipeline("summarization")
    summarizer("An apple a day, keeps the doctor away", min_length=5, max_length=20)

    #summary
    #install('sentencepiece')

    #from transformers import pipeline

    # using pipeline API for summarization task
    summarization = pipeline("summarization")

    original_text = """
    Paul Walker is hardly the first actor to die during a production. 
    But Walker's death in November 2013 at the age of 40 after a car crash was especially eerie given his rise to fame in the "Fast and Furious" film franchise. 
    The release of "Furious 7" on Friday offers the opportunity for fans to remember -- and possibly grieve again -- the man that so many have praised as one of the nicest guys in Hollywood. 
    "He was a person of humility, integrity, and compassion," military veteran Kyle Upham said in an email to CNN. 
    Walker secretly paid for the engagement ring Upham shopped for with his bride. 
    "We didn't know him personally but this was apparent in the short time we spent with him. 
    I know that we will never forget him and he will always be someone very special to us," said Upham. 
    The actor was on break from filming "Furious 7" at the time of the fiery accident, which also claimed the life of the car's driver, Roger Rodas. 
    Producers said early on that they would not kill off Walker's character, Brian O'Connor, a former cop turned road racer. Instead, the script was rewritten and special effects were used to finish scenes, with Walker's brothers, Cody and Caleb, serving as body doubles. 
    There are scenes that will resonate with the audience -- including the ending, in which the filmmakers figured out a touching way to pay tribute to Walker while "retiring" his character. At the premiere Wednesday night in Hollywood, Walker's co-star and close friend Vin Diesel gave a tearful speech before the screening, saying "This movie is more than a movie." "You'll feel it when you see it," Diesel said. "There's something emotional that happens to you, where you walk out of this movie and you appreciate everyone you love because you just never know when the last day is you're gonna see them." There have been multiple tributes to Walker leading up to the release. Diesel revealed in an interview with the "Today" show that he had named his newborn daughter after Walker. 
    Social media has also been paying homage to the late actor. A week after Walker's death, about 5,000 people attended an outdoor memorial to him in Los Angeles. Most had never met him. Marcus Coleman told CNN he spent almost $1,000 to truck in a banner from Bakersfield for people to sign at the memorial. "It's like losing a friend or a really close family member ... even though he is an actor and we never really met face to face," Coleman said. "Sitting there, bringing his movies into your house or watching on TV, it's like getting to know somebody. It really, really hurts." Walker's younger brother Cody told People magazine that he was initially nervous about how "Furious 7" would turn out, but he is happy with the film. "It's bittersweet, but I think Paul would be proud," he said. CNN's Paul Vercammen contributed to this report.
    """
    summary_text = summarization(original_text)[0]['summary_text']
    print("Summary:", summary_text)

if __name__ == '__main__':
    sys.argv = ['']
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query",default = "lycopene muscle", type = str) 
    parser.add_argument("-p","--path",default = "text.csv", type = str)
    args = parser.parse_args()

    results = search(query = args.query)
    id_list = results['IdList']
    papers = fetch_details(id_list)
    pd_df = pd.DataFrame()
    pd_str = ""
    for i, paper in enumerate(papers['PubmedArticle']):
       df = pd.Series(process(ppr = papers['PubmedArticle'][i]))

       if len(df) > 0:
        #df['id'] = str(i)
        pd_df = pd.concat([pd_df, df], axis = 0).drop_duplicates()
        pd_str = pd_str + df[0] + """



        """
        #pd_df.iloc[1][0]
        pd_df.to_csv(args.path)
        from datetime import date
        (pd_str).to_csv("2021-12-01-lycopene.csv")
        listToString(pd_df[0])
        

        #print(pd_df.drop_duplicates())
        #or save to some location for use, or post to app
