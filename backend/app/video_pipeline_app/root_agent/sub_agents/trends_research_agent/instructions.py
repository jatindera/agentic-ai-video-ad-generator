trends_query_creator_instructions = """

You will receive 
business information: {business_requirements_output}

Your task is to analyze all provided details—including the business profile, target audience, industry, brand tone, objectives, pain points, and visual preferences—and generate a **single one-line actionable search query** suitable for an automated workflow.

### **Requirements for the one-line query:**

- It must be **short, clear, and actionable**.
- It must start with an **action verb**, such as: *Search, Analyze, Generate, Discover, Identify, Create, Research, Summarize, Recommend*.
- It must be **directly aligned** with the business requirements (industry, audience, pain points, ad objective, platform, visuals).
- It must produce **marketing insights, creative ideas, or trend research** relevant to the business.
- **Do NOT repeat or summarize the JSON.** Only output the final one-liner.

### **Output Format:**

Return **only the one-line actionable search query**. No explanations. No additional text.


"""