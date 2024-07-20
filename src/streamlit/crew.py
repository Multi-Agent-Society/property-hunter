from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel
from utils import get_serper_api_key 


import streamlit as st
import os

class PropertyDetails(BaseModel):
    location: str
    no_beds: int
    no_baths: int
    budget_high: int
    budget_low: int
    pets: str
    public_transit: bool
    move_in_date: str
    car_parking: bool
    other_ameneties: str
    # Will be filled with information relevant to making a decision but not explicitly mentioned by user
    extra_considerations: str    

class SearchResults(BaseModel):
    location: str
    no_beds: int
    no_baths: int
    budget_high: int
    budget_low: int
    pets: str
    public_transit: bool
    move_in_date: str
    car_parking: bool
    other_ameneties: str
    # Will be filled with information relevant to making a decision but not explicitly mentioned by user
    extra_considerations: str    

@CrewBase
class PropertyHunterCrew():
    def __init__(self):
        self.agents_config = "config/agents.yaml"
        self.tasks_config = "config/tasks.yaml"

        # Initialize the tools
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        os.environ["SERPER_API_KEY"] = get_serper_api_key() # Need to define this function 

    def llm(self):
        llm = ChatGroq(
            api_key=os.environ["GROQ_API_TOKEN"],
            model="llama3-70b-8192"
        )

        return llm

    @agent
    def proppy(self) -> Agent:
        return Agent(
            config=self.agents_config["proppy"],
            allow_delegation=False,
            verbose=True,
            llm=self.llm()
        )

    @agent
    def scrappy(self) -> Agent:
        return Agent(
            config=self.agents_config["scrappy"],
            allow_delegation=False,
            tools=[self.search_tool, self.scrape_tool],
            verbose=True,
            llm=self.llm()
        )

    @agent
    def closing_consultant(self) -> Agent:
        return Agent(
            config=self.agents_config["closing_consultant"],
            allow_delegation=False,
            verbose=True,
            llm=self.llm()
        )

    @task
    def gather_detailed_preferences(self) -> Task:
        return Task(
            config=self.tasks_config["gather_detailed_preferences"],
            # By setting human_input=True, the task will ask for human feedback (whether you like the results or not) before finalising it.
            # i.e., "Let me make sure I understand all of your preferences correctly before continuing..."
            human_input=True,
            output_json=PropertyDetails(),
            output_file="property_details.json",  
            agent=self.proppy()
        )
    
    @task
    def search_task(self) -> Task:
        return Task(
            config=self.tasks_config["search_task"],
            # Need some kind of way to store search results, perhaps as JSON with a for loop over each relevant search result
            output_json=SearchResults(),
            output_file="search_results.json",  
            agent=self.scrappy()
        )
    
    @task
    def presentation_task(self) -> Task:
        return Task(
            config=self.tasks_config["presentation_task"],
            output_file="short_list.md",  # Outputs the final results as a text file
            agent=self.closing_consultant()
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            # agents=[self.planner(), self.writer(), self.editor()],
            # tasks=[self.plan_task(), self.write_task(), self.edit_task()],
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2
        )