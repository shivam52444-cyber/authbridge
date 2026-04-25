from jd_analysis_chain import *




resume_prompt = PromptTemplate.from_template("""
You are an expert recruiter.

Return STRICT JSON:

{{
  "overall_score": number,
  "strengths": [],
  "gaps": [],
  "summary": "short summary",
  "recommendation": "shortlist/reject"
}}

JD:
{jd}

Resume:
{resume}
""")

resume_chain = resume_prompt | llm | StrOutputParser()


def score_resume(jd, resume):
    return resume_chain.invoke({
        "jd": jd,
        "resume": resume
    })
    

    
    
