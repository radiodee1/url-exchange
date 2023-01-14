# url-exchange
* Comparing GPTJ with GPT3 using some prompt engineering.
* Introduce something called a 'URL-Exchange.'

## History
* In 2020 I worked on my thesis project that included some experiments with GPT2. These models were installed on Raspberry Pi computers. This code was mostly python. Speech to text and text to speech were attempted.
* Subsequently to that I have a private github repo for GPTJ and other relatively sized GPT models. These models were generally hosted by some company on-line and accessed using web fetch-like commands. This repo used javascript and electron for a gui. This project was ported to android.
* Still later I have attempted a chatbot that uses BERT. This is a departure from the GPT projects. The chat-bert project uses hard coded responses to many questions. It is not Auto-generative. It is comparable to AIML, but because the project uses BERT, the input prompt need not match the saved prompt completely. You can find more on this at the project repo. BERT is a smaller model when compared to GPT3.
* This repo is similar to the 'electron' repo, in that it is used with GPTJ and GPT3 on line. I am interested in comparing GPTJ and GPT3 and trying out various experiments, the most interesting being the 'URL-Exchange,' as described below.

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

## Problems
When you use these models you don't have to prompt the model in exactly the same way every time. You can address the model with lines like 'Hello there' or 'How are you'. Both of these are general greetings and they will be treated similarly. At the same time, the output will be human-readable, but not easy to predict. In our example, the outputs could be 'hi' or 'I'm fine'. Both outputs are possible, along with a number of others. The outputs are slighlty unpredictable.

We want to edit our prompt so that when, for example, we want to turn on the radio, the model will understand and will signal us somehow with a predictable reply.

## URLs in Generative models 
When you use GPT models you can sometimes predict what the model will answer. Sometimes you want to do something like launching code when the model broaches a certian subject.


