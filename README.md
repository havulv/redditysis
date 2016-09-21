redditysis
==========

Reddit site scraping and analysis

Considerations
--------------

I considered using the API, which would honestly still be preferable, but it was too powerful for my use case. Instead, redditysis just scrapes a single grouping of pages on a scheduler and then stores the results into a file. Included are some useful tools for analyzing the data.
As well, each of the queries are run as seperate processes that block until all are completed.

Usage
-----

To run on a schedule:

```
  >python schedule.py
```

To run once:

```
  python web_scrape.mp_scrape.py http://www.reddit.com/r/{subreddit1} http://www.reddit.com/r/{subreddit2} ...
```

To Do
------

* Allow for user choice in which subreddits to scrape
* Update the tools so that they easily notify the user when there is a statistically significant occurence
* Organize the data so that it takes up less data (pickling or compressing the file) and is easier to manipulate
* Clarify what each of the tools is used for and how they are implemented on the scraped data set
* Add option to set wait times
