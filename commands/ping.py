from time import time
from math import ceil


def ping(message, msg):
    text = "🏓 Pong"
    if len(msg) > 1 and msg[1] in ['long', 'exact', 'ex', 'долгий', 'точный', 'точн']:
        results = []
        start = time()
        message.edit(text)
        response_time = ceil((time() - start)*1000)
        results.append(response_time)
        for i in range(29):
            try:
                start = time()
                message.edit(text + f"\n- response in **{response_time}** ms")
                response_time = ceil((time() - start)*1000)
                results.append(response_time)
            except: pass
        message.edit('📊 Average response time:\n**'+str(round(sum(results) / len(results), 2))+' ms**')
    else:
        start = time()
        message.edit(text)
        response_time = ceil((time() - start)*1000)
        message.edit(text + f"\n- response in **{response_time}** ms")