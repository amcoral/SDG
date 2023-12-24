import openai
from sdg_data import GOALS
from os import getenv
from dotenv import load_dotenv
load_dotenv()
#client = OpenAI()

MODEL = "gpt-3.5-turbo"

def get_prompt(goal, company, metrics):
  return f"""
  You work for the United Nations as an analyst who evaluates companies' efforts against the UN's sustainable development goals.
  You are given names of private companies and make quantitative and qualitative assessments for the initiatives they take towards making an impact across one or more of the following sustainable development initiatives.
  You are given the UN SDG goal {goal} and information about the company {company}. You are told to scrutinise the company's information from the perspective of whether they contribute towards countries meeting the following objectives:
  {", ".join(metrics)}. Produce an essay explaining how the company addresses each of these metrics comprehensively with specific examples and facts related to their activity.
  """

def get_overview(goal_num, company):
  client = openai.OpenAI()
  goal = GOALS[goal_num]["goal"]
  metrics = GOALS[goal_num]["metrics"]
  response = client.chat.completions.create(
    model=MODEL,
    messages=[
      { "role": "user", "content": get_prompt(goal=goal, metrics=metrics, company=company) }
    ],
    temperature=0
  )
  return response.choices[0].message.content
