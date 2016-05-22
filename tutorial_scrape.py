#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from ipdb import set_trace
from os import path, makedirs
from selenium import webdriver
import youtube_dl
# from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("TutorialThatIWasGoingToScrape")
assert "SiteTitle" in driver.title
driver.find_element_by_id('signInLink').click()
driver.find_element_by_id('userHandle').send_keys('username')
driver.find_element_by_id('password').send_keys('password')
driver.find_element_by_id('submit').click()
driver.get("CourseURL")

# BeatifulSoup Filters
parsed_html = BeautifulSoup(driver.page_source.encode('utf-8'))
title = parsed_html.find('title').string
divFilter = parsed_html.body.find('div', attrs={'class': 'section-container accordion'})
tableContentsFilter = divFilter.findAll('a', attrs={'class': 'ng-binding'})
timefilter = divFilter.findAll('span', attrs={'class': 'list-item module toc-time number ng-binding'})
block = divFilter.findAll('div', attrs={'class': 'section ng-scope'})

main_contents = []  # holds main listings; the folder names
inner_contents = []  # holds sub contents
check = []

for m_counter, (contents, duration, bs_innercontent) in enumerate(zip(tableContentsFilter, timefilter, block)):
    main_contents.append("%02d" % m_counter + '_' + contents.string.replace(" ", "_") + '_' + duration.string)
    subheadings = bs_innercontent.findAll('h5', attrs={'class': 'ng-binding'})
    check.append(False)

    inner = []
    for sub_counter, subheading in enumerate(subheadings):
        inner.append("%02d" % sub_counter + '_' + subheading.string.replace(" ", "_"))
        check.append(True)

    inner_contents.append(inner)

if not path.exists(title):
    makedirs(title)

for heading in main_contents:
    if not path.exists(title + '/' + heading):
        makedirs(title + '/' + heading)

directory_listing = list(check)

for cnt, ch in enumerate(check):
    if not ch:
        directory_listing[cnt] = main_contents[cnt]


def youtube(url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(ext)s'})

    with ydl:
        result = ydl.download(url)
        return result

div_select = driver.find_elements_by_css_selector(
    """html#ng-app.js.no-touch.svg.inlinesvg.svgclippaths.no-ie8compat.ng-scope \
    body div.ng-scope div.ng-scope section.band div.row div.large-8.columns \
    div.ng-scope section#table-of-contents.ng-scope div.row \
    div.small-12.columns div.section-container.accordion""")

filter2 = div_select[0].find_elements_by_css_selector('a')

for c, link in zip(check, filter2):
    if not c:
        link.click()
    else:
        link.click()
        driver.switch_to_window(driver.window_handles[1])
        player_html = BeautifulSoup(driver.page_source.encode('utf-8'))
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        video = player_html.find('video', attrs={'id': 'video'}).get("src")
        youtube(video)
        set_trace()


# Todo:
# scrape second window for mp4
# scrape for video lengths, description
