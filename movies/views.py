# airtable.com
# Python Airtable wrapper - https://github.com/gtalarico/airtable-python-wrapper
# Sourcelair.com

from django.shortcuts import render, redirect
from airtable import Airtable
import urllib
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query + "', {Name})")

    stuff_for_frontend = {"search_result": search_result}
    return render(request, "movies/movies_stuff.html", stuff_for_frontend)


def create(request):
    if( request.method == "POST"):
        data = {
          "Name": request.POST.get("name"),
          "Pictures": [
            {
              "url": request.POST.get("url")
            }
          ],
          "Rating": int(request.POST.get("rating")),
          "Notes": request.POST.get("notes")
        }

        try:
            insert = AT.insert(data)
        except:
            return render(request, "movies/error.html")
        return redirect("/")

    return render(request, "movies/error.html")

def delete(request, id):
    try:
        AT.delete(id)
    except:
        pass
    return redirect("/")
