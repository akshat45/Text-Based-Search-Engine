import numpy as np
import operator
from numpy import linalg as la

file = open("words.txt",'r')
dataset = file.read()
tokens=dataset.split(',')

tracks= open("tracks.txt",'r')
trackset=tracks.read()
trackset=trackset.split()

num_of_tracks= len(trackset)
top_songs={}
for i in range(0,210519):
    top_songs[i]=0

total_words_in_a_doc=[]
main_dict={}
for i in range(0,5001):
    main_dict[i]={}


track_name=[]
sum1=0
for j in range(0,210519):
    doc= trackset[j].split(',')
    docsize= len(doc)
    sum=0
    track_name.append(doc[0])
    for i in range(2,docsize):
        splitdoc=doc[i].split(':')
        word_id=int(splitdoc[0])
        count=int(splitdoc[1])
        sum+=count
        main_dict[word_id][j]=count
    sum1+=sum
    total_words_in_a_doc.append(sum)

def get_track_name(id):
        return track_name[id]
def get_songs_based_on_query(track):
    for x,y in track.items():
        print(get_track_name(x))
def get_top_songs(track):
    for (x,y) in track:
        print(get_track_name(x))

def get_songs_given_query():
    str= input("Enter Song Query ")
    str = str.split()
    query_size=len(str)
    query=[]
    store={}
    flag=0
    for i in range(0,query_size):
        if str[i] in dataset:
            flag=1
            if str[i] in store:
                store[str[i]]+=1
            else:
                store[str[i]]=1
    if flag==0:
        print("sorry!No songs found")
    else:
        query_list=[]        
        for x,y in store.items():
            query.append(x)
            query_list.append(y)
        query_size=len(query)
        
        vector_list=np.zeros( (210519, query_size) )
        count=0
        

        for qword in query:
            qword_id=tokens.index(qword)+1
            num_of_docs_having_qword=len(main_dict[qword_id])
            
            idf=np.log(210519/(num_of_docs_having_qword+1))
            
            for doc_id in main_dict[qword_id]:
                tf_for_a_doc=main_dict[qword_id][doc_id]/total_words_in_a_doc[doc_id]
                #tf_idf_for_docs_having_qword[doc_id]=(tf_for_a_doc*idf)
                vector_list[doc_id][count]=(tf_for_a_doc*idf)
            count+=1
                
        query_list=np.array(query_list)
        
        final_dict={}
        for i in range(0,210519):
            temp=la.norm(vector_list[i])*la.norm(query_list)
            if(temp==0):
                temp=1
            final_dict[i]=np.dot(vector_list[i], query_list)/temp
        
        sorted_final_dict = sorted(final_dict.items(),key=operator.itemgetter(1),reverse=True)
        final_ans=sorted_final_dict[0:10]
        final_ans=dict(final_ans)

        global top_songs
        top_songs=dict(top_songs)
        for i,j in final_ans.items():
            top_songs[i]+=1
        top_songs=sorted(top_songs.items(),key=operator.itemgetter(1),reverse=True)
        
        print("Here are the top 10 songs according to the query")
        get_songs_based_on_query(final_ans)
        print("\n\n\n\n")
        
    print("Here are the top 10 searches by the users")
    get_top_songs(top_songs[0:10])

get_songs_given_query()
