# Separate banana-lyzer args from pytest args
# Look for an instance of Banana-lyzer in the current directory
# If it doesn't exist, error
import argparse
import ast
import importlib.util
import sys
from pathlib import Path
from typing import List
from urllib.parse import urlparse

from bananalyzer import AgentRunner
from bananalyzer.data.banana_seeds import download_mhtml
from bananalyzer.data.examples import (
    download_examples,
    get_examples_path,
    get_test_examples,
    get_training_examples,
)
from bananalyzer.runner.generator import PytestTestGenerator
from bananalyzer.runner.runner import run_tests
from bananalyzer.schema import AgentRunnerClass, Args, PytestArgs, XDistArgs


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
        description="Run the agent inside a bananalyzer agent definition file "
        "against the benchmark",
    )
    parser.add_argument(
        "path", type=str, nargs="?", default=None, help=f"Path to the {file_name} file"
    )
    parser.add_argument(
        "--headless", action="store_true", help="Whether to run headless or not"
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
        type=lambda s: s.replace("_", "-").split(","),
        default=None,
        help="Filter tests by id. "
        "Ids could be of shape a4c8292a_079c_4e49_bca1_cf7c9da205ec or a4c8292a-079c-4e49-bca1-cf7c9da205ec, "
        "and can be passed as a comma-separated list.",
    )
    parser.add_argument(
        "-tags",
        "--tags",
        type=lambda s: s.split(","),
        default=None,
        help="Filter tests by tag. Can be passed as a comma-separated list.",
    )
    parser.add_argument(
        "-d",
        "--domain",
        type=str,
        default=None,
        help="Filter tests by a particular URL domain",
    )
    parser.add_argument(
        "-i",
        "--intent",
        type=str,
        default=None,
        help="Filter tests by a particular intent",
    )
    parser.add_argument(
        "-c",
        "--category",
        type=str,
        default=None,
        help="Filter tests by a particular category",
    )
    parser.add_argument(
        "--subcategory",
        type=str,
        default=None,
        help="Filter tests by a particular subcategory",
    )
    parser.add_argument(
        "-n",
        "--n",
        type=str,
        default="logical",
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
        help="Will decrease the verbosity of pytest. By default we run with the `--v` pytest param.",
    )
    parser.add_argument(
        "--single_browser_instance",
        action="store_true",
        help="Run tests in a single browser instance as opposed to creating a browser "
        "instance per test. This is faster but less reliable as test contexts can "
        "occasionally bleed into each other, causing tests to fail",
    )
    parser.add_argument(
        "--type",
        type=str,
        default=None,
        help="Filter tests by a particular type",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Will re-download training and test examples",
    )
    parser.add_argument(
        "--examples_bucket",
        type=str,
        default=None,
        help="Download examples from the specified public S3 bucket",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Use test set examples instead of training set examples",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="The number of times to run an individual test. Won't work for detail pages",
    )
    parser.add_argument(
        "--junitxml",
        type=str,
        default=None,
        help="The path for the junitxml report file",
    )
    parser.add_argument(
        "--dist",
        type=str,
        default="loadscope",
        help="The distribution mode for pytest-xdist",
    )

    args = parser.parse_args()
    if args.download and not args.path:
        args.path = "DOWNLOAD_ONLY"

    if not args.path:
        print(
            f"Please provide the path to a {file_name} file. "
            f"Use the --help flag for more information."
        )
        exit(1)

    return Args(
        path=args.path,
        headless=args.headless,
        intent=args.intent,
        id=args.id,
        domain=args.domain,
        category=args.category,
        subcategory=args.subcategory,
        skip=args.skip,
        single_browser_instance=args.single_browser_instance,
        type=args.type,
        test=args.test,
        download=args.download,
        examples_bucket=args.examples_bucket,
        count=args.count,
        pytest_args=PytestArgs(
            s=args.s,
            q=args.quiet,
            xml=args.junitxml,
        ),
        xdist_args=XDistArgs(
            n=args.n,
            dist=args.dist,
        ),
        tags=args.tags,
    )


def find_agents(file_path: Path) -> List[AgentRunnerClass]:
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
    if args.download:
        print("##################################################")
        print("# Downloading examples, this may take a while... #")
        print("##################################################")
        download_examples(examples_bucket=args.examples_bucket)

        if args.path == "DOWNLOAD_ONLY":
            return 0

    agent = load_agent_from_path(Path(args.path))
    print(f"Loaded agent {agent.class_name} from {agent.class_name}")

    # Filter examples based on args
    examples = get_test_examples() if args.test else get_training_examples()

    filters = []
    if args.id:
        filters.append(lambda e: e.id in args.id if args.id else True)
    if args.tags:
        filters.append(lambda e: any(tag in e.tags for tag in args.tags or []))
    if args.intent:
        filters.append(lambda e: e.type == args.intent)
    if args.domain:
        filters.append(
            lambda e: ".".join(urlparse(e.url).netloc.split(".")[-2:]) == args.domain
        )
    if args.category:
        filters.append(lambda e: e.category == args.category)
    if args.skip:
        filters.append(lambda e: e.id not in args.skip)
    if args.type:
        filters.append(lambda e: e.type == args.type)
    if args.subcategory:
        filters.append(lambda e: e.subcategory == args.subcategory)

    # Test we actually have tests to run
    examples = [e for e in examples if all(f(e) for f in filters)]
    if len(examples) == 0:
        print()
        print("=======================================================================")
        print("🍌 No tests to run. Please ensure your filter parameters are correct 🍌")
        print("=======================================================================")
        return 0

    for example in examples:
        if example.mhtml_url is not None:
            mhtml_path = get_examples_path() / example.id / "index.mhtml"
            if not mhtml_path.exists():
                mhtml_str = download_mhtml(example.mhtml_url)
                mhtml_path.parent.mkdir(parents=True, exist_ok=False)
                with open(mhtml_path, "w") as file:
                    file.write(mhtml_str)

    # Load the desired tests
    generator = PytestTestGenerator()
    tests = [generator.generate_test(e) for e in examples]

    if args.count:
        for i in range(args.count - 1):
            for e in examples:
                copy = e.model_copy()
                copy.id = f"{copy.id}_{i + 2}"
                tests.append(generator.generate_test(copy))

    # Run the tests and return the exit code
    return run_tests(
        tests,
        agent,
        args.pytest_args,
        args.xdist_args,
        args.headless,
        args.single_browser_instance,
    )


if __name__ == "__main__":
    exit(main())
