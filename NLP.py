from lib2to3.pgen2 import token
from logging import exception
from operator import indexOf
from traceback import print_tb
from types import TracebackType
import openai
import time
import os

import requests
import random
from pydantic import BaseModel
from typing import Optional


key = os.getenv('gooseAiKey')
openai.api_key = key
openai.api_base = "https://api.goose.ai/v1"

"""Get tags relating to question"""
def completeTag(prompt):
 
  completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt=''' The piercing and sucking mouth parts are found in  mosquitoes: Tags: nutrition, mosquitoes, anthropoda\nThe organelle responsible for osmoregulation in Paramecium is contractile vacuole : Tags: Excretion, earthworm, organ\n'''+prompt + ":",
    max_tokens=12,
    temperature = 0.0,
    presence_penalty = 1.5,
    top_k =90,
    stream=True)
  output = ""
  for c in completion:
    output += c.choices[0].text
  output = output.splitlines()[0].strip().replace("Tags:","").strip().split(",")
  print(output)
  return output
 

def difficulty(prompt):
  completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt=''' The piercing and sucking mouth parts are found in  mosquitoes: difficulty: Meduim\nOzone hole refers to :difficulty: easy\nThe organelle responsible for osmoregulation in Paramecium is contractile vacuole : difficulty: Hard\n'''+prompt + ":",
    max_tokens=12,
    temperature = 0.9,
    presence_penalty = 1.5,
    top_k =90,
    stream=True)
  output = ""
  for c in completion:
    output += c.choices[0].text
  output = output
  print(output)

#difficulty("what is the causative agent for malaria")
"""aunthenticate api"""
def login(email,password):
  try:
    url = "https://afternoonprep-test.herokuapp.com/api/v1/auth/login"

    payload = {
    "email": "xaouliang@gmail.com",
    "password": "january27"
    }
    headers = {}

    response = requests.request("POSt",url,headers = headers ,data = payload)
    return response.json()["data"]["token"]

  except Exception as e:
    print(e.args)

"""pick one question from given questions.Would be changed when get limited question route is working on api"""
async def getOneQuestion(questions):
  try:
    num = random.randint(1, 20)
    options = ["A","B","C","D","E"]
    correcOption = questions[num]["correctOption"]
    question = questions[num]["text"]+questions[num]["options"][indexOf(options,correcOption)]["text"]
    return question
  except Exception as e:
    print(e.args)

"""get questions given subject  year and examtype"""
def getQuestion(subject,year,examType):
  try:
    token = login("xaouliang@gmail.com","january27")
    url = "https://afternoonprep-test.herokuapp.com/api/v1/questions?year=" + year + "&exam=" + examType + "&subject=" + subject
    headers = {"Authorization": "Bearer " + token}
    response = requests.request("GET", url, headers=headers)
    questions = response.json()["data"]["questions"]
    randomQuestion = getOneQuestion(questions)
    completeTag(randomQuestion)

  except Exception as e:
    print(e)





class question(BaseModel):
    question : str
#getQuestion("Biology","2004","JAMB")



def questionFromText(text):
  try:
    
    
    completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt=''' [Context]: NLP Cloud was founded in 2021 when the team realized there was no easy way to reliably leverage Natural Language Processing in production.
    [Question]: When was NLP Cloud founded? A)2019 B)2020 C)2021 D)2022
    [Answer] :C) 2021
    ###
    [Context]: All plans can be stopped anytime. You only pay for the time you used the service. In case of a downgrade, you will get a discount on your next invoice.
    [question]: When can plans be stopped? A) Anytime B) Never C)Monthly D) Weekly
    [answer] : A) Anytime
    ###
    [Context]:'''+text + ":",
    max_tokens=100,
    presence_penalty = 1.5,
    temperature = 0.1,
    top_k =90,
    stream=True
    )
    output = ""
    for c in completion:
      
      output += c.choices[0].text
    
    print(output.strip().split("###")[0])
    

  except Exception as e:
    print(e)

