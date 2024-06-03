from langchain.prompts import PromptTemplate

question_prompt_template = """
        You have been given a PDF. Generate a list of 15 questions based on the following text:
        {text}
        List of questions (inclosed in a iterable list []):
    """

question_prompt = PromptTemplate.from_template(question_prompt_template)

refine_template = (
    "Your job is to produce a list of 15 questions covering across the text.\n"
    "We have provided an existing question list up to a certain point: {existing_answer}\n"
    "We have the opportunity to refine the existing list."
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{text}\n"
    "------------\n"
    "Given the new context, refine the original list.\n"
    "If the context isn't useful, return the original question list.\n"
    "Do not generate more than 15 questions\n"
)
refine_prompt = PromptTemplate.from_template(refine_template)