import tomli

# this is needed as we want to use hatch.docs env for all doc dependencies
# but readthedocs can't use hatch env and we have to either provide setup.py or requirement.txt
# using this script we are syncing requirements.txt from docs dependencies automatically
# this is build as part of the `make sync` command

def generate_requirements(hatch_env='docs'):
    # Path to your pyproject.toml
    toml_file_path = 'pyproject.toml'

    try:
        # Open and read the pyproject.toml file
        with open(toml_file_path, 'rb') as toml_file:
            toml_data = tomli.load(toml_file)

        # Extract dependencies for the specific Hatch environment
        dependencies = toml_data.get('tool', {}).get('hatch', {}).get('envs', {}).get(hatch_env, {}).get('dependencies',
                                                                                                       [])

        # Write dependencies to requirements.txt
        if dependencies:
            with open('docs/requirements.txt', 'w') as req_file:
                for dependency in dependencies:
                    req_file.write(f"{dependency}\n")
            print("requirements.txt generated successfully.")
        else:
            print("No dependencies found for the specified environment.")

    except FileNotFoundError as e:
        print("The pyproject.toml file was not found.")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


if __name__ == "__main__":
    generate_requirements()
