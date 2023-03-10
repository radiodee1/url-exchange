# url-exchange
* Comparing GPTJ with GPT3 using some prompt engineering.
* Test something called a 'URL-Exchange' that does not work well.

## History
* In 2020 I worked on my thesis project that included some experiments with GPT2. These models were installed on Raspberry Pi computers. This code was mostly python. Speech to text and text to speech were attempted.
* Subsequently to that I have a private github repo for GPTJ and other relatively sized GPT models. These models were generally hosted by some company on-line and accessed using web fetch-like commands. This repo used javascript and electron for a gui. This project was ported to android. The desktop version was programmed entirely in Javascript, and the android version used Java and Javascript.
* Still later I have attempted a chatbot that uses BERT. This is a departure from the GPT projects. The chat-bert project uses hard coded responses to many questions. It is not Auto-generative. It is comparable to AIML, but because the project uses BERT, the input prompt need not match the saved prompt completely. You can find more on this at the project repo. BERT is a smaller model when compared to GPT3.
* This repo is similar to the 'electron' repo, in that it is used with GPTJ and GPT3 on line. I am interested in comparing GPTJ and GPT3 and trying out various experiments, the most interesting being the 'URL-Exchange,' as described below. This version and repo uses Python 3.10.

## Disclaimer
In some ways this project and what it attempts to do flat-out doesn't work. Launching code from a GPT client is difficult. This repository is and was used for experiments with GPTJ and GPT3. In no way does that mean the code here is ready for any kind of distribution or other use.

## Prompts
For the totality of my interaction with GPT I have been interested in the chatbot model. I would describe this as a question and answer paradigm where you can ask the model something and it will respond in a normal way, as if you were having a conversation. 

To implement this I have come up with my own prompt. It is probably what would be described as 'multi-shot'. Essentially the GPT model is shown a number of question and answer pairs, with the final question/answer left empty - later to be filled in by the user and the model.

The first few question/answer pairs are examples that include some simple facts that we would like the model to use with every response. The questions and answers are also labled with names so that the model can use the info to make some sort of persona. This sounds complex, but it is really very simple. Below is an example. I have used this prompt system pretty consistently from my first experiments with GPT models.

```
Human: Hi?
Jane: Hello there.

Human: Do you like candy?
Jane: Yes I like candy.

Human: What is your favorite color?
Jane: My favorite color is blue.

Human: How old are you?
Jane: I am 21 years old.

Human:

```

The prompt here is constructed before hand, and then the user's input is pasted after the identifier 'Human'. Then the word 'Jane' is added to the prompt, and the whole thing is fed to the GPT model. It tries to finish the line with the identifier 'Jane'. 

With this system you can get the models to answer your questions, but the outcomes are only partly predictable. 

## Home-Assistants
I had the experience of going to someone's house and observing them using their Alexa or Google-Home-Assistant devices. I was surprised at the things that the device could do. You could set timers. You could play radio stations. I suspect you could ask it to search the web for you. I wanted to do some of these things in my language models.

Imagine you wanted to instruct the model to turn on a radio. You might say 'Turn on the radio' and the model might reply 'OK, I'll turn on the radio'. It might reply 'The radio will be turned on' or just 'radio'. What we want is a predictable output that we can process. GPT models are great at generating text, but the text is not always the same. Computers can process this text, but they are best at the job when they get exactly what they expect. It would be easier for the computer if the text were always the same. This was the inspiration for the URL Exchange.

What I did is I added a custom question/answer pair for every outcome that I want the model to detect. The question is something like 'Turn on the radio' and the answer is essentially a url. What I wanted was for the models to reply to the question with the exact url, spelled exactly as specified in the prompt. This ability to answer with the exact url is more evident in the smaller GPT models. An example is below.

```
Human: Turn on classic radio.
Jane: Set radio http://radio 

Human: Set a timer for five minutes.
Jane: Set timer http://timer 

Human: Hi?
Jane: Hello there.

Human: Do you like candy?
Jane: Yes I like candy.

Human: What is your favorite color?
Jane: My favorite color is blue.

Human: How old are you?
Jane: I am 21 years old.

```

Originally I thought that the models, especially GPTJ, were trained on material taken from the web. One of the things common in the corpus is complete urls. I thought the model was trained on complete urls and so it knows that they need to be reproduced letter for letter. This may not be true.

## URL Exchange - Overview
Using the URL Exchange would require the following steps. Essentially the Exchange trades URLs or Keywords with the execution of some specific piece of code.

