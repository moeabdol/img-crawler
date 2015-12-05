# img-crawler
Simple Python 2 script to crawl a webpage and download images.

## Dependencies
* [requests](http://docs.python-requests.org/en/latest/)
* [urlparse](https://docs.python.org/2/library/urlparse.html)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

## How to use
Make sure depindencies are installed then:<br>
```
$ python img-crawler
```

### Specify site to crawl
To define a custom site you want to crawl change the following in the
script (line 79):<br>
```python
if __name__ == "__main__":
    root = "http://moeabdol.com"  # change to site you want to crawl
```

### Specify maximum links to crawl
To specify the number of links you want to crawl, change the following in the
script (line 24):<br>
```python
def traverse_site(max_links=10):  # change max_links
```
