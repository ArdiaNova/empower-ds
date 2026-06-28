    # ruff: noqa
    # Copyright 2026 Google LLC
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #     https://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.    

import datetime
from zoneinfo import ZoneInfo   
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import LongRunningFunctionTool, FunctionTool, AgentTool
from google.genai import types
import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


def request_user_input(message: str) -> dict:
    """Request additional input from the user.

    Use this tool when you need more information from the user to complete a task.
    Calling this tool will pause execution until the user responds.

    Args:
        message: The question or clarification request to show the user.
    """
    return {"status": "pending", "message": message}


# Define sub-agents
companion_agent = Agent(
    name="companion_agent",
    model=Gemini(model="gemini-flash-latest", retry_options=types.HttpRetryOptions(attempts=3)),
    description="An agent for individuals with Down Syndrome, focusing on visual routines and AAC-style communication.",
    instruction="You are a supportive companion agent for individuals with Down Syndrome. Use visual aids and simple language.",
    tools=[],  # Tools will be added here for specific skills later
)

progress_mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python3",
            args=["mcp_server.py"],
            cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "progress_analyst"),
        ),
        timeout=10.0,
    ),
)

progress_agent = Agent(
    name="progress_agent",
    model=Gemini(model="gemini-flash-latest", retry_options=types.HttpRetryOptions(attempts=3)),
    description="An agent for parents, tracking milestones, providing summaries, and managing consent.",
    instruction=(
        "You are a progress analyst agent for parents. Use your tools to fetch "
        "real benchmark and milestone data -- never simulate or fabricate "
        "verification steps or data. When asked how a child is progressing, "
        "call get_milestones to retrieve real saved records before answering. "
        "If there are no saved records, say so honestly rather than inventing one."
    ),
    tools=[progress_mcp_toolset],
)

coaching_agent = Agent(
    name="coaching_agent",
    model=Gemini(model="gemini-flash-latest", retry_options=types.HttpRetryOptions(attempts=3)),
    description="An agent for trainers/therapists, assisting with activity planning and session notes.",
    instruction="You are a coaching specialist agent for trainers and therapists. Help plan activities and record session notes efficiently.",
    tools=[],  # Tools will be added here for specific skills later
)

# Wrap each sub-agent as a tool the orchestrator can call directly.
companion_agent_tool = AgentTool(agent=companion_agent)
progress_agent_tool = AgentTool(agent=progress_agent)
coaching_agent_tool = AgentTool(agent=coaching_agent)


root_agent = Agent(
    name="EmpowerDS_Orchestrator",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Orchestrates interactions for individuals with Down Syndrome, parents, and trainers/therapists.",
    instruction=(
        "You are the EmpowerDS Orchestrator. Your primary job is to route each "
        "interaction to the correct specialized sub-agent based on the authenticated "
        "user's role. Never let one agent silently do another's job.\n\n"
        "If you do not know the user's role yet, use request_user_input to ask "
        "whether they are a 'DS_individual', 'Parent', or 'Trainer_Therapist'.\n\n"
        "Once you know the role, call the matching tool to get the real response:\n"
        "- DS_individual -> call companion_agent\n"
        "- Parent -> call progress_agent\n"
        "- Trainer_Therapist -> call coaching_agent\n\n"
        "Always relay the sub-agent's actual response back to the user as your "
        "final answer. Do not just announce that you are routing -- give the "
        "user the real answer from the specialist."
    ),
    tools=[
        companion_agent_tool,
        progress_agent_tool,
        coaching_agent_tool,
        LongRunningFunctionTool(func=request_user_input),
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)