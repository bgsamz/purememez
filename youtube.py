#!/usr/bin/python

from urllib.request import urlopen


def youtube_first_result(search):
    """ Given a search (some series of words you'd put into YouTube's search bar), return a URL of
    the first video found. """

    try:
        # turn whitespace splits into +
        query_params = "+".join(search.split())

        # get the search query
        query_url = "https://www.youtube.com/results?search_query={}&page=&utm_source=opensearch".format(query_params)

        # parse it
        response = urlopen(query_url)
        html = str(response.read())

        # look for the relevant blob
        start_string = 'href="/watch?v='
        end_string = '" class='

        # find the indices
        start = html.find(start_string)
        end = html.find(end_string, start)

        # error check
        if start < 0 or end < 0:
            return None

        # return the right thing
        return "https://www.youtube.com/watch?v={}".format(html[start+len(start_string):end])
    except Exception as e:
        print(e)
        return None
