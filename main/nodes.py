from state import graphState
from prompts import FAQ_prompt, Lead_prompt, Escal_prompt, Convo_prompt, Conversation_ender
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_anthropic import ChatAnthropic
from pydantic import SecretStr
from dotenv import load_dotenv
import os
load_dotenv()
groq_api=os.getenv("groq_api")


model1=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=SecretStr(groq_api) if groq_api else None,
    temperature=0.1
)

api_anthro=os.getenv('anthro')
api = SecretStr(api_anthro) if api_anthro else None

model = ChatAnthropic(
    model_name="claude-3-5-haiku-20241022",
    api_key=api, # type: ignore
    temperature=0,
    timeout=60,
    stop=None
)

def FAQ_node(state:graphState):
    user_message="" 
    message=''
    user_messages=[]
    ai_messages=[]
    message_history=[]
    prompt=PromptTemplate(template=FAQ_prompt, input_variables=['usermessage','user_messages', 'ai_messages'])
    route_node=state.get('route_node')
    while route_node=='FAQ_node':
        user_message=input("Enter your quesiton:")
        #finalprompt=prompt.format_prompt(usermessage=user_message, user_messages=user_messages, ai_messsages=ai_messsages)
        chain=(prompt| model1 |JsonOutputParser())
        result=chain.invoke(input={'usermessage':user_message, 'user_messages':user_messages, 'ai_messages':ai_messages})
        message=result.get("ai_message")
        print(message)
        user_messages.append(user_message)
        ai_messages.append(message)
        message_history={'user_messages':user_message,'ai_messages':message}
        route_node=result.get("route_node")
    return{
        'message_history':message_history,
        'route_node':route_node
    }
   

def Lead_node(state:graphState):
    counter=1
    message_history=state.get('message_history')
    user_reply=''
    questions=[]
    route_node=state.get('route_node')
    prompt=PromptTemplate(template=Lead_prompt, input_variables=['message_history', 'user_message','asked_questions'])
    while route_node=='Lead_node' and counter<4:
        chain=(prompt| model1 |JsonOutputParser())
        result=chain.invoke(input={'message_history':message_history, 'asked_questions':questions,'user_message':user_reply})
        question=result.get("ai_message")
        print(question)
        user_reply=input("Enter your answer:")
        questions.append(question)
        message_history={'Lead_ai_messages':question,'Lead_user_reply':user_reply}
        route_node=result.get("route_node")
        counter+=1
    if counter==4 and route_node=='Lead_node':
            prompt=PromptTemplate(template=Conversation_ender, input_variables=['message_history'])
            chain=(prompt| model1 |StrOutputParser())
            result=chain.invoke(input={'message_history':message_history})
            print(result)
            route_node='Convo_node'


    return{
        'message_history':message_history,
        'route_node':route_node
    }

def Escal_node(state:graphState):
    message_history=state.get('message_history')
    prompt=PromptTemplate(template=Escal_prompt, input_variables=['message_history'])
    chain=(prompt| model1 |JsonOutputParser())
    result=chain.invoke(input={'message_history':message_history})
    escalation=result.get('Escalation')    
    print("ESCALATION Report",result)
    return {
        'escalation':escalation,
        'escalation_ticket':result,
        'route_node':'Convo_node'
    }

def Convo_node(state:graphState):
    message_history=state.get('message_history')
    prompt=PromptTemplate(template=Convo_prompt, input_variables=['message_history'])
    chain=(prompt| model1 |JsonOutputParser())
    result=chain.invoke(input={'message_history':message_history})
    print("COVERSATION Report",result)
    return {
        'conversation_summary':result
    }

def router_node(state:graphState):
    route=state.get('route_node')
    if route=='Lead_node':
        return 'Lead_node'
    elif route=='Escal_node':
        return 'Escal_node'
    elif route=='Convo_node':
        return 'Convo_node'


# state:graphState={
#     'route_node':'FAQ_node'
#     }
# result=FAQ_node(state)
# state.update(result) # type: ignore
# if state.get('route_node')=='Lead_node':
#     result1=Lead_node(state)
#     print(result1)
# elif state.get('route_node')=='Escal_node':
#     result1=Escal_node(state)
#     print(result1)

# state.update(result1) # type: ignore
# if state.get('route_node')=='Convo_node':
#     result2=Convo_node(state)
#     print(result2)




