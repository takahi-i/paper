#!/usr/bin/env python


import unittest
from paper.librarian import Librarian
from pyquery import PyQuery


class TestSearch(unittest.TestCase):

    def test_extract_papers_from(self):
        html = """
        <html>
          <div class="gs_r gs_or gs_scl">
            <div class="gs_ggs gs_fl">
              <a href="paper_url"></a>
            </div>
            <div class="gs_ri">
              <h3>title</h3>
              <div class="gs_a">author - conference, year - site_url</div>
            </div>
          </div>
        </html>
        """
        pq_html = PyQuery(html)
        papers = Librarian()._extract_papers_from(pq_html)
        assert papers == [
            {
                'url': 'paper_url',
                'title': 'title',
                'authors': ['author'],
                'year': 'year',
            }
        ]


if __name__ == "__main__":
    unittest.main()
