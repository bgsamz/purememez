#!/usr/bin/python

import urllib2


def youtube_first_result(search):
    """ Given a search (some series of words you'd put into YouTube's search bar), return a URL of
    the first video found. """

    try:
        # turn whitespace splits into +
        query_params = "+".join(search.split())

        # get the search query
        query_url = "https://www.youtube.com/results?search_query={}&page=&utm_source=opensearch".format(query_params)

        # parse it
        response = urllib2.urlopen(query_url)
        html = response.read()

        # look for the relevant blob
        start_string = 'href="/watch?v='
        end_string = '" class='

        # find the indices
        start = html.find(start_string)
        end = html.find(end_string)

        # error check
        if start < 0 or end < 0:
            return None

        # return the right thing
        return "https://www.youtube.com/watch?v={}".format(html[start+len(start_string):end])
    except Exception as e:
        # any kind of issue, just return None
        return None
