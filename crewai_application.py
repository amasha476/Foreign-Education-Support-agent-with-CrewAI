from crewai import Agent, Task, Crew, LLM
from datetime import datetime
from dotenv import load_dotenv
import requests
import os
from tavily import TavilyClient
from crewai.tools import tool

dotenv_path = "education_support_agent/.env"  
load_dotenv(dotenv_path=dotenv_path)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool("tavily_search_tool")
def tavily_search_tool(query: str):
    """
    Search for real-time information such as  flights,
    weather, and currency using Tavily Search API.
    """
    result = tavily.search(query=query, max_results=1)
    return result


def run_study_planner(country,level, stream, current_time=None):

    if current_time is None:
        current_time = datetime.now()

    ## Initialize LLMs
    llm1 = LLM(
        model="groq/llama-3.1-8b-instant",
        temperature=0.5,
        max_completion_tokens=400,
        stream=False,
    )


    llm2 = LLM(
        model="groq/llama-3.3-70b-versatile",
        temperature=0.6,
        max_completion_tokens=400,
        stream=False,
    )

    ## Agent 1 — University Finder
    uni_agent = Agent(
        role="University Finder",
        goal=(
            f"Return a list of top 10 private universities and the offered program details in {country} for foreign students that provides degree programs for the level {level} in {stream}. "
            "Do not include prices."
        ),
        backstory=(
            "You provide accurate private university names for foreign students with the location and program details (Specializations / Majors,Program Duration,Reputation / Ranking, University ranking)."  
            "Do NOT include thoughts, reasoning steps, or explanations."
        ),
        llm=llm1,
        verbose=False
    )

    ## Agent 2 — Financial Planner Agent
    financial_agent = Agent(
        role="Financial Planner",
        goal=(
            f"Return the budget free monthly Living Expenses like Rent, food, transport  in LKR for {country} at {current_time.strftime('%Y-%m-%d %H:%M:%S')} for a single student"
        ),
        backstory=(
            "You fetch the rough living expenses for a month for a student for Rent, food and transport seperatly.  Do NOT include thoughts, reasoning steps, or explanations. "
        ),
        llm=llm2,
        verbose=False
    )

    ## Agent 3 — Airlines Finder
    airlines_agent = Agent(
        role="Airlines Expert",
        goal=(
            f"Return a list of 10 frequently travle airlines that operate flights to {country} as of {current_time.strftime('%Y-%m-%d %H:%M:%S')}."
        ),
        backstory=(
            "You provide airline names only. No flight prices, schedules, or summaries.  Do NOT include thoughts, reasoning steps, or explanations. "
        ),
        # tools=[tavily_search_tool],
        llm=llm1,
        verbose=False
    )

    ## Agent 4 — Local lifestyle Finder
    lifestyle_agent = Agent(
        role="Lifestyle Expert",
        goal=(
            f"Return a small description on Cultural Fit like Language, lifestyle, student community, special occasions in {country}."
        ),
        backstory=(
            "You provide a description on lifestyle of the country and special events.Do NOT include thoughts, reasoning steps, or explanations. "
        ),
        llm=llm2,
        verbose=False
    )

    ## Agent 5 — Currency & Exchange Rate Checker
    currency_agent = Agent(
        role="Currency Expert",
        goal=(
            f"Return the list of current exchange rate against USD, GBP, EURO, YEN of {country}"
        ),
        backstory=(
            "Provide only the currency name/code and exchange rate number. Do NOT include thoughts, reasoning steps, or explanations. "
        ),
        # tools=[tavily_search_tool],
        llm=llm1,
        verbose=False
    )

       ## Tasks
    uni_task = Task(
        description=f"List private universities in {country} for foreign students that provides degree programs for the level {level} in {stream}.",
        expected_output="Markdown list of accurate private university names for foreign students with the location and program details (Specializations / Majors,Program Duration,Reputation / Ranking, University ranking). Do not include thoughts or reasoning.Do not include text 'Final Answer' or 'Thought: I now can give a great answer' text.",
        agent=uni_agent,
        output_file="output/Universities.md"
    )

    financial_task = Task(
        description=f"Return the rough living expenses for a month for a university student for Rent, food and transport seperatly in {country} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}.",
        expected_output="Return the answer in the following **structured Markdown format without using tables**:\n\n"
        "##  Estimated Monthly Expenses\n\n\n"
        "**Rent:** <rent_range>\n\n"
        "**Food:** <food_range>\n\n"
        "**Transport:** <transport_range>\n\n\n"
        "**Notes:**\n"
        "- Rent depends on city and accommodation type.\n"
        "- Food costs vary based on personal diet and lifestyle.\n"
        "- Transport costs include public transport and occasional taxis.\n\n"
        "Replace <rent_range>, <food_range>, <transport_range> with actual values. "
        "Do not include any reasoning or extra text.",
        agent=financial_agent,
        output_file="output/Financial.md"
    )

    airlines_task = Task(
        description=f"List airlines flying to {country} as of {current_time.strftime('%Y-%m-%d %H:%M:%S')}.",
        expected_output="Return the answer in the following **structured Markdown format without using tables**:\n\n"
        "##  Airlines Flying to {country}\n\n"
        "- <Airline_1>\n"
        "- <Airline_2>\n"
        "- <Airline_3>\n"
        "- <Airline_4>\n"
        "- <Airline_5>\n\n"
        "**Notes:**\n"
        "- This list includes major airlines currently operating flights to {country}.\n"
        "- Airline schedules may vary; always check the official airline website for updates.\n\n"
        "Do not include any reasoning or extra text. Only return the structured output.",
        agent=airlines_agent,
        output_file="output/Airlines.md"
    )

    lifestyle_task = Task(
        description=f"A small description on Cultural Fit like Language, lifestyle, student community, special occasions in {country}.",
        expected_output="Return the answer in the following **structured Markdown format without using tables**:\n\n"
        "##  Cultural Fit in {country}\n\n"
        "**Language:**\n"
        "- <Primary language(s)>\n"
        "- <Secondary language(s) if any>\n\n"
        "**Lifestyle:**\n"
        "- <Typical daily routines or social norms>\n"
        "- <Student life and community culture>\n"
        "- <Cost of living habits, leisure activities>\n\n"
        "**Special Occasions & Festivals:**\n"
        "- <Major national holidays and celebrations>\n"
        "- <Cultural or student-centered events>\n\n"
        "Do not include any reasoning or extra text. Only return the structured output.",
        agent=lifestyle_agent,
        output_file="output/Lifestyle.md"
    )

    currency_task = Task(
        description=f"Provide the currency and exchange rate of {country} against USD, GBP, EURO, INR",
        expected_output="Return the answer in the following **structured Markdown format without using tables**:\n\n"
        "##  Currency Exchange Rates\n\n"
        "**Currency:** USD\n"
        "**Rate:** 1 <country_currency> = <usd_rate>\n\n"
        "**Currency:** GBP\n"
        "**Rate:** 1 <country_currency> = <gbp_rate>\n\n"
        "**Currency:** EURO\n"
        "**Rate:** 1 <country_currency> = <euro_rate>\n\n"
        "**Currency:** INR\n"
        "**Rate:** 1 <country_currency> = <inr_rate>\n\n"
        "**Notes:**\n"
        "- Rates are approximate and may fluctuate daily.\n\n"
        "Do not include any reasoning or extra text. Only return the structured output.",
        agent=currency_agent,
        output_file="output/Currency.md"
    )


    ## Crew
    crew = Crew(
        agents=[uni_agent, financial_agent, lifestyle_agent, airlines_agent, currency_agent],
        tasks=[uni_task, financial_task, lifestyle_task, airlines_task, currency_task],
        verbose=False
    )

    inputs = {"country": country, "level" :level, "stream":stream, "current_time": current_time.strftime('%Y-%m-%d %H:%M:%S')}
    crew.kickoff(inputs=inputs)

    ## Read reports
    reports = {}
    for file in ["output/Universities.md", "output/Financial.md", "output/Lifestyle.md",
    "output/Airlines.md",  "output/Currency.md"]:
        with open(file, "r") as f:
            reports[file.split('/')[-1]] = f.read()

    return reports