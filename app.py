import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults



if  'defalt_temperature' not in st.session_state:
    st.session_state['default_temperature'] = 0.5

# Model and Agent tools
llm = ChatGroq(
    api_key=st.secrets["GROQ_API_KEY"],
    temperature=st.session_state['default_temperature']
    )

search = TavilySearchResults(max_results=2)
parser = StrOutputParser()
# tools = [search] # add tools to the list

def change_temperature():
    st.session_state['default_temperature'] = st.session_state.temperature
    return

# Page Header
st.title("Assistant Agent")
st.markdown("Assistant Agent Powered by Groq.")

st.sidebar.title("AI Assistant Settings")
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value = 1.0, value=0.01, key = 'temperature', on_change=change_temperature)



# Data collection/inputs
with st.form("company_info", clear_on_submit=True):

    
    product_name = st.text_input("**Product Name** (What product are you selling?):")
    
    company_url = st.text_input(
        "**Company URL** (The URL of the company you are targeting):"
    )
    
    product_category = st.text_input(
        "**Product Category** (e.g., 'Data Warehousing' or 'Cloud Data Platform')"
    )
    
    competitors_url = st.text_input("**Competitors URL** (ex. www.apple.com):")
    
    value_proposition = st.text_area(
        "**Value Proposition** (A sentence summarizing the product’s value):"
    )
    
    target_customer = st.text_input(
        "**Target Customer** (Name of the person you are trying to sell to.) :"
    )

    # For the llm insights result
    company_insights = ""

    # Data process
    if st.form_submit_button("Generate Insights"):
        if product_name and company_url:
            st.spinner("Processing...")

            # Use search tool to get Company Information
            company_information = search.invoke(company_url)
            print(company_information)

            # TODO: Create prompt <=================
            prompt = """
            You are an experienced customer service representative helping potential 
            customers understand the unique value of our product. Your goal is to 
            increase conversion rates by effectively communicating our competitive 
            advantages while maintaining authenticity and addressing customer needs.
            
            
            
            company_info: {company_information}
            product_name: {product_name}
            competitors_url: {competitors_url}
            product_category: {product_category}
            value_proposition: {value_proposition}
            target_customer: {target_customer}
            
            Generate a report including the following:
            1.  Insight's into the company's strategy, activities and priorities.
            2.  The competitora presence and relationship with the company.
            3.  Key market trends and customer needs.leadership information and thier roles in both the company and the competitor
            4.  Any product insights from public document or reports that show the competitive advantage of the company over the competitor
            5.  Relevant leaders and thair roles.
            6.  Pros and cons of launching the product into a new market.
            7.  Any productAny refernces .links to articles, press releases or other source used to support analysis
            
            Based on the report, create a marketing email template to target_customer.  Emphasize the benefits of the product and the company's strengths. 
            # Include optional information if provided. 
            """

            # Prompt Template
            prompt_template = ChatPromptTemplate([("system", prompt)])

            # Chain
            chain = prompt_template | llm | parser

            # Result/Insights
            company_insights = chain.invoke(
                {
                    "company_information": company_information,
                    "product_name": product_name,
                    "competitors_url": competitors_url,
                    "product_category": product_category,
                    "value_proposition": value_proposition,
                    "target_customer": target_customer,
                
                }
            )

st.markdown(company_insights)