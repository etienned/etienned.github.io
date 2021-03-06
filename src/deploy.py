#! /usr/bin/env python

import subprocess
import sys


def run(args, check_err=True):
    """
    Simplified subprocess runner. Check also return code and stderr and exit
    on problems.
    """
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return_code = process.poll()
    if return_code != 0 or (check_err and stderr):
        command = ' '.join(args)
        print """Problem running `%s`.
Return code: %s
STDOUT: ___________________
%s
STDERR: ___________________
%s
""" % (command, return_code, stdout, stderr)
        sys.exit(1)

    return stdout


def deploy():
    """
    Deploy Blog to Github account
    """
    # Check if where on master branch
    stdout = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    if stdout.strip() != 'master':
        print "You're not on the master branch. Switch to it before running 'deploy'."
        sys.exit(1)

    # Check that everything is commited except untracked files
    stdout = run(['git', 'status', '-s'])

    if stdout != '':
        print "Git status is not clean. Commit changes before deployment."
        print stdout
        sys.exit(1)

    # Build the blog to be sure everything is up to date
    print run(['nikola', 'build'], False)

    # Check that there's changes to commit
    stdout = run(['git', 'status', '-s'])
    if stdout != '':
        # Check if local is ahead of remote
        stdout = run(['git', 'rev-list', 'origin/master..HEAD'])
        # Add updated build files
        print run(['git', 'add', '-A', '..'])
        if stdout == '':
            # local is not ahead of remote so do a new commit
            print run(['git', 'commit', '-m', '"Rebuild site before deployment."'])
        else:
            # local is ahead so put changes made by the build in previous commit
            print run(['git', 'commit', '--amend', '-C', 'HEAD'])

    # Push repo to origin
    print run(['git', 'push', '--porcelain', 'origin', 'master'])


if __name__ == '__main__':
    deploy()
