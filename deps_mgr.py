#!/usr/bin/env python3

def get_test_repo():
	from git import Repo
	Repo.clone_from("https://github.com/kmuszyn/deps_test.git", "deps_test")

def load_config():
	import json
	with open("deps.cfg","r") as f:
		deps_config = json.load(f)
		for repo in deps_config["repos"]:
			print("{}: {}".format(repo["name"], repo["url"]))

if __name__ == "__main__":
	print("main")

	load_config()
	# get_test_repo()