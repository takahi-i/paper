# -*- coding: utf-8 -*-

import os
import re
import requests
from pyquery import PyQuery


class Librarian:

    __SCHOLAR_URL = "https://scholar.google.com/scholar?q="
    __GS_A_REGEXP = re.compile(r'(.+?)(?:&#8230;)? - .+?, (.+?) - .+?')

    def search(self, keywords):
        pq_html = PyQuery(self.__SCHOLAR_URL + ' '.join(keywords))
        papers = self._extract_papers_from(pq_html)
        return papers

    def _extract_papers_from(self, pq_html):
        papers = []
        for div in pq_html.find('div.gs_r.gs_or.gs_scl'):
            pq_div = PyQuery(div)
            paper = self._extract_paper_from(pq_div)
            papers.append(paper)
        return papers

    def _extract_paper_from(self, pq_div):
        paper = {'url': '', 'title': '', 'authors': [], 'year': 0}
        paper['url'] = pq_div.find('div.gs_ggs.gs_fl a').attr('href')
        paper['title'] = pq_div.find('div.gs_ri h3').text()
        match = re.search(self.__GS_A_REGEXP, pq_div.find('.gs_a').html())
        if not match:
            return paper
        for author in match.group(1).split(', '):
            paper['authors'].append(re.sub(r'<a.+?>|</a>', '', author))
        paper['year'] = match.group(2)
        return paper

    def get_user_input(self, papers):
        user_input = input('Paper to download [0-9]: ')
        while self._is_valid_input(user_input, papers):
            user_input = input('Paper to download [0-9]: ')
        return int(user_input)

    def _is_valid_input(self, user_input, papers):
        if re.match(r'[0-9]', user_input) is None:
            return 0
        elif papers[int(user_input)]['url'] is None:
            return 0
        else:
            return 1

    def save(self, paper):
        response = requests.get(paper['url'])
        if response.status_code != 200:
            return

        if not os.path.isdir('~/.paper/pdf'):
            os.makedirs('~/.paper/pdf')

        last_name = paper['authors'][0].split(' ')[1]
        file_name = last_name + paper['year'] + '.pdf'
        with open('~/.paper/pdf/' + file_name, 'wb') as pdf_file:
            pdf_file.write(response.content)
