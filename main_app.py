# autogen_setup.py
from autogen import AssistantAgent, UserProxyAgent, GroupChatManager, GroupChat
from tools import getYahooFinance, code_executor
from config import llm_config, config_list
from sys_messages import (manager_description, retrieval_description, analyst_description,
                          ml_engineer_description, predictor_description, reporter_description)
# ---------------------------------------


# ---------------------------------------
# Specify configuration
llm_config = llm_config
# -----------------------------------------
# Create agents
manager_agent = AssistantAgent(
    name="manager",
    system_message=manager_description,
    llm_config=llm_config
)

retrieval_agent = AssistantAgent(
    name="data_retriever",
    system_message=retrieval_description,
    llm_config=llm_config
)

data_analyst = AssistantAgent(
    name="data_analyst",
    system_message=analyst_description,
    llm_config=llm_config
)

ml_engineer = AssistantAgent(
    name="ML_Engineer",
    system_message=ml_engineer_description,
    llm_config=llm_config
)

predictor = AssistantAgent(
    name="Price_Predictor",
    system_message=predictor_description,
    llm_config=llm_config
)

reporter = AssistantAgent(
    name="report_writer",
    system_message=reporter_description,
    llm_config=llm_config
)

# ----------------------------------------
# Put the agents in a group chat
groupchat = GroupChat(
    agents=[manager_agent, retrieval_agent, data_analyst,
            ml_engineer, predictor, reporter],
    messages=[],
    max_round=50,  # Increased for complex workflow
    speaker_selection_method="round_robin",

)

# Update manager configuration
chat_manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list},
    system_message=manager_description
)

# ---------------------------------------
# Register the tool with the worker
manager_agent.register_function(
    function_map={
        "getYahooFinance": getYahooFinance,
        "code_executor": code_executor
    }
)

# ------------------------------------
# Start the conversation


def process_text_task(task_input):
    chat_manager.initiate_chat(
        chat_manager,
        message=f"Please handle this task: {task_input}",
        recipients=[retrieval_agent, data_analyst,
                    ml_engineer, predictor, reporter]
    )


if __name__ == "__main__":
    process_text_task(
        "Analyze trends and predict the next 10 days stock price for the Apple stock. Give me a comprehensive report at the end.")
