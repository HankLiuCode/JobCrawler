import crawler104Core
    




if __name__ == '__main__':
    
    url1 = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}&indcat=1004002000'
    url2 = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}&jobcat=2007002000'
    url3= 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}&jobcat=2017000000'
    urls = [url3]
    cc = Crawler104Core()

    #test startCrawl
    """
    cc.startCrawl(urls)
    df = pandas.DataFrame(cc.getResult())
    df.to_excel('test.xlsx')
    """

    #traverseParamTree tests
    """
    param_list = []
    cc.traverseParamTree(param_list, url3, 'jobcat', '2017000000')
    print(param_list)
    """
    #sieveUrlWithParam tests
    """
    for url in urls:
        url_infos = [(url, cc.getTotal(url)['totalCount'], False)]
        url_info_list = cc.sieveUrlWithParam(url_infos,'jobcat')
        print(url_info_list)
        print(len(url_info_list))
    """
