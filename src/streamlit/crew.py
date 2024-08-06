from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from utils import PropertyDetails, SearchResults, get_api_key

import streamlit as st
import os

@CrewBase
class PropertyHunterCrew():
    def __init__(self):
        self.agents_config = "config/agents.yaml"
        self.tasks_config = "config/tasks.yaml"

        # Initialize the tools
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        os.environ["SERPER_API_KEY"] = get_api_key("SERPER_API_KEY")
        os.environ["GROQ_API_TOKEN"] = get_api_key("GROQ_API_TOKEN")
        os.environ["OPENAI_API_KEY"] = get_api_key("OPENAI_API_KEY")

    def llm(self):
        llm = ChatGroq(
            api_key=os.environ["GROQ_API_TOKEN"],
            model="llama3-groq-70b-8192-tool-use-preview",
            max_tokens=1000,
            max_retries=3,
        )

        # llm = ChatOpenAI(
        #     api_key=os.environ["OPENAI_API_KEY"],
        #     model="gpt-3.5-turbo",
        # )

        return llm

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
            allow_delegation=False,
            tools=[self.search_tool],
            verbose=True,
            llm=self.llm(),
        )

    @agent
    def real_estate_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["real_estate_agent"],
            allow_delegation=False,
            tools=[self.scrape_tool],
            verbose=True,
            llm=self.llm(),
        )

    @agent
    def data_wrangler(self) -> Agent:
        return Agent(
            config=self.agents_config["data_wrangler"],
            allow_delegation=False,
            verbose=True,
            llm=self.llm(),
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.research_agent()
        )

    @task
    def search_task(self) -> Task:
        return Task(
            config=self.tasks_config["search_task"],
            # Need some kind of way to store search results, perhaps as JSON with a for loop over each relevant search result
            # output_json=SearchResults(),
            # output_file="search_results.json",  
            agent=self.real_estate_agent()
        )
    
    @task
    def aggregate_task(self) -> Task:
        return Task(
            config=self.tasks_config["aggregate_task"],
            # output_file="short_list.md",  # Outputs the final results as a text file, could possible email this
            agent=self.data_wrangler()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )
