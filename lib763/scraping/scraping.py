import requests


def get_html(url: str) -> tuple:
    """
    @param:
        url : str 対象のurl
    @return:
        tuple( htmlの文字列、エンコーディング)
    htmlテキストとエンコーディングを取得する
    """
    response = requests.get(url)
    return response.text, response.encoding


def get_tag_strings(html_str: str, tag: str) -> list:
    """
    @param:
        html_str str htmlテキスト
        tag str 検索するタグ
    @return:
        list 引っかかった文字列
    指定したタグに囲まれている文字列を返す。
    (例；<div>aaaa</div>のaaaaを取得する、ただしtag = 'div')
    """
    html = html_str.replace(" ", "")
    result = []
    start_index = 0
    while True:
        start_index = html.find("<" + tag, start_index)
        if start_index == -1:
            break
        end_index = html.find("</" + tag + ">", start_index)
        result.append(html[start_index : end_index + len("</" + tag + ">")])
        start_index = end_index + len("</" + tag + ">")
    return result


def get_enclosed_strings(sentence: str) -> list:
    """
    @param:
        sentence str  htmlテキスト
    @return:
        list 引っかかった文字列
    >aaa<となっている場合、aaaを返す。
    """
    result = []
    start = 0
    while True:
        start = sentence.find(">", start)
        if start == -1:
            break
        end = sentence.find("<", start + 1)
        if end == -1:
            break
        enclosed_str = sentence[start + 1 : end]
        if len(enclosed_str) != 0:
            result.append(enclosed_str)
        start = end + 1
    return result
