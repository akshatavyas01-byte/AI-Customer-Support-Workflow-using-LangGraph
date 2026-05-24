from typing import TypedDict

class graphState(TypedDict, total=False):
    route_node:str
    user_message:str
    ai_message:str
    message_history:list[dict]
    escalation:bool
    escalation_ticket:dict
    conversation_summary:dict