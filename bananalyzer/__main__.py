# Separate banana-lyzer args from pytest args
# Look for an instance of Banana-lyzer in the current directory
# If it doesn't exist, error
import argparse
import ast
import importlib.util
import os
import sys
from pathlib import Path
from typing import List

from bananalyzer import AgentRunner, examples
from bananalyzer.runner.runner import TestGenerator, run_tests
from bananalyzer.schema import AgentRunnerClass, Args, PytestArgs


def print_intro() -> None:
    # https://www.asciiart.eu/food-and-drinks/bananas
    print(
        r"""
//\
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
        description=f"Run the agent inside a bananalyzer agent definition file "
        f"against the benchmark",
    )
    parser.add_argument("path", type=str, help=f"Path to the {file_name} file")
    parser.add_argument(
        "--headless", action="store_true", help=f"Whether to run headless or not"
    )
    parser.add_argument(
        "-s",
        "--s",
        action="store_true",
        help="Shortcut for --capture=no in pytest. Will print stdout and stderr",
    )
    parser.add_argument(
        "-id",
        "--id",
        type=str,
        default=None,
        help="Filter tests by id",
    )
    parser.add_argument(
        "-i",
        "--intent",
        type=str,
        default=None,
        help="Filter tests by a particular intent",
    )
    parser.add_argument(
        "-d",
        "--domain",
        type=str,
        default=None,
        help="Filter tests by a particular domain",
    )
    parser.add_argument(
        "-n",
        "--n",
        type=str,
        default=None,
        help="Number of test workers to use. The default is 1",
    )
    parser.add_argument(
        "-skip",
        "--skip",
        type=lambda s: s.split(","),
        default=[],
        help="A list of ids to skip tests on, separated by commas",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Will decrease the verbosity of pytest",
    )
    parser.add_argument(
        "--turbo",
        action="store_true",
        help="Will run tests in a single browser instance. This is faster but less "
        "reliable",
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
        domain=args.domain,
        skip=args.skip,
        turbo=args.turbo,
        pytest_args=PytestArgs(
            s=args.s,
            n=args.n,
            q=args.quiet,
        ),
    )


def find_agents(file_path: Path) -> List[AgentRunnerClass]:
    print(f"Finding agents in {file_path}")
    with open(file_path, "r") as source:
        node = ast.parse(source.read())

    runners: List[AgentRunnerClass] = []
    for clazz in [n for n in node.body if isinstance(n, ast.ClassDef)]:
        if "AgentRunner" in [getattr(base, "id", "") for base in clazz.bases]:
            runners.append(
                AgentRunnerClass(
                    class_name=clazz.name,
                    class_path=str(file_path),
                )
            )

    return runners


def load_agent_from_path(path: Path) -> AgentRunnerClass:
    if path.is_dir():
        files = [p for p in path.glob("**/*.py") if "venv" not in p.parts]
    else:
        files = [path]

    runners: List[AgentRunnerClass] = []
    for file in files:
        runners.extend(find_agents(file))

    if len(runners) == 0:
        raise RuntimeError(f"Could not find any agent runners in {path}")

    if len(runners) > 1:
        raise RuntimeError(f"Found multiple agent runners in {path}")

    runner = runners[0]
    runner_file = Path(runner.class_path)
    module_name = path.stem

    spec = importlib.util.spec_from_file_location(module_name, runner_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from path {runner_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    agent = getattr(module, runner.class_name)()
    if not isinstance(agent, AgentRunner):
        raise TypeError("User defined agent is is not an instance of AgentRunner")

    return runner


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
    agent = load_agent_from_path(Path(args.path))

    print(f"Loaded agent {agent.class_name} from {agent.class_name}")

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
    if args.domain:
        filtered_examples = [
            example for example in filtered_examples if example.domain == args.domain
        ]
    if args.skip:
        filtered_examples = [
            example for example in filtered_examples if example.id not in args.skip
        ]

    # Test we actually have tests to run
    if len(filtered_examples) == 0:
        print()
        print("=======================================================================")
        print("🍌 No tests to run. Please ensure your filter parameters are correct 🍌")
        print("=======================================================================")
        return 0

    # Load the desired tests
    generator = TestGenerator()
    tests = [generator.generate_test(example) for example in filtered_examples]

    # Run the tests
    return run_tests(tests, agent, args.pytest_args, args.headless, args.turbo)


if __name__ == "__main__":
    main()