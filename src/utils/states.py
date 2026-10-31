import operator
from typing_extensions import TypedDict, NotRequired, Annotated
from typing import Optional, List
from .objects import Analyst
from langgraph.graph import MessagesState

class GenerateAnalystsState(TypedDict):
    topic: str # Research topic
    max_analysts: int # number of analysts
    human_analyst_feedback: NotRequired[Optional[str]]  # human feedback for what is generated
    analysts: NotRequired[List[Analyst]]   # List of all our analysts


class InterviewState(MessagesState):
    # messages comes as default reducer type here like context
    max_num_turns: int # number of turns in conversation
    context: Annotated[List,operator.add]  # source of docs
    analyst: Analyst # my analyst
    interview: str # interview transcript
    sections: list # final key we duplicate in outer state for Send() api

### Annotated is used to add metadata to a type. Here, it adds a reducer to change default behhaviour of overwriting to appending to maintain history

class ResearchGraphState(TypedDict):
    topic: str # Research topic
    max_analysts: int # Number of analysts
    human_analyst_feedback: NotRequired[Optional[str]] # Human feedback
    analysts: List[Analyst] # Analyst asking questions
    sections: Annotated[list, operator.add] # Send() API key
    introduction: str # Introduction for the final report
    content: str # Content for the final report
    conclusion: str # Conclusion for the final report
    final_report: str # Final report
