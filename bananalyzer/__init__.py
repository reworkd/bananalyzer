# Separate banana-lyzer args from pytest args
# Look for an instance of Banana-lyzer in the current directory
# If it doesn't exist, error
import argparse
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

from bananalyzer.data.examples import examples
from bananalyzer.data.schemas import GoalType
from bananalyzer.runner.agent_runner import AgentRunner
from bananalyzer.runner.runner import generate_test, run_tests
from bananalyzer.schema import Args


def print_intro() -> None:
    # https://www.asciiart.eu/food-and-drinks/bananas
    print(
        """//\ 
V  \ 
 \  \_
  \,'.`-.
   |\ `. `.       
   ( \  `. `-.                        _,.-:\ 
    \ \   `.  `-._             __..--' ,-';/
     \ `.   `-.   `-..___..---'   _.--' ,'/
      `. `.    `-._        __..--'    ,' /
        `. `-_     ``--..''       _.-' ,'
          `-_ `-.___        __,--'   ,'
             `-.__  `----'''    __.-'
                  `--..____..--'
"""
    )
    print("Bananalyzing... 🍌")


def parse_args() -> Args:
    file_name = "bananalyzer-agent.py"
    parser = argparse.ArgumentParser(
        description=f"Run the agent inside a bananalyzer agent definition file against the benchmark",
    )
    parser.add_argument("path", type=str, help=f"Path to the {file_name} file")
    parser.add_argument(
        "--headless", action="store_true", help=f"Whether to run headless or not"
    )
    parser.add_argument(
        "-i",
        "--intent",
        type=str,
        default=None,
        help="Filter tests by a particular intent",
    )
    parser.add_argument(
        "-id",
        "--id",
        type=str,
        default=None,
        help="Filter tests by id",
    )

    args = parser.parse_args()

    file_name = os.path.basename(args.path)
    if file_name != file_name:
        raise RuntimeError(f"The provided file name must be {file_name}")

    return Args(
        path=args.path,
        headless=args.headless,
        intent=args.intent,
        id=args.id,
    )


def load_agent_from_path(file_path: str) -> Any:
    path = Path(file_path)
    module_name = path.stem

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from path {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return getattr(module, "agent")


def validate_agent_instance_available(agent: Any) -> None:
    # Ensures there is some "agent" variable in the global context
    # This is a bit hacky, but it's the best way to ensure the agent is available
    # without actually running the file
    if not isinstance(agent, AgentRunner):
        raise TypeError("User defined agent is is not an instance of AgentRunner")


def main() -> int:
    """
    Load the agent from the provided path and run it against the benchmark

    Note that pytest creates a new global context when running tests.
    Because of this, we first load the agent and validate that it is of the correct type here.
    Then we pass the path to the agent runner and let it load it within the pytest context.
    Note your AgentRunner must be concurrency safe.
    """
    print_intro()

    # Load the agent
    args = parse_args()
    agent = load_agent_from_path(args.path)
    validate_agent_instance_available(agent)

    # Filter examples based on args
    filtered_examples = examples[:]
    if args.id:
        filtered_examples = [
            example for example in filtered_examples if example.id == args.id
        ]
    if args.intent:
        filtered_examples = [
            example for example in filtered_examples if example.type == args.intent
        ]

    # Test we actually have tests to run
    if len(filtered_examples) == 0:
        print()
        print("=======================================================================")
        print("🍌 No tests to run. Please ensure your filter parameters are correct 🍌")
        print("=======================================================================")
        return 0

    # Load the desired tests
    tests = [generate_test(example, args.headless) for example in filtered_examples]

    # Run the tests
    return run_tests(tests, args.path)


if __name__ == "__main__":
    main()
