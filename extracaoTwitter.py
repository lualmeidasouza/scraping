#!/usr/bin/env python
# coding: utf-8


#Os produtos que requerem o uso de um Token de Portador são os seguintes:
#API de engajamento
#API de tweets de pesquisa

"""

Você precisará se inscrever para uma conta de desenvolvedor e criar um aplicativo do Twitter. 
Depois de tê-los, você também precisará obter as chaves de API encontradas no portal do desenvolvedor. Siga os passos abaixo:

Faça login na sua conta do Twitter em developer.twitter.com.
Navegue até o painel do Twitter App e abra o Twitter App para o qual você gostaria de gerar tokens de acesso.
Navegue até a página "chaves e tokens".
Você encontrará as chaves de API, os tokens de acesso do usuário e o token do portador nesta página.


"""

import requests
import os
import json


def auth(): 
    # Variavel de ambiente criada anteriormente no seu SO
    return os.environ.get("BEARER_TOKEN")


def create_url():
    
    #A pesquisa que voce deseja fazer no Twitter
    query = "Adenor Tite"
    
    # Tweet fields (Voce pode escolher quais campos consultar)
    # Para saber quais campos podem ser solicitados/consultados, acesse a página da documentação da API e pesquise por "Search Tweets":
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all     
    
    # Opções:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    
    #As expansoes permitem que você solicite objetos de dados adicionais relacionados aos Tweets
    
    #Importante:  versão essencial da API só permite pesquisar até 7 dias retroativos a data atual
    tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,text"
    user_fields = "expansions=author_id&user.fields=id,name,username,created_at"
    filters = "start_time=2023-01-11T00:00:00.00Z&end_time=2023-01-13T00:00:00.00Z"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}".format(
        query, tweet_fields, user_fields, filters
    )
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def paginate(url, headers, next_token=""):
    if next_token:
        full_url = f"{url}&next_token={next_token}"
    else:
        full_url = url
    data = connect_to_endpoint(full_url, headers)
    yield data
    if "next_token" in data.get("meta", {}):
        yield from paginate(url, headers, data['meta']['next_token'])


def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    for json_response in paginate(url, headers):    
        print(json.dumps(json_response, indent=4, sort_keys=True))

        
if __name__ == "__main__":
    main()