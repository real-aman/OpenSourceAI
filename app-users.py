import openai
from urllib.request import urlopen
from bs4 import BeautifulSoup
import googleSerp as gs
import html2text
import requests
import json
import streamlit as st
openai.api_key = "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"
openai.organization = "org-tJQ0iXbGIKtxFBzgRfxk7GMh"


def SearchTheWeb(query):
    print("Searching the web...")
    url = gs.GetTop1GoogleResults(query)
    print("URL Found: " + url)
    print("Opening URL...")
    html = urlopen(url).read()
    print("Pasrsing Content...")
    soup = BeautifulSoup(html, features="html.parser")
    extractedText = soup.get_text()
    print("Extract Text...")
    h = html2text.HTML2Text()
    h.ignore_links = True
    blogPost = h.handle(extractedText)
    print("Generating Summary...")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "user", "content": """In the following input, I am going to give you a text you
             should summarize for me. I will give you a maximum and a minimum
             amount of words you should use for the text. I am also going
             to give you the text itself after that. The language
             of the text you get should define in which language
             you write the summary. For Example, if the text is German
             the summary should be in German too. This goes for every language.
             While writing the summary I want you to remember the following information:
             When it comes to writing content, two factors are crucial,'perplexity' and 'burstiness'
             ,Perplexity measures the complexity of text. Separately, burstiness compares
             the variations of sentences. Humans tend to write with great burstiness,
             for example, with some longer or complex sentences alongside shorter sentences.
             AI sentences tend to be more uniform. Therefore, when writing the following content
             I am going to ask you to create, I need it to have a good amount of perplexity
             and burstiness. Keep that information in mind while writing. Minimum: 100, Maximum: 500, Text: """ + blogPost}

        ]
    )

    summary = completion.choices[0].message.content
    return summary


# SearchTheWeb("input any thing with key word search")
st.title('OpenSourceAI 🚀')
st.subheader(
    'Search The Web With OpenSourceAI')

input = st.text_input("Prompt:", value="", max_chars=100, key=None,
                      type="default", help=None, autocomplete=None, on_change=None,
                      args=None, kwargs=None, placeholder="search the web for ...", disabled=False,
                      label_visibility="visible")


if st.button('Generate'):
    if 'search' in input:
        with st.spinner('Searching the web for the latest information...'):
            input = input.replace("search the web for ", "")
            result = SearchTheWeb(input)
            st.text_area("Results", result.strip(),
                         height=500, max_chars=None, key=None,)
        st.success('Done!')