# questionFromText(''' Biology is the science that studies life. What exactly is life? This may sound like a silly question with an obvious answer, but it is not easy to define life. For example, a branch of biology called virology studies viruses, which exhibit some of the characteristics of living entities but lack others. It turns out that although viruses can attack living organisms, cause diseases, and even reproduce, they do not meet the criteria that biologists use to define life.From its earliest beginnings, biology has wrestled with four questions: What are the shared properties that make something “alive”? How do those various living things function? When faced with the remarkable diversity of life, how do we organize the different kinds of organisms so that we can better understand them? And, finally—what biologists ultimately seek to understand—how did this diversity arise and how is it continuing? As new organisms are discovered every day, biologists continue to seek answers to these and other questions.Properties of LifeAll groups of living organisms share several key characteristics or functions: order, sensitivity or response to stimuli, reproduction, adaptation, growth and development, regulation/homeostasis, and energy processing. When viewed together, these eight characteristics serve to define life.OrderOrganisms are highly organized structures that consist of one or more cells. Even very simple, single-celled organisms are remarkably complex. Inside each cell, atoms make up molecules. These in turn make up cell components or organelles.Multicellular organisms, which may consist of millions of individual cells, have an advantage over single-celled organisms in that their cells can be specialized to perform specific functions, and even sacrificed in certain situations for the good of the organism as a whole. How these specialized cells come together to form organs such as the heart, lung, or skin in organisms like the toad shown in Figure 1.2 will be discussed later.''')

"""use given tags to form questions"""
def tagsToQuestions(tags):
  try:
    
    tagStrng = ",".join(tags)
    completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt=''' [Tags]: nutrition, mosquitoes, anthropoda
    [question]: The piercing and sucking mouth parts are found in  A.  grasshoppers B.  mosquitoes C.  termites D.  cockroaches
    [Answer] :B) mosquitoes
    ###
    Tags: Excretion, earthworm, organ :
    [question]: The organelle responsible for osmoregulation in Paramecium is A.  flame cell B.  nephridia C.  contractile vacuole D.  Malpighian tubule
    [answer] : C) contractile vacuole
    ###
    # '''+tagStrng + ":",
    max_tokens=100,
    presence_penalty = 1.5,
    temperature = 0.5,
    top_k =90,
    stream=True
    )
    output = ""
    for c in completion:
      
      output += c.choices[0].text
    
    print(output.strip().split("###")[0])
    print(tagStrng)

  except Exception as e:
    print(e)

#tagsToQuestions(["cell","blood","life"])

"""translate fom english to french"""
def engToFrench(eng):
  try:
    
    completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt=" English :"+ eng +"\German : ",
    max_tokens=100,
    presence_penalty = 1.5,
    temperature = 0.0,
    top_k =90,
    stream=True
    )
    output = ""
    for c in completion:
      
      output += c.choices[0].text
    
    print(output.strip().splitlines()[0])
    return output.strip().splitlines()[0]
  except Exception as e:
    print(e)

#engToFrench("Thank you for your patience with me after alot of thinking about what the long term strategy should be, i decided to go back to the drawing board")

"""translate from french to english"""
def frnchToEnglish(french):
  try:
    
    completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt=" German :"+ french +"\English : ",
    max_tokens=100,
    presence_penalty = 1.5,
    temperature = 0.0,
    top_k =90,
    stream=True
    )
    output = ""
    for c in completion:
      
      output += c.choices[0].text
    
    print(output.strip().splitlines()[0])
    return output.strip().splitlines()[0]
  except Exception as e:
      print(e)

#frnchToEnglish(" Merci pour votre patience avec moi après beaucoup d'efforts de réflexion sur la stratégie à long terme, j'ai décidé de revenir au point de départ et de redessiner le projet.")
"""paraphrase or rewrite a given block of text"""

