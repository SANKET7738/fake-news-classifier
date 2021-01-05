from django.shortcuts import render
from .forms import InputForm
from newspaper import Article
from classifier.scrapper import scrape, similarity, google_search, predict
from classifier.models import NewsInfo


# Create your views here.
def index(request):
    return render(request, 'classifier/landingpage.html')


def form(request):
    form = InputForm()
    return render(request, 'classifier/form.html', {'form': form})


def output(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['input_url']
            if not NewsInfo.objects.filter(user_input=url).exists():
                article = Article(url)
                try:
                    article.download()
                except Exception as e:
                    print(e)
                    return render(request, 'classifier/error.html')
                article.parse()
                news_img = article.top_image
                article = article.text
                output, news_title, score = classify(url)
            else:
                print("news already exists")
                values = NewsInfo.objects.fiter(user_input=url)
                print(values)
                error = "Oops"
                return render(request, 'classifier/output.html', {'news_article': error})
            username = request.user.username
            if len(username) == 0:
                username = "Anonymous"
            args = {'output': output, 'news_title': news_title, 'news_article': article, 'score': score, 'news_img': news_img, 'username': username}
            return render(request, 'classifier/output.html', args)
        else:
            print(form.errors())

    else:
        print("error")
        error = "Oops"

    return render(request, 'classifier/output.html', {'url': error})


def classify(url):
    print("step-3")
    news_model = NewsInfo.objects.create()
    test_text, test_title, test_link, test_article = scrape(url)
    news_model.news_title = test_title
    news_model.news_link = test_link
    news_model.news_text = test_text
    search_urls, source_sites = google_search(test_link, test_title)
    sim_score = similarity(search_urls, test_text)
    pred_output = predict(test_text)
    if(pred_output == 1):
        output = "Unreliable"
    else:
        output = "Reliable"
    print(output)
    news_model.output = output
    news_model.save()

    return output, test_title, sim_score
