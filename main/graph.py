from langgraph.graph import StateGraph, START, END
from state import graphState
from nodes import FAQ_node, Escal_node, Lead_node, Convo_node, router_node

graph=StateGraph(graphState)

graph.add_node('faq_node',FAQ_node)
graph.add_node('lead_node',Lead_node)
graph.add_node('escal_node',Escal_node)
graph.add_node('convo_node',Convo_node)
graph.add_node('router_node',router_node)

graph.add_edge(START, 'faq_node')
graph.add_conditional_edges('faq_node',
                            router_node,
        {'Lead_node':'lead_node',
         'Escal_node':'escal_node'
})
graph.add_conditional_edges('lead_node',
                            router_node,
        {'Convo_node':'convo_node',
         'Escal_node':'escal_node'
})
graph.add_edge('escal_node','convo_node')
graph.add_edge('convo_node',END)

Customer_support=graph.compile()

state:graphState={
    'route_node':'FAQ_node'
    }
Customer_support.invoke(state)
