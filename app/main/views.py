from flask import render_template, redirect, url_for,request
from ..requests import get_headline_articles,get_news_sources,search_language_based,get_headline_search,get_all_source_result
import json
from . import main
from . forms import LanguageForm
from ..models import Article



@main.route('/', methods=['GET', 'POST'])
def index():
    """
	View root page function that returns the index page and its data
	"""
    title = "Your one stop news aggregation site"
    form = LanguageForm(request.form)
    category = request.args.get('cat')
    keyword = request.args.get('item_h')
    source_list = get_news_sources()
    if request.method=='POST' and form.validate():
        language_selected = form.language.data
        return redirect(url_for('.lang',lan=language_selected))
    else:
        return render_template('index.html',title=title,select_box = form ,sources=source_list)

@main.route('/headlines/<category>')
def headlines(category):
    """
	View headlines page function that returns the headline page and its data
	"""
    title = "headline"
    form = LanguageForm(request.form)
    headlines = get_headline_articles(category)

    return render_template('headline.html',title=title,headline=headlines,select_box = form)

@main.route('/source/<link>')
def source(link):
    """
    View function to display the news of a particular clicked news source
    """
    link = link.replace(" ","+")
    source = get_all_source_result(link)
    return render_template('sources.html',sources=source)
@main.route('/language/<lan>')
def lang(lan):
    """
    View function to display news based on Language
    """
    title=f'News in {lan}'
    set_language_results = search_language_based(lan,'sources')
    return render_template('language.html',title=title,source_req=set_language_results)

@main.route('/search', methods=['GET', 'POST'])
def search():
    """
    View search function that returns search results
    """
   
    item = request.form.get('item')

    result = []
    source_list = get_headline_search(item)
    if item:
        result_l = get_headline_articles()
        for res in result_l:
            if item in res.title or res.name or res.description:
                result.append(res)

    return render_template('result.html',result=result)