import sys
from tkinter import TOP
import numpy as np


sys.path.append("..")
from config import TOP_K, DEFAULT_TABLE
from logs import LOGGER

def L2(v1,v2):
    return sum((v1[i]-v2[i])**2 for i in range(len(v1)))

def score(vectors1,vectors2):
    print("v1",vectors1)
    print("v2",vectors2)
    distances=[[L2(vectors1[i],vectors2[j]) for i in range(len(vectors1))] for j in range(len(vectors2))]

    score=0
    for i in range(len(vectors1)):
        for j in range(len(vectors2)):
            if distances[j][i]<0.3:
                score+=1/(distances[j][i]+1)
    return score

def search_in_milvus(user,milvus_cli, mysql_cli):
    LOGGER.info("ici_1.1")

    try:
        #get user ids
        user_ids=mysql_cli.user_ids(user)
        print("user_ids",user_ids)
        if len(user_ids)==0:
            return []

        #get nearest users


        user_vectors=[]
        for id in user_ids:
            user_vectors.append(milvus_cli.id_vectors([id])[0])



        ids=set(milvus_cli.nearest_ids(user_vectors,TOP_K))
        nearest_users=set()
        for id in ids:
            nearest_users.add(mysql_cli.id2user(id))
        nearest_users=list(nearest_users)
        users_ids=[]
        for user in nearest_users:
            #get user vectors
            users_ids.append(mysql_cli.user_ids(user))
        users_vectors=[]
        for user_ids in users_ids:
            users_vectors.append([])
            for id in user_ids:
                users_vectors[-1].append(milvus_cli.id_vectors([id])[0])


        dists=[[nearest_users[i], score(user_vectors,vectors)] for i ,vectors in enumerate(users_vectors)]
        dists.sort(key=lambda x:-x[1])
        result=[]
        for dis in dists[:50]:
            result.append({"user":dis[0],"score":dis[1]})
        #get nearest users of these vectors
        #get vector of these users
        return result
    except Exception as e:
        LOGGER.error(f" Error with search : {e}")
        sys.exit(1)


def query_search(query,model, milvus_cli, mysql_cli):
    LOGGER.info("AAAAAAAAAAAAAA")
    
    embedding=model.sentence_encode([query])[0]
    try:
        ids=milvus_cli.vector_nearest_ids(embedding,TOP_K)
        result=[]
        for id in ids:
            print("ID",id)
            user,todo=mysql_cli.id2infos(id)
            result.append({'id':str(id),'user':user,'todo':todo})


        return result
    except Exception as e:
        LOGGER.error(f" Error with search : {e}")
        sys.exit(1)