def rewrite(text):
  try:
    
    completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt="""[Original]: Algeria recalled its ambassador to Paris on Saturday and closed its airspace to French military planes a day later after the French president made comments about the northern Africa country. 
        [Paraphrase]: Last Saturday, the Algerian government recalled its ambassador and stopped accepting French military airplanes in its airspace. It happened one day after the French president made comments about Algeria.
        ###
        [Original]: President Macron was quoted as saying the former French colony was ruled by a "political-military system" with an official history that was based not on truth, but on hatred of France.
        [Paraphrase]: Emmanuel Macron said that the former colony was lying and angry at France. He also said that the country was ruled by a "political-military system".
        ###
        [Original]: The diplomatic spat came days after France cut the number of visas it issues for citizens of Algeria and other North African countries.
        [Paraphrase]: Diplomatic issues started appearing when France decided to stop granting visas to Algerian people and other North African people.
        ###
        [Original]: """ + text +  """.
        [Paraphrase]:""",
    max_tokens=100,
    end_sequence="\n###",
    presence_penalty = 2.0,
    temperature = 0.1,
    top_k =90,
    stream=True
    )
    output = ""
    for c in completion:
    
      output += c.choices[0].text
    
    print(output.strip().splitlines()[0])
    return output.strip().splitlines()[0]
  except Exception as e:
      print(e)

#rewrite("i persevere in every situation")
def rewriteWithTranslation(text):
  try:
    
    
    answer = engToFrench(text)
    
    reply = frnchToEnglish(answer)
    
    
    
    
  except Exception as e:
      print(e)


#rewriteWithTranslation("i persevere in every situation")

"""summarize a given block of text"""
def summarize(text):
  try:
    
    completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt="""[Original]: America has changed dramatically during recent years. Not only has the number of graduates in traditional engineering disciplines such as mechanical, civil, electrical, chemical, and aeronautical engineering declined, but in most of the premier American universities engineering curricula now concentrate on and encourage largely the study of engineering science.  As a result, there are declining offerings in engineering subjects dealing with infrastructure, the environment, and related issues, and greater concentration on high technology subjects, largely supporting increasingly complex scientific developments. While the latter is important, it should not be at the expense of more traditional engineering.
        Rapidly developing economies such as China and India, as well as other industrial countries in Europe and Asia, continue to encourage and advance the teaching of engineering. Both China and India, respectively, graduate six and eight times as many traditional engineers as does the United States. Other industrial countries at minimum maintain their output, while America suffers an increasingly serious decline in the number of engineering graduates and a lack of well-educated engineers. 
        (Source:  Excerpted from Frankel, E.G. (2008, May/June) Change in education: The cost of sacrificing fundamentals. MIT Faculty 
        [Summary]: MIT Professor Emeritus Ernst G. Frankel (2008) has called for a return to a course of study that emphasizes the traditional skills of engineering, noting that the number of American engineering graduates with these skills has fallen sharply when compared to the number coming from other countries. 
        ###
        [Original]: So how do you go about identifying your strengths and weaknesses, and analyzing the opportunities and threats that flow from them? SWOT Analysis is a useful technique that helps you to do this.
        What makes SWOT especially powerful is that, with a little thought, it can help you to uncover opportunities that you would not otherwise have spotted. And by understanding your weaknesses, you can manage and eliminate threats that might otherwise hurt your ability to move forward in your role.
        If you look at yourself using the SWOT framework, you can start to separate yourself from your peers, and further develop the specialized talents and abilities that you need in order to advance your career and to help you achieve your personal goals.
        [Summary]: SWOT Analysis is a technique that helps you identify strengths, weakness, opportunities, and threats. Understanding and managing these factors helps you to develop the abilities you need to achieve your goals and progress in your career.
        ###
        [Original]: """ + text + """
        [Summary]:""",
    max_tokens=100,
    end_sequence="\n###",
    presence_penalty = 1.5,
    temperature = 1.0,
    top_k =90,
    stream=True
    )
    output = ""
    for c in completion:
    
      output += c.choices[0].text
    
    print(output.strip().splitlines()[0])
    return output.strip().splitlines()[0]
  except Exception as e:
      print(e)
