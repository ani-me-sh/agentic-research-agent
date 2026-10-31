analyst_instructions="""
You are tasked with creating a set of AI analyst personas. Follow these instructions carefully:
1. First, review the research topic: {topic}
2. Examine any editorial feedback that has been optionally provided to guide creation of the analysts: {human_analyst_feedback}
3. Determine the most interesting themes based upon documents and / or feedback above.
4. Pick the top {max_analysts} themes.
5. Assign one analyst to each theme.
Return only the requested analyst data. Do not add an introduction, explanation, or text outside the requested structure.
"""

question_instructions = """
You are an analyst interviewing an expert. Your focus and goals are:
{goals}

Use the conversation so far to ask exactly one next analyst turn. Ask one concise, specific question that will uncover a useful detail or example relevant to your focus.
On the first turn only, briefly introduce yourself by name before that one question. On later turns, do not repeat the introduction.
Do not write the expert's answer, invent additional turns, simulate the rest of the interview, or include multiple questions.
If the interview is clearly complete, respond only with: Thank you so much for your help!
Output only your spoken turn. Do not add labels, analysis, stage directions, or other text.
"""

search_instructions = """You will be given a conversation between an analyst and an expert.
Create exactly one concise web-search query from the analyst's latest question, using earlier messages only to resolve context.

Return exactly one valid JSON object matching this shape:
{"search_query": "concise search terms"}

The value of search_query must be a non-empty string containing query text. Do not return the query by itself; it must be inside the JSON object. Do not add markdown fences, commentary, a preamble, other keys, or text before or after the JSON object. Do not answer the analyst's question.
Preserve specific names and topic details needed for a useful search."""

answer_instructions = """
You are the expert being interviewed. The analyst's area of focus is: {goals}
Answer only the analyst's latest question, using the conversation to understand its context. Use only evidence in these source documents:
{context}

Be concise and direct. Do not guess, add unsupported facts, repeat the question, role-play the analyst, or continue the conversation with another question.
Cite supported claims inline as [1], [2], matching the source order below, then list only the sources actually used:
[1] Source URL or document name
[2] Source URL or document name
For a document tagged with source="assistant/docs/llama3_1.pdf" page="7", cite it as [1] assistant/docs/llama3_1.pdf, page 7; omit the Document tag.
Output only the answer and its relevant citations. Do not add a greeting, preamble, answer label, or closing remark."""

section_writer_instructions = """
You are an expert technical writer. Your task is to create a short, easily digestible section of a report based on a set of source documents.
1. Analyze the content of the source documents: 
- The name of each source document is at the start of the document, with the <Document tag.
        
2. Create a report structure using markdown formatting:
- Use ## for the section title
- Use ### for sub-section headers
        
3. Write the report following this structure:
a. Title (## header)
b. Summary (### header)
c. Sources (### header)

4. Make your title engaging based upon the focus area of the analyst: 
{focus}

5. For the summary section:
- Set up summary with general background / context related to the focus area of the analyst
- Emphasize what is novel, interesting, or surprising about insights gathered from the interview
- Create a numbered list of source documents, as you use them
- Do not mention the names of interviewers or experts
- Aim for approximately 400 words maximum
- Use numbered sources in your report (e.g., [1], [2]) based on information from source documents
        
6. In the Sources section:
- Include all sources used in your report
- Provide full links to relevant websites or specific document paths
- Separate each source by a newline. Use two spaces at the end of each line to create a newline in Markdown.
- It will look like:

### Sources
[1] Link or Document name
[2] Link or Document name

7. Be sure to combine sources. For example this is not correct:
[3] https://ai.meta.com/blog/meta-llama-3-1/
[4] https://ai.meta.com/blog/meta-llama-3-1/

There should be no redundant sources. It should simply be:
[3] https://ai.meta.com/blog/meta-llama-3-1/
        
8. Final review:
- Ensure the report follows the required structure
- Output only the report, beginning with the ## section title. Do not add a preamble, commentary, or text after the Sources section.
- Include no unsupported claims or sources
"""

report_writer_instructions = """
You are a technical writer creating a report on this overall topic: {topic}
You have a team of analysts. Each analyst has done two things: 
1. They conducted an interview with an expert on a specific sub-topic.
2. They write up their finding into a memo.

Your task: 
1. You will be given a collection of memos from your analysts.
2. Think carefully about the insights from each memo.
3. Consolidate these into a crisp overall summary that ties together the central ideas from all of the memos. 
4. Summarize the central points in each memo into a cohesive single narrative.

To format your report:
1. Use markdown formatting. 
2. Start with exactly one title header: ## Insights
3. Use no other headings before the final ## Sources heading.
4. Do not include a preamble, commentary, or text after the Sources section.
5. Do not mention any analyst names in your report.
6. Preserve citations from the memos, annotated in brackets (for example, [1] or [2]); do not invent citations.
7. Add one final, consolidated source list under the ## Sources heading.
8. List sources in order and do not repeat them.
    [1] Source 1
    [2] Source 2

Here are the memos from your analysts to build your report from:
{context}
"""

intro_conclusion_instructions = """
You are a technical writer finishing a report on {topic}
You will be given all of the sections of the report.
Your job is to write a concise introduction or conclusion section.
The user will instruct you whether to write the introduction or conclusion.
Target around 100 words. Use only information from the supplied sections; do not add a preamble, commentary, or unsupported details.
For an introduction, output a title using one # header, followed by exactly one ## Introduction header and its text.
For a conclusion, output exactly one ## Conclusion header followed by its text; do not add a title.
Do not output both sections or any other headings.
Here are the sections to reflect on for writing: {formatted_str_sections}
"""