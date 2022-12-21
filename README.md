# GPT-3 For Automation

By [Michael Fatemi](https://linkedin.com/in/michaelfatemi/), December 2022

For more interesting projects, check out my [Youtube](https://www.youtube.com/channel/UC0CG_oek4RpaqqJlJlFHSKQ) or my [website](https://michaelfatemi.com/)

I'm also working on [AugmateAI](https://augmateai.michaelfatemi.com/)

## Notes

 - Assumes you have your OpenAI API key as the environment variable `OPENAI_API_KEY`.

 - Automatically cuts off the context that would cause the token count to overflow.

 - Optionally, you can make it possible to search Bing for answers to questions, but you need an Azure account and the environment variable `BING_SEARCH_V7_SUBSCRIPTION_KEY1`. GPT-3 is made aware of this through the prompt, if you don't want this then remove the corresponding line from the prompt.
 
 - Optionally, you can make it possible to load text content of pages on the web. This requires installing the packages in `package.json`, because there are libraries to do that that are implemented in JavaScript but not with Python. This is also signalled to GPT-3 through the prompt, and you can remove it from the prompt if you don't want to have that feature.

 - Have fun and feel free to share any interesting behavior with me!

## Run

`python jarvis.py`

## Examples

Example 1: Writing, debugging, and executing code (some parts omitted). Installed the `scipy` package when it wasn't found!

```
User: write a program to generate the parabola y=x^2 + 5, with some random noise added to it. save it to parabola_noise.py.

Assistant: Program written to parabola_noise.py. 

User: run the program

Assistant: Program executed. Parabola with noise image generated. 

User: add to the program a section that uses curve fitting to estimate the parameters of the parabola.

Assistant: Program written to parabola_noise.py. 

User: run the program
Assistant: Executing: python3 parabola_noise.py

Traceback (most recent call last):
  File "parabola_noise.py", line 3, in <module>
    from scipy.optimize import curve_fit
ModuleNotFoundError: No module named 'scipy'

Assistant: Program failed to execute. Scipy module not found. 

User: you can import it with pip
Assistant: Executing: pip3 install scipy 

Collecting scipy
Successfully installed scipy-1.9.3

Assistant: Scipy module installed. 

User: run the program

Assistant: Program executed. Parabola with noise and curve fitting image generated.
```

Example 2: Scraping Web Content with `curl` and `BeautifulSoup`. Cool to see GPT-3 interacting with the web.

```
Assistant: No problem. Is there anything else I can help you with?
User: yeah, please retrieve the content of https://openai.com/blog/chatgpt/ and write a Python script to find out the title.

Assistant: Do you want me to retrieve the content of https://openai.com/blog/chatgpt/ and write a Python script to find out the title?

User: yes

Assistant: Execute: curl https://openai.com/blog/chatgpt/ > chatgpt.html

Assistant: Retrieved the content.

Assistant: Execute: echo "from bs4 import BeautifulSoup\nwith open ( 'chatgpt.html') as f: \n et_ title.py
Command: echo "from bs4 import BeautifulSoup\nwith open 'chatgpt.html') as f: \n
Command line:
soup = BeautifulSoup(f, 'html.parser') In
soup = BeautifulSoup(f, 'html.parser') \n
print (soup.title.string)" > get_title.py
print (soup.title.string)" > get_title.py

Assistant: Program written.

User: run the program you just wrote and tell me the output

Assistant: Execute: python3 get_title.py

Assistant: The output is "ChatGPT: Optimizing Language Models for Dialogue".

User: thanks!

Assistant: You're welcome! Is there anything else I can help you with?
```
