import functools
import requests
import os


def huggingface(model_key, prompt: str, temperature=0.7, max_tokens=120, stop=None):
	API_URL = "https://api-inference.huggingface.co/models/" + model_key # "bigscience/bloom"
	response = requests.post(API_URL, headers={
		"Authorization": "Bearer " + os.environ['HUGGINGFACE_API_KEY'],
	}, json={
		"inputs": prompt,
		"parameters": {
			"max_length": max_tokens,
			"temperature": temperature,
			"return_full_text": False,
			"stop": stop,
		}
	})
	j = response.json()
	if type(j) is list:
		j = j[0]
	return j['generated_text']

def openai(model_key, prompt: str, temperature=0.7, max_tokens=120, stop=None) -> str:
	body = {
		'model': model_key,
		'prompt': prompt,
		'temperature': temperature,
		'max_tokens': max_tokens,
		'top_p': 1,
		'frequency_penalty': 0,
		'presence_penalty': 0,
		'stop': stop,
	}
	headers = {
		'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
		'Content-Type': 'application/json',
	}
	response = requests.post('https://api.openai.com/v1/completions', json=body, headers=headers)
	response = response.json()

	if 'choices' not in response:
		raise ValueError("Invalid response from OpenAI: " + str(response))

	return response['choices'][0]['text']

def get_api(method: str):
	if method.startswith("hf:"):
		return functools.partial(huggingface, method[3:])
	elif method.startswith("openai:"):
		return functools.partial(openai, method[7:])
	else:
		return None

class CompletionPrompt:
	def __init__(self, template: str, model_key: str = 'text-davinci-003', generation_params = {}):
		self.template = template
		self.model_key = model_key
		self.generation_params = generation_params

	def __call__(self, **kwargs):
		# print(f"Calling prompt with {kwargs=} and {self.generation_params=}")
		return openai(self.model_key, self.template.format(**kwargs), **self.generation_params)

class ListPrompt(CompletionPrompt):
	def __call__(self, **kwargs):
		completion = super().__call__(**kwargs)
		return extract_list_from_gpt_completion(completion)

def extract_list_from_gpt_completion(completion: str):
	import re

	results = []
	next_is_result = False
	for line in completion.splitlines():
		line = line.strip()

		if len(line) == 0:
			continue

		if next_is_result:
			results.append(line)
			next_is_result = False
			continue

		if len(results) == 0:
			results.append(line.strip())
		elif re.match(r'^\d+\. .+$', line):
			phrase = line[line.index('.') + 1:].strip()
			results.append(phrase)
		elif re.match(r'^\d+\.$', line):
			next_is_result = True
	
	return results
