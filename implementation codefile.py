Use Gemini and ChatGPT to learn from two capable teachers
Use Google's latest model release, Gemini, to teach you what you want to know and compare those with ChatGPT's responses.
The models are specifically prompted not to generate extra text to make it easier to compare any differences.

#Configure Gemini API key

#@title Configure Gemini API key

# access your Gemini API key

import google.generativeai as genai
from google.colab import userdata

gemini_api_secret_name = 'GOOGLE_API_KEY'  # @param {type: "string"}

try:
  GOOGLE_API_KEY=userdata.get(gemini_api_secret_name)
  genai.configure(api_key=GOOGLE_API_KEY)
except userdata.SecretNotFoundError as e:
   print(f'''Secret not found\n\nThis expects you to create a secret named {gemini_api_secret_name} in Colab\n\nVisit https://makersuite.google.com/app/apikey to create an API key\n\nStore that in the secrets section on the left side of the notebook (key icon)\n\nName the secret {gemini_api_secret_name}''')
   raise e
except userdata.NotebookAccessError as e:
  print(f'''You need to grant this notebook access to the {gemini_api_secret_name} secret in order for the notebook to access Gemini on your behalf.''')
  raise e
except Exception as e:
  # unknown error
  print(f"There was an unknown error. Ensure you have a secret {gemini_api_secret_name} stored in Colab and it's a valid key from https://makersuite.google.com/app/apikey")
  raise e

model = genai.GenerativeModel('gemini-pro')

#Configure OpenAI API key

#@title Configure OpenAI API key

# access your OpenAI API key

# installing llmx first isn't necessary but avoids a confusing error when installing openai
!pip install -q llmx
!pip install -q openai
from openai import OpenAI

openai_api_secret_name = 'OPENAI_API_KEY'  # @param {type: "string"}

try:
  OPENAI_API_KEY=userdata.get(openai_api_secret_name)
  client = OpenAI(
    api_key=OPENAI_API_KEY
  )
except userdata.SecretNotFoundError as e:
   print(f'''Secret not found\n\nThis expects you to create a secret named {openai_api_secret_name} in Colab\n\nVisit https://platform.openai.com/api-keys to create an API key\n\nStore that in the secrets section on the left side of the notebook (key icon)\n\nName the secret {openai_api_secret_name}''')
   raise e
except userdata.NotebookAccessError as e:
  print(f'''You need to grant this notebook access to the {openai_api_secret_name} secret in order for the notebook to access Gemini on your behalf.''')
  raise e
except Exception as e:
  # unknown error
  print(f"There was an unknown error. Ensure you have a secret {openai_api_secret_name} stored in Colab and it's a valid key from https://platform.openai.com/api-keys")
  raise e

#Ask a question!

#@title Ask a question!

text = 'Write a python function that calculates the distance between any two latitudes and longitudes on earth' # @param {type:"string"}

# ask Gemini
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

response = chat.send_message('%s -- Please answer as concisely as you can, avoiding any extra conversation or text' % text)
gemini_response = response.text

# ask ChatGPT
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": '%s -- Please answer as concisely as you can, avoiding any extra conversation or text' % text}
  ]
)

openai_response = completion.choices[0].message.content

# render the diff

# importing these every execution is unnecessary but avoids another notebook cell
from IPython.display import HTML
import difflib

# omit the legend to slim down the UI
difflib.HtmlDiff._legend = ''

HTML(difflib.HtmlDiff().make_file(gemini_response.splitlines(), openai_response.splitlines(), 'Gemini', 'ChatGPT'))

