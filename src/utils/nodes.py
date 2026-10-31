from dotenv import load_dotenv
from .states import GenerateAnalystsState, InterviewState, ResearchGraphState
from .models import llm,llama_llm
from .objects import Analyst, Perspectives, SearchQuery
from .prompts import analyst_instructions, question_instructions, search_instructions, answer_instructions, section_writer_instructions, report_writer_instructions, intro_conclusion_instructions
from langchain.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt
from langchain_tavily import TavilySearch
from langchain_core.messages import get_buffer_string

load_dotenv()

def create_analysts(state: GenerateAnalystsState):

    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback','')

    # enforce structured output
    structured_llm = llm.with_structured_output(Perspectives)

    # system message
    system_message = analyst_instructions.format(topic=topic,human_analyst_feedback=human_analyst_feedback,max_analysts=max_analysts)

    # Generate analyst
    analysts = structured_llm.invoke([SystemMessage(content=system_message)] + [HumanMessage(content="Please generate the set of analysts")])

    return {'analysts': analysts.analysts}


def human_feedback(state: GenerateAnalystsState):

    feedback = interrupt({
        "question":"Are these analysts okay for you?",
        "analysts":[
            analyst.model_dump() if hasattr(analyst,"model_dump") else analyst for analyst in state.get('analysts',[])
        ],
        "instructions": "Return feedback to regenerate analysts or return empty/perfect/continue/okay/none to approve and continue the graph"
    })

    if feedback is None:
        return {'human_analyst_feedback': None}
    
    if isinstance(feedback, str):

        if feedback.strip().lower() in ['perfect','continue','yes','okay','empty','none','']:
            return {'human_analyst_feedback': None}

        return {'human_analyst_feedback': feedback}

    return {'human_analyst_feedback': None}


def generate_question(state: InterviewState):

    analyst = state['analyst']

    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    messages = state['messages']

    system_message = question_instructions.format(
        goals=analyst.persona
    )

    question = llm.invoke(
        [SystemMessage(content=system_message)] + messages
    )

    return {'messages': [question]}

def search_web(state: InterviewState):
    # query generator llm
    structured_llm = llm.with_structured_output(SearchQuery)
    # search instructions
    system_message = SystemMessage(content=search_instructions)
    search_query = structured_llm.invoke([system_message] + state['messages'])

    # search using the query generated
    search_engine = TavilySearch(max_results=3)
    data = search_engine.invoke({'query':search_query.search_query})
    search_docs = data.get('results',data)

    formatted_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {'context': [formatted_docs]}

def search_web2(state: InterviewState):
    # query generator llm
    structured_llm = llm.with_structured_output(SearchQuery)
    # search instructions
    system_message = SystemMessage(content=search_instructions)
    search_query = structured_llm.invoke([system_message] + state['messages'])

    # search using the query generated
    search_engine = TavilySearch(max_results=3)
    data = search_engine.invoke({'query':search_query.search_query})
    search_docs = data.get('results',data)

    formatted_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {'context': [formatted_docs]}


def generate_answer(state: InterviewState):


    analyst = state['analyst']
    messages = state['messages']
    context = state['context']

    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    system_message = answer_instructions.format(
        goals=analyst.persona,
        context=context
    )

    answer = llm.invoke(
        [SystemMessage(content=system_message)] + messages
    )
    answer.name = 'expert'

    return {'messages': [answer]}

def save_interview(state: InterviewState):
    messages = state['messages']
    # Convert sequence of messages to strings and concatenate them into one string.
    interview = get_buffer_string(messages)

    return {'interview': interview}

def write_section(state: InterviewState):
    interview = state['interview']
    context = state['context']
    analyst = state['analyst']

    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)

    system_message = SystemMessage(content=section_writer_instructions.format(focus = analyst.description))
    section = llama_llm.invoke([system_message] + [HumanMessage(content=f"Use this source to write your section: {context}")])

    return {'sections': [section.content]}


def write_report(state: ResearchGraphState):
    sections = state['sections']
    topic = state['topic']

    formatted_sections = "\n\n".join([f"{section}" for section in sections])

    system_message = report_writer_instructions.format(topic=topic, context=formatted_sections)
    report = llm.invoke([SystemMessage(content=system_message)] + [HumanMessage(content=f"Write a report based upon these memos.")])

    return {'content':report.content}


def write_introduction(state: ResearchGraphState):

    sections = state["sections"]
    topic = state["topic"]
    
    formatted_sections = "\n\n".join([f"{section}" for section in sections])
    
    instructions = SystemMessage(content = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_sections))    
    intro = llm.invoke([instructions]+[HumanMessage(content=f"Write the report introduction")]) 
    return {"introduction": intro.content}

def write_conclusion(state: ResearchGraphState):

    sections = state["sections"]
    topic = state["topic"]

    formatted_sections = "\n\n".join([f"{section}" for section in sections])
    
    instructions = SystemMessage(content = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_sections))    
    conclusion = llm.invoke([instructions]+[HumanMessage(content=f"Write the report conclusion")]) 
    return {"conclusion": conclusion.content}


def finalize_report(state: ResearchGraphState):

    content = state["content"]
    if content.startswith("## Insights"): content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    return {"final_report": final_report}


