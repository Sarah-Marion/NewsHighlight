import urllib.request,json
from .models import Article, Source, News

api_key = None
headlines_url = None
source_url = None
everything_url = None
search_url = None


def configure_request(app):
    global api_key,headlines_url,everything_url,source_url
    api_key = app.config['NEWS_API_KEY']
    headlines_url = app.config['NEWS_HEADLINES_URL']
    source_url = app.config['NEWS_SOURCE_URL']
    everything_url = app.config['NEWS_EVERYTHING_URL']
    search_url = app.config['NEWS_HEADLINES_SEARCH_URL']

def get_headline_articles(category='general'):
    """
	Function that gets the json response to our headlines url request
	"""
    get_headline_url = headlines_url.format(category,api_key)

    with urllib.request.urlopen(get_headline_url) as url:
        get_headlines_data = url.read()
        get_headlines_response = json.loads(get_headlines_data)

        headlines_results = None

        if get_headlines_response['articles']:
            headlines_result_list=get_headlines_response['articles']
            headlines_results = process_headlines(headlines_result_list)

    return headlines_results

def process_headlines(headlines_list):
    """
    	Function  that processes the headlines result and transform them to a list of Objects
    	Args:
        	headlines_list: A list of dictionaries that contain news headlines
    	Returns :
        	headlines_results: A list of news headlines objects
	"""
    headlines_results = []

    for headline in headlines_list or []:
        title = headline.get('title')
        name = headline.get('source.name')
        description = headline.get('description')
        url = headline.get('url')
        urlToImage = headline.get('urlToImage')
        publishedAt = headline.get('publishedAt')
        author = headline.get('author')

        article_object = Article(title,name,url,urlToImage,publishedAt,description,author)
        headlines_results.append(article_object)

    return headlines_results

def get_news_sources(category='',country='',language=''):
    """
    Function that get json response from the api soures endpoint
    """
    get_sources_url = source_url.format(category,country,language,api_key)
    with urllib.request.urlopen(get_sources_url) as url:
        get_sources_data = url.read()
        get_sources_response = json.loads(get_sources_data)

        sources_results = None

        if get_sources_response['sources']:
            sources_result_list = get_sources_response['sources']
            sources_results = process_sources(sources_result_list)

    return sources_results

def process_sources(sources_list):
    """
    Function that processes the sources result and transform them to a list of Objects
    Args:
        sources_list: A list of dictionaries that contains sources
    Returns:
        sources_results: A list of news sources Objects
    """
    sources_results = []
    for source in sources_list or []:
        name = source.get('name')
        description = source.get('description')
        category  = source.get('category')
        url = source.get('url')
        country = source.get('country')
        language = source.get('language')

        source_object = Source(name,description,category,url,country,language)
        sources_results.append(source_object)
    return sources_results

def search_language_based(language,code):

    item_list= []
    if code=='sources':
        items_req = get_news_sources()
        for item in items_req:
            if item.country == language:
                item_list.append(item)
        return item_list
    elif code=='headline':
        items_req = get_headline_search(language)
        for item in items_req:
            if language in item.get('title') or item.get('source.name'):
                item_list.append(item)
        return item_list
    elif code=='source':
        items_req = get_news_sources()
        for item in items_req:
            if item.category == language:
                item_list.append(item)

    else:
        item_list = get_news_sources()

    return item_list

def get_headline_search(query):
    """
    Function that returns news  from a particular headline
    """
    query = query.replace(' ',"")
    category=""
    get_headline_url = 'https://newsapi.org/v2/top-headlines?category={}&query={}&language=en&apiKey={}'.format(category,query,api_key)
    headlines_results = []
    with urllib.request.urlopen(get_headline_url) as url:
        get_headlines_data = url.read()
        get_headlines_response = json.loads(get_headlines_data)
        if get_headlines_response['articles']:
            headlines_result_list=get_headlines_response['articles']
            for headline in headlines_result_list:
                headlines_results.append(headline)
    return headlines_results

def get_all_source_result(source):
    """
    Function that returns all news from a particular source
    """
    get_sources_url = everything_url.format(source,api_key)
    with urllib.request.urlopen(get_sources_url) as url:
        get_sources_data = url.read()
        get_sources_response = json.loads(get_sources_data)

        news_results = None
        if get_sources_response['articles']:
            sources_result_list = get_sources_response['articles']
            news_results = process_news(sources_result_list)
    return news_results
def process_news(news_list):
    news_results = []
    for news in news_list:
        name = news.get('name')
        description =news.get('description')
        url = news.get('url')

        news_object = News(name,description,url)
        news_results.append(news_object)
    return news_results