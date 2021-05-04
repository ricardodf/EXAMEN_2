import json
import http.client

conn = http.client.HTTPSConnection('e2-is714522-nlu.mybluemix.net')
headers = {'Content-type': 'application/json'}

def lambda_handler(event, context):
    foo = {
        "text": event["historial_clinico"],
        "features": {
            "keywords": {
                "sentiment": True,
                "emotion": True,
                "limit": 5
            },
            "entities": {
                "metions": True,
                "model": True,
                "sentiment": True,
                "emotion": True,
                "limit": 5
            }
        }
    }
    json_data = json.dumps(foo)
    
    conn.request('POST', '/api/analyze', json_data, headers)
    
    response = conn.getresponse()
    jsonData = json.loads(response.read().decode("utf-8"))
    
    # FOR para KEYWORDS
    keywordsArr = list()
    keywordsDetail = list()
    for keyword in jsonData["keywords"]:
        keywordsArr.append(keyword["text"])
        keywordsDetail.append({
            keyword["text"]: {
                "sentimiento": keyword["sentiment"]["label"],
                "relevancia": keyword["relevance"],
                "repeticiones": keyword["count"],
                "emocion": sorted(keyword["emotion"], key=lambda emt: emt[1], reverse=True)[0]
            }
        })
    
    # FOR para ENTITIES
    entitiesArr = list()
    entitiesDetail = list()
    for entity in jsonData["entities"]:
        entitiesArr.append(entity["text"])
        entitiesDetail.append({
            entity["text"]: {
                "tipo": entity["type"],
                "sentimiento": entity["sentiment"]["label"],
                "relevancia": entity["relevance"],
                "emocion": sorted(entity["emotion"], key=lambda emt: emt[1], reverse=True)[0],
                "repeticiones": entity["count"],
                "porcentaje_confianza": entity["confidence"]
            }
        })
    
        
    return {
        "language": jsonData["language"],
        "palabras_clave": keywordsArr,
        "entidades": entitiesArr,
        "palabras_clave_desc": keywordsDetail,
        "entidades_desc": entitiesDetail
    }