* Start the GPT language model.
* Answer the model's initial question and request that it perform some action.
* The model recognizes the Keyword in the request and starts the URL Exchange.
* The URL Exchange starts a Wizard which, unseen to the user, collects all the info necessary to launch some code.
* The code is launched.

## URL Exchange - Prompt  
We add these specific urls to our prompt. We put them at the beginning. There is one of these urls for every task we want the model to perform. 

* We expect the model to answer with the particular url whenever we suggest that the model should do one of our pre-determined tasks. This is called our 'url exchange.' We exchange the url for a specific programmatic action.
* We ask the chatbot to answer questions about the single statement we collect that caused the model to use the url. We call this a 'Wizard' as it is modeled after the Wizards that are common in Windows operating systems when you install software. The Wizard poses questions to the model, and the questions are not visible to the user. 

## URL Exchange vs. Keyword Exchange 
Strangely the URL copying ability is not as strong in GPT3. For GPT3 we do our search for the url, but also for the english word that has the same representation as the url. For example, when we want to detect when the GPT3 model launches a timer, we search for 'http://timer' and also 'timer', since the word for the action can easily be designated as 'timer'.

While the GPT3 model does not always repeat the full url, it does repeat the simpler word ('timer') and it answers the question set about the timer very well. It answers the questions better than the GPTJ model.

It turns out that neither model repeats the url totally faithfully. This is a failure in our original concept. If we choose to search for both the url and the english equivelent we catch the hint that the model is making, and then we can launch the Wizard properly. Of course, if we follow this new search method, we probably should call the project a 'Text Exchange' or a 'Keyword Exchange'.

## URL Exchange - Wizards 
The Wizards are series of questions that are posed to the model. The name Wizard is just a programing name. It's just the name I used for the section of the code that questions about the thing that the user wants the model to do. The prompt during these questions includes the user's questions asking the model to do something. The model's answer is recorded but the questions are disgarded. The wizard questions are not added to the prompt history.

The answers to these Wizard questions go twards performing the special task. For example, the timer questions ask what the timer length is and what is the name for it.

## Requirements
I am working on Ubuntu 22.10, and Python 3.10. I install these files.
```
sudo apt install -y rustc cargo python3.10-dev python3-pip python3-pip-whl  
```

The code is also meant to be Docker-izable. You need to install Docker yourself, but after that there are scripts in the repository that help to make the Docker container. 

## Environment Variables
This code uses AI models on line that require special authentication to be performed. In order for this model to work for you, you need special authentication information stored in environment variables on your computer. For a linux setup these variables would be set in the `.bashrc` file in your `home` directory. The content of these variables needs to be obtained from either OpenAI, or Mystic.ai/Pipeline.ai, and the process of obtaining these is beyond the scope of this document. Basically you need to go to the sites and get the authentication keys. You might need to pay for Pipeline.ai. Note, GPT3 from OpenAI is the larger model and GPTJ from Mystic.ai is the smaller model.

The program uses two variables for GPTJ. They are GPT_ETC_GPTJ_KEY and GPT_ETC_GPTJ_MODEL.

The program also can be directed to use GPT3. That uses the OPENAI_API_KEY environment variable. 

## ChatGPT vs GPT3 vs GPTJ 
At the time of this writing ChatGPT is a very big deal in the AI world. The prompts we construct for GPT3 and GPTJ do not work on ChatGPT. We need to spend time on the other GPT models. 

GPT3 is larger than GPTJ. GPT3 also is faster than GPTJ, and is a larger model, so it does things like answer questions from the Wizards better. GPT3 is free at this moment, While GPTJ is a paid for service. Unfortunately GPT3 is sometimes unavailable because it is so busy.

## Curses 
The `exchange.py` program is composed of several classes. It is meant to be easily incorporated in other programs. It has code that keeps track of a number of Wizard objects that could be used for managing things like timers and online radio services. This is the purpose of the 'URL Exchange', though as stated above, it might be misnamed. A better name might be 'Keyword Exchange.' It has an object called `Exchange` that has a method called `get_status` that should be easy to call from another program and that returns all the info needed to operate special appliances like timers and on-line radio stations, etc.

For this example the `main.py` program was written. The `main.py` program is written to make example of `exchange.py`. The `main.py` program uses threads and curses (though curses is not a thread-safe library) to display its output. There is a box on the screen for input, one for output, and one that is especially for the state of the Wizard objects from `exchange.py`. These Wizard objects are updated every 10 seconds. This update interval is specified in the `main.py` code.
