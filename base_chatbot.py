import re
from json_loader import load_problem
from model_processor import HuggingFaceModelProcessor 

PROBLEM_PATH = "D:/ML/Project/BOT/DATA/Problems"
EDITORIAL_PATH = "D:/ML/Project/BOT/DATA/Editorials"

class ProblemChatbot:
    def __init__(self):
        self.model = HuggingFaceModelProcessor()  
        self.current_problem = None
        self.problem_data = None

    def _extract_problem_id(self, text):
        """Extract problem ID with flexible formatting"""
        match = re.search(r'(\d{4}[A-Za-z])', text, re.IGNORECASE)
        return match.group(1).upper() if match else None
    
    def _load_problem(self, problem_id):
        """Load problem data with validation"""
        data = load_problem(problem_id, PROBLEM_PATH, EDITORIAL_PATH)
        if not data:
            raise ValueError(f"No data found for problem {problem_id}")
        return data
    
    def _build_context(self):
        """Build comprehensive problem context"""
        if not self.current_problem or not self.problem_data:
            return None
        
        return (
            f"Problem {self.current_problem}: {self.problem_data.get('title', 'Untitled')}\n"
            f"Statement: {self.problem_data.get('statement', '')}\n"
            f"Input Specification: {self.problem_data.get('input', '')}\n"
            f"Output Specification: {self.problem_data.get('output', '')}\n"
            f"Hint: {self.problem_data.get('hint', 'None provided')}\n"
            f"Solution Approach: {self.problem_data.get('solution', 'None provided')}"
        )
    
    def respond(self, user_input):
        """Handle user input with hybrid approach"""
        user_input = user_input.strip()

        if any(greet in user_input.lower() for greet in ["hi", "hello", "hey"]):
            return "Hello! I'm your competitive programming assistant. Please provide a problem ID (e.g., 2093I) to get started."

        problem_id = self._extract_problem_id(user_input)
        if problem_id:
            try:
                self.current_problem = problem_id
                self.problem_data = self._load_problem(problem_id)
                return f"Loaded problem {problem_id}. You can ask about:\n- The problem statement\n- Input/output specifications\n- Solution approach"
            except ValueError as e:
                return str(e)
        
        if not self.current_problem:
            return "Please first specify a problem ID (e.g., 2093I)."
        
        context = self._build_context()
        
        if "hint" in user_input.lower():
            prompt = (
                f"You are a competitive programming assistant. Provide a helpful hint for problem {self.current_problem} "
                f"without giving away the full solution. Problem details:\n{context}"
            )
        elif "solution" in user_input.lower() or "solve" in user_input.lower():
            prompt = (
                f"You are a competitive programming assistant. Explain the solution approach for problem {self.current_problem} "
                f"in a step-by-step manner. Include any important insights or algorithms needed. "
                f"Problem details:\n{context}"
            )
        elif "explain" in user_input.lower() or "how" in user_input.lower():
            prompt = (
                f"You are a competitive programming assistant. Explain how to approach solving problem {self.current_problem} "
                f"in simple terms suitable for a beginner. Problem details:\n{context}"
            )
        else:
            
            prompt = (
                f"You are a competitive programming assistant. Answer this question about problem {self.current_problem}: "
                f"{user_input}\n\nProblem details:\n{context}"
            )
        
        return self.model.generate_response(prompt)