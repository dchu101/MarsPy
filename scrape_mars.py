def scrape():

# Import dependencies

    from bs4 import BeautifulSoup as soup
    from splinter import Browser
    import pandas as pd
    import aux_func as aux

    # initialize splinter browser
    browser = Browser('chrome', 
                    **{"executable_path": "/usr/local/bin/chromedriver"}, 
                    headless=False)

# Scrape NASA Mars site for headlines, dates, and content preview

    url = 'https://mars.nasa.gov/news/'
    webpage = aux.getParsedWebpage(browser, url)

    # Scrapes most recent headlines, date, and text in order
    headlines_grouped = soup.find_all(webpage, 'h3', class_=None)
    dates_grouped = soup.find_all(webpage, 'div', class_='list_date')
    text_grouped = soup.find_all(webpage, 'div', class_='article_teaser_body')

    # Iterates and generates list of all items
    zip_headlines = list(zip(aux.getParsedTextList(headlines_grouped),
                                aux.getParsedTextList(dates_grouped),
                                aux.getParsedTextList(text_grouped)))

    # Generate Dataframe from raw data
    headline_df = pd.DataFrame(zip_headlines)
    headline_df.rename(columns={0:'headline', 
                                1:'date', 
                                2:'text'}, 
                    inplace=True)
    headline_df

# Scrape JPL Mars website for most recent image
# For some reason this pulls an image of Neptune

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    webpage = aux.getParsedWebpage(browser, url)

    # Get title and description

    featured_title = soup.find(webpage, 'h1', class_='media_feature_title').get_text()
    featured_description = soup.find(webpage, 'a', class_='button fancybox').get('data-description')

    # 
    featured_url = soup.find(webpage, 'a', class_='button fancybox').get('data-fancybox-href')

    featured_url=f'https://www.jpl.nasa.gov{featured_url}'

    print(featured_title)
    print(featured_description)
    print(featured_url)

#Mars Twitter Parse

    #Hardcoded a single tweet for now for testing (not all tweets are weather reports, causes errors)
    url = 'https://twitter.com/MarsWxReport/status/1038219633726316544'
    webpage = aux.getParsedWebpage(browser, url)

    #std_tweet_class = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'
    std_tweet_class = 'TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text'

    # pull text of most recent tweet about the weather
    mars_weather = soup.find_all(webpage, 'p', class_= std_tweet_class)[0].get_text()

    # create split string to pull apart and add to dataframe
    mars_weather_split = recent_weather.split(',')

    # create dictionary to turn into a dataframe
    weather_dict = {'mars_date':f'{mars_weather.split("(")[0]}',
                    'earth_date':f'{mars_weather.split("(")[1].split(")")[0]}',
                    'temp_high':f'{mars_weather_split[1].split(" ")[2]}',
                    'temp_low':f'{mars_weather_split[2].split(" ")[2]}',
                    'pressure':f'{mars_weather_split[3].split(" ")[3]}',
                    'daylight':f'{mars_weather_split[4].split(" ")[2]}'}
    weather_df = pd.DataFrame.from_dict(weather_dict, orient='index')
    weather_df = weather_df.rename(columns={0:'Most Recent Weather on Mars'})
    weather_df

# Mars Facts

    url = 'https://space-facts.com/mars/'
    webpage = aux.getParsedWebpage(browser, url)

    # dictionary to hold facts
    facts_dict = {}

    # get rows in facts table, parse into dictionary
    facts_all = soup.find(webpage, 
                        'table', 
                        class_='tablepress tablepress-id-mars').find_all('tr')
    for fact in facts_all:
        facts_dict[soup.find(fact, 'strong').get_text()] = (soup.find(fact, class_='column-2').get_text())

    # convert fact_dict to DF and HTML
    facts_df = pd.DataFrame.from_dict(facts_dict, orient='index')
    facts_df.rename(columns={0:'Facts about Mars'}, inplace=True)
    facts_html = pd.DataFrame.to_html(facts_df)

    facts_df

# Mars Hemispheres

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    webpage = aux.getParsedWebpage(browser, url)

    base_url = 'https://astrogeology.usgs.gov/'

    # get all unique links to photo pages
    page_links_list = []
    page_links = soup.find_all(webpage, 'a', class_='itemLink product-item')
    [page_links_list.append(page.get('href')) for page in page_links]
    page_links_list = list(set(page_links_list))

    image_list = []

    # iterate through links and pull image URLs
    for link in page_links_list:
        url = f'https://astrogeology.usgs.gov{link}'
        webpage = aux.getParsedWebpage(browser, url)
        
        # get image title
        title = soup.find(webpage, 'h2', class_='title').get_text()
        
        # get full size image link
        downloads_section = soup.find(webpage, 'div', class_='downloads')
        image_link = soup.find(downloads_section, 'a').get('href')
        
        # add title and full-size image url to dict
        image_list.append({'title':title,
                        'image_url':image_link})

    # create DF
    image_df = pd.DataFrame(image_list, columns=['title', 'image_url'])
    image_df

# Return dictionary

    scrape_dict = {'headlines':zipped_headlines,
                   'featured_img_url':featured_url,
                    'weather':weather_html, 
                    'facts':fact_html, 
                    'image_urls':image_list}
    
    return scrape_results_dict;