#summarize('''Jupiter is the fifth planet from the Sun and the largest in the Solar System. It is a gas giant with a mass one-thousandth that of the Sun, but two-and-a-half times that of all the other planets in the Solar System combined. Jupiter is one of the brightest objects visible to the naked eye in the night sky, and has been known to ancient civilizations since before recorded history. It is named after the Roman god Jupiter.[19] When viewed from Earth, Jupiter can be bright enough for its reflected light to cast visible shadows,[20] and is on average the third-brightest natural object in the night sky after the Moon and Venus.
 #      Jupiter is primarily composed of hydrogen with a quarter of its mass being helium, though helium comprises only about a tenth of the number of molecules. It may also have a rocky core of heavier elements,[21] but like the other giant planets, Jupiter lacks a well-defined solid surface. Because of its rapid rotation, the planet's shape is that of an oblate spheroid (it has a slight but noticeable bulge around the equator).
#      ''')

#could be integrated with postma but process not cleaqr yet
#still not precise

"""provide answer to an obj question
   still not precise
   could be integrated to use postman 
    """
def explainObjAnswer(question):
  try:
    
    completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt="""Who among the following could be described as the founding father of Nigeria nationalism: Herbert Macaulay 
        [Expalnation]: Olayinka Herbert Samuel Heelas Badmus Macaulay(14 November 1864 – 7 May 1946) was a Nigerian nationalist, politician, engineer, architect, journalist, and musician and is considered by many Nigerians as the founder of Nigerian nationalism
        ###
        [Original]:Rule of law means supremacy of the law : supremacy of the law
        [Explanation]: The rule of law simply means that the law is supreme in the law. supremacy of the law is the  command of the Sovereign state which means that law has its source in sovereign authority, law is accompanied by sanctions, and the command to be a law should compel a course of conduct.
        ###
        [Original]:A major characteristics of civil society is  : social responsibility
        [Explanation]:"""
,
    max_tokens=100,
    end_sequence="\n###",
    presence_penalty = 1.5,
    temperature = 0.1,
    top_k =90,
    stream=True
    )
    output = ""
    for c in completion:
    
      output += c.choices[0].text
    
    print(output.strip().split("###")[0])
    return output.strip().splitlines()[0]
  except Exception as e:
      print(e)

#explainObjAnswer("dd")
#could be integrated with postma but process not cleaqr yet

"""provide answer to a theory question
   problem with list questions
   could be integrated to use postman 
    """
def getTheoryAnswer(question):
  max_token = 0
  try:
    questionSplit = question.lower().split(" ")
    if "highlight" in questionSplit or "enumerate" in questionSplit or "list" in questionSplit or "mention" in questionSplit:
      max_token = 500
      
    else:
      max_token = 50
    completion = openai.Completion.create(
    engine="gpt-j-6b",
    prompt="""[Original]: (a) What are values?
          [Explanation]:(a) Definition of Values; 

          -Values can be defined as the importance or worth which is attached to something. or

          - Values mean that which is desirable, right and acceptable, that which is generally accepted as being of great worth to people. or

          - Values are regarded as the beliefs, norms, traditions, behaviours and practices acceptable in the society which guide and direct the behaviour of the people in the society. or

          - Values is the usefulness or worth of something. or

          -Values are the actual worth of an object or item in monetary form
        ###
        [Original]: (b) State six importance of values
        [Explanation]:i. Values bring about happiness and contentment

          ii. Values guide human behaviour

          iii. Values promote positive relationship among people

          iv. Values give good purpose and direction to our lives, both in the family and in the society

          v. Values help us to resist pressure to conform to other people's values and behaviour which may not be good norms

          vi. Values ultimately promote development in the society

          vii. Values encourage tolerance and relationship among people in the society

          viii. Values promote unity, harmony and cooperation in the society

          ix. Values modify attitudes and feelings towards other people and make people more friendly

          x. Values act as criteria or measures for the judgment of the actions of individuals in society 
        ###   
          [Original]: """ + question +"""
        [Explanation]:
        """
,
    max_tokens=max_token,
    end_sequence="\n###",
    presence_penalty = 1.5,
    temperature = 0.5,
    top_k =90,
    stream=True
    )
    output = ""
    for c in completion:
    
      output += c.choices[0].text
    if max_token == 50:
      print(output.strip().splitlines()[0])
      #return output.strip()
    else:
      print(output.strip().split("###")[0])
      return output.strip().split("###")[0]
  except Exception as e:
      print(e)
#getTheoryAnswer(" Define citezenship")