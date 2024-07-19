from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
import streamlit as st
import os

@CrewBase
class PropertyHunterCrew():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def llm(self):
        llm = ChatGroq(
            api_key=os.environ["GROQ_API_TOKEN"],
            model="llama3-70b-8192"
        )

        return llm

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config["planner"],
            allow_delegation=False,
            verbose=True,
            llm=self.llm()
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config["writer"],
            allow_delegation=False,
            verbose=True,
            llm=self.llm()
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
            allow_delegation=False,
            verbose=True,
            llm=self.llm()
        )

    @task
    def plan_task(self) -> Task:
        return Task(
            config=self.tasks_config["plan_task"],
            agent=self.planner(),
        )

    @task
    def write_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_task"],
            agent=self.writer(),
        )

    @task
    def edit_task(self) -> Task:
        return Task(
            config=self.tasks_config["edit_task"],
            agent=self.editor(),
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