import pandas as pd
import numpy as np
import requests
# 카카오 주소검색 API
"""https://developers.kakao.com/console/app"""
def search_kakao_api(keyword, kakao_key):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(keyword)
    headers = {
        "Authorization": kakao_key
    }
    places = requests.get(url, headers = headers).json()['documents']
    df = pd.DataFrame(places).copy()
    if len(df)==0: # 검색 안되면 패스
        print("Failed!")
        return np.nan
    else:
				df['keyword'] = keyword
        return df

from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen, Request
import json
# 도로명주소 주소검색 API
"""https://www.juso.go.kr/addrlink/devAddrLinkRequestWrite.do?returnFn=write&cntcMenu=URL"""
def search_address_api(keyword, doro_key):
    resulttype= 'json'
    url = 'http://www.juso.go.kr/addrlink/addrLinkApi.do'     
    queryParams = '?' + urlencode({quote_plus('currentPage') : '1' ,
                                   quote_plus('countPerPage') : '10',
                                   quote_plus('resultType') : resulttype,
                                   quote_plus('keyword') : keyword,
                                   quote_plus('confmKey') : api_key})
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    # print(response_body.decode('utf-8'))
    root_json = json.loads(response_body)
    df = pd.DataFrame(root_json['results']['juso'])
    if len(df)==0: # 검색 안되면 패스
        print("Failed!")
        return np.nan
    else:
        df['PNU'] = df['bdMgtSn'].str[:19]
        df['keyword'] = keyword
        return df
