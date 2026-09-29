class UserProfile:
    def __init__(
        self,
        skills: list[str],
        interests: list[str],
        education: str,
        experience_level: str,
        preferred_location: str
    ):
        self.skills = skills
        self.interests = interests
        self.education = education
        self.experience_level = experience_level
        self.preferred_location = preferred_location

    def to_text(self) -> str:
        skills_text = ", ".join(self.skills)
        interests_text = ", ".join(self.interests)

        profile_text = f"""
Skills: {skills_text}

Interests: {interests_text}

Education: {self.education}

Experience Level: {self.experience_level}

Preferred Location: {self.preferred_location}
"""

        return profile_text.strip()

    def to_retrieval_query(self) -> str:
        skills_text = ", ".join(self.skills)
        interests_text = ", ".join(self.interests)

        retrieval_query = f"""
Candidate skills:
{skills_text}

Relevant technical skills:
{skills_text}

Career interests:
{interests_text}

Education background:
{self.education}

Experience level:
{self.experience_level}

Preferred location:
{self.preferred_location}

Find job roles that strongly match the candidate's technical
skills and career interests.
"""

        return retrieval_query.strip()
