from dotenv import load_dotenv
from .states import GenerateAnalystsState, InterviewState, ResearchGraphState
from langgraph.graph import END
from langchain.messages import AIMessage, HumanMessage
from typing import Literal
from langgraph.types import Send

load_dotenv()

def should_continue(state:GenerateAnalystsState):
    """Return next node to continue"""

    human_analyst_feedback = state.get('human_analyst_feedback',None)
    if human_analyst_feedback:
        return "create_analysts"
    return END

def routes_messages(state: InterviewState, name:str = 'expert'):
    """Routes between question and answer"""

    messages = state['messages']
    max_turns = state.get('max_num_turns',2)

    # count how many AI responses are actual answers by experts and not just questions
    num_responses = len([m for m in messages if isinstance(m,AIMessage) and m.name == name])

    if num_responses >= max_turns: return "save_interview"

    return "ask_question"

def initiate_all_interviews(state: ResearchGraphState):
    """Map step to run interview for each analyst using the subgraph"""
    human_analyst_feedback = state.get('human_analyst_feedback',None)
    if human_analyst_feedback:
        return "create_analysts"
    else:
        topic = state['topic']
        # use the Send() API to call the sub-graph on all available analysts
        return [
            Send('conduct_interview',{
                'analyst': analyst,
                'messages':[HumanMessage(content=f"So you said you were writing an article on {topic}")]
            }) for analyst in state['analysts']
        ]
