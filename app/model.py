from typing import List, Tuple, Dict

from app.data import MongoDB


class MatcherSortSearch:
    """ Callable matching class implementing sorted search algorithm """
    db = MongoDB()

    def __call__(self, n_matches: int, profile_id: str) -> List[str]:
        """ Return a list of profile_id for matched mentors """
        mentee = self.db.first("Mentees", {"profile_id": profile_id})

        def sort_mentors(mentor: Dict) -> Tuple:
            return (
                mentee["pair_programming"] != mentor["pair_programming"],
                mentee["job_help"] != mentor["job_help"],
                not mentor["industry_knowledge"],
            )

        results = sorted(
            self.db.read("Mentors", {
                "tech_stack": mentee["tech_stack"],
                "is_active": True,
                "accepting_new_mentees": True,
                "validate_status": 'approved'
            }),
            key=sort_mentors,
        )[:n_matches]
        return [mentor["profile_id"] for mentor in results]
