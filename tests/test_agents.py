import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.profile_agent import ProfileAgent
from agents.planner_agent import PlanningAgent

class TestAgents(unittest.TestCase):
    def test_profile_agent_structure(self):
        agent = ProfileAgent()
        self.assertIsNotNone(agent)
        # Add more tests based on actual implementation

    def test_planner_agent_structure(self):
        agent = PlanningAgent()
        self.assertIsNotNone(agent)

if __name__ == '__main__':
    unittest.main()
