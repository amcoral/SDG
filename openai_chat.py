import openai
from sdg_data import GOALS
from os import getenv
from dotenv import load_dotenv
load_dotenv()
#client = OpenAI()

MODEL = "gpt-4o"

def get_prompt(goal, company, metrics):
  return f"""
  You work for the United Nations as an analyst who makes qualitative and quantitative assessments of the activities of a given private company that contribute towards the UN's Sustainable Development Goals (SDG).
  You are given the UN SDG goal {goal} and its following targets: {", ".join(metrics)}. You are also given several news articles about company {company}. For each target, list the facts about the company's activities that contribute to achieving that target. There should be at least 3 detailed facts with examples of acivities and names of institutions involved for each target.
  Produce a source for each fact you found.
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
